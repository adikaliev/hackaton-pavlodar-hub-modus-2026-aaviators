"""Convert the organizers' .docx files to Markdown, and the demo dataset to JSON.

Standard library only. Run from the project root:
    python tools/convert_source_docs.py docs/source/task-spec_TZ.docx docs/source/dataset.docx docs data
Writes docs/task-spec.md, docs/dataset.md and data/seed_requests.json.
"""
import sys, zipfile, re, json
from pathlib import Path
from xml.etree import ElementTree as ET
sys.stdout.reconfigure(encoding="utf-8")
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

def paras(path):
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read('word/document.xml'))
    for p in root.find(W + 'body').iter(W + 'p'):
        st = p.find(f'{W}pPr/{W}pStyle')
        text = ''.join(t.text or '' for t in p.iter(W + 't')).strip()
        if text:
            yield (st.get(W + 'val') if st is not None else ''), text

def to_md(path, style_map):
    out, n = [], 0
    for style, text in paras(path):
        kind = style_map.get(style, 'p')
        if kind != 'ol':
            n = 0
        if kind.startswith('h'):
            out += ['', '#' * int(kind[1]) + ' ' + text, '']
        elif kind == 'ul':
            out.append('- ' + text)
        elif kind == 'ol':
            if text.startswith('- '):          # TZ section 6 questions are typed with a dash
                out.append(text)
            else:
                n += 1
                out.append(f'{n}. ' + text)
        elif kind == 'sub':
            out += [f'_{text}_', '']
        else:
            if out and out[-1].startswith(('- ', '1.', '2.', '3.', '4.', '5.', '6.', '7.')):
                out.append('')
            out += [text, '']
    md = '\n'.join(out)
    return re.sub(r'\n{3,}', '\n\n', md).strip() + '\n'

tz, ds, out_dir, data_dir = map(Path, sys.argv[1:5])
SRC_NOTE = '<!-- Generated from docs/source/{name} by tools/convert_source_docs.py. Do not edit by hand. -->\n\n'

tz_md = to_md(tz, {'aa': 'h1', '1': 'h2', '21': 'h3', 'a0': 'ul', 'a': 'ol'})
# The TZ has a two-line title block: make the subtitle lines plain text under the H1
(out_dir / 'task-spec.md').write_text(SRC_NOTE.format(name=tz.name) + tz_md, encoding='utf-8')

ds_md = to_md(ds, {'Title': 'h1', 'Subtitle': 'sub', 'Heading1': 'h2', 'Heading2': 'h3',
                   'ListBullet': 'ul', 'ListNumber': 'ol'})
(out_dir / 'dataset.md').write_text(SRC_NOTE.format(name=ds.name) + ds_md, encoding='utf-8')

# --- dataset -> JSON -------------------------------------------------------
items, cur = [], None
for style, text in paras(ds):
    if style == 'Heading2':
        rid, rtype, cat = [s.strip() for s in text.split('·')]
        cur = {'id': rid, 'type': rtype, 'category': cat}
        items.append(cur)
    elif cur is not None and style == 'Heading1':
        cur = None
    elif cur is not None:
        if text.startswith('Автор:'):
            m = re.match(r'Автор:\s*(.+?)\s{2,}Приоритет:\s*(.+?)\s{2,}Статус:\s*(.+)$', text)
            cur.update(author_role=m[1], priority=m[2], status=m[3])
        elif text.startswith('Текст обращения.'):
            cur['text'] = text.removeprefix('Текст обращения.').strip()
        elif text.startswith('Условный ответственный:'):
            m = re.match(r'Условный ответственный:\s*(.+?)\s{2,}Пример дальнейшего действия:\s*(.+)$', text)
            cur.update(assignee_role=m[1], next_action=m[2])
        else:
            raise SystemExit(f'unparsed line in {cur["id"]}: {text!r}')
keys = ['id', 'type', 'category', 'author_role', 'priority', 'status', 'text', 'assignee_role', 'next_action']
missing = [(i['id'], k) for i in items for k in keys if k not in i]
assert not missing, missing
(data_dir / 'seed_requests.json').write_text(
    json.dumps([{k: i[k] for k in keys} for i in items], ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'{len(items)} requests;',
      'types:', sorted({i["type"] for i in items}),
      'statuses:', sorted({i["status"] for i in items}),
      'priorities:', sorted({i["priority"] for i in items}),
      'categories:', len({i["category"] for i in items}))
