"""Text matching without AI: similar requests and a category suggestion.

Deliberately simple and transparent: words are lower-cased, short and common
words are dropped, and the rest are cut to a stem of six letters. Two texts are
similar when they share enough stems. An AI model can replace this later behind
the same two functions (solution design, section 7: "AI suggests, a person confirms").
"""
from __future__ import annotations

import re

from ..models import Appeal, Category

_WORD = re.compile(r"[a-zа-яё0-9]+", re.IGNORECASE)
_STOP = {
    "чтобы", "когда", "иногда", "всегда", "можно", "нужно", "нужна", "нужен", "нужны", "было", "были", "будет",
    "этого", "этом", "этой", "этот", "того", "также", "очень", "если", "либо", "какой", "какие", "какая",
    "которые", "который", "которых", "между", "после", "перед", "предлагаю", "хотелось", "полезно", "через",
    "более", "менее", "только", "свой", "своих", "наших", "наши", "есть", "может", "могут", "хочу", "сейчас",
    "просто", "чего", "ними", "него", "всех", "этих", "один", "одного", "одних", "разных", "разные", "другие",
}
_STEM = 6


def stems(text: str) -> set[str]:
    result = set()
    for word in _WORD.findall((text or "").lower().replace("ё", "е")):
        if len(word) < 4 or word in _STOP:
            continue
        result.add(word[:_STEM])
    return result


def similarity(a: set[str], b: set[str]) -> tuple[int, float]:
    """(shared stems, share of the shorter text that is shared)."""
    if not a or not b:
        return 0, 0.0
    shared = len(a & b)
    return shared, shared / min(len(a), len(b))


def find_similar(text: str, queryset, limit: int = 3, exclude_pk=None) -> list[Appeal]:
    """Open or recently handled requests on the same theme, best match first."""
    wanted = stems(text)
    if len(wanted) < 3:
        return []
    scored = []
    for appeal in queryset:
        if appeal.pk == exclude_pk:
            continue
        shared, share = similarity(wanted, stems(appeal.text))
        if shared >= 3 and share >= 0.3:
            scored.append((shared, share, appeal))
    scored.sort(key=lambda item: (item[0], item[1]), reverse=True)
    return [appeal for _, _, appeal in scored[:limit]]


def suggest_category(text: str) -> Category | None:
    """The category whose keywords occur most often in the text, or None."""
    wanted = stems(text)
    if not wanted:
        return None
    best, best_score = None, 0
    for category in Category.objects.filter(is_active=True).exclude(keywords=""):
        keys = set()
        for phrase in category.keywords.split(","):
            keys |= stems(phrase)
        score = len(wanted & keys)
        if score > best_score:
            best, best_score = category, score
    return best
