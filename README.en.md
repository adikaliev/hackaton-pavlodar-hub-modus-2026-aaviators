# Modus Trade hackathon 2026: employee feedback and suggestions system

[Русская версия](README.md)

Hackathon entry for the ГК «Модус Трейд» track (Pavlodar IT Hub). Employees submit problems and improvement ideas. Each request gets an owner and a deadline, the author can follow its status through to a result, and management sees everything on one screen.

- Submission deadline: **13 Nov 2026, 14:00**. Final: **16 Nov 2026**, Pavlodar.
- Start with [docs/solution-design.en.md](docs/solution-design.en.md) (how the solution works) and [docs/value-proposition.en.md](docs/value-proposition.en.md) (value and how it differs from competitors).

## Repository layout

```
docs/
  solution-design.md           processes, roles, access, integrations
  value-proposition.md         value proposition, competitor comparison, answers to objections
  task-spec.md                 the spec (ТЗ), converted from .docx
  dataset.md                   demo requests and demo scenarios, converted from .docx
data/
  seed_requests.json           the 20 demo requests as JSON
tools/
  convert_source_docs.py       regenerates task-spec.md, dataset.md and seed_requests.json
```

The documents in `docs/` have English versions with the `.en.md` suffix.

## Setup, run, test

The tech stack isn't chosen yet. This section will hold setup, run and test commands once there is an app.

To regenerate the converted docs (Python 3.12, standard library only). This needs the organizers' original `.docx` files in `docs/source/`; they aren't in the repository.

```
python tools/convert_source_docs.py docs/source/task-spec_TZ.docx docs/source/dataset.docx docs data
```

## Documentation

The main version of each document is in Russian; the English version sits next to it with the `.en.md` suffix (e.g. `README.en.md`). Update both when you change one.
