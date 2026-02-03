"""Utility helpers for input normalization and validation."""

from __future__ import annotations

ACCENT_TRANSLATION = str.maketrans(
    {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "ü": "u",
        "ñ": "n",
    }
)


def normalize(text: str) -> str:
    """Normalize text for matching: lowercase, remove accents, keep letters only."""
    cleaned = text.strip().lower().translate(ACCENT_TRANSLATION)
    return "".join(ch for ch in cleaned if ch.isalpha())


def normalize_char(ch: str) -> str:
    """Normalize a single character to its matching form."""
    if not ch:
        return ""
    lowered = ch.lower().translate(ACCENT_TRANSLATION)
    if lowered.isalpha():
        return lowered
    return ""


def is_single_letter(text: str) -> bool:
    """Return True if the input is exactly one alphabetic character."""
    stripped = text.strip()
    return len(stripped) == 1 and stripped.isalpha()
