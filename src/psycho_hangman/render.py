"""Render utilities for the hangman game."""

from __future__ import annotations

from psycho_hangman.utils import normalize_char

HANGMAN_STAGES = [
    r"""
 +---+
 |   |
     |
     |
     |
     |
=======""",
    r"""
 +---+
 |   |
 O   |
     |
     |
     |
=======""",
    r"""
 +---+
 |   |
 O   |
 |   |
     |
     |
=======""",
    r"""
 +---+
 |   |
 O   |
/|   |
     |
     |
=======""",
    r"""
 +---+
 |   |
 O   |
/|\  |
     |
     |
=======""",
    r"""
 +---+
 |   |
 O   |
/|\  |
/    |
     |
=======""",
    r"""
 +---+
 |   |
 O   |
/|\  |
/ \  |
     |
=======""",
]


def render_hangman(attempts_left: int, max_attempts: int) -> str:
    if max_attempts <= 0:
        return HANGMAN_STAGES[-1]

    attempts_used = max_attempts - attempts_left
    ratio = min(max(attempts_used / max_attempts, 0.0), 1.0)
    stage_index = int(ratio * (len(HANGMAN_STAGES) - 1))
    return HANGMAN_STAGES[stage_index]


def mask_term(term: str, guessed_letters: set[str]) -> str:
    revealed = []
    for ch in term:
        if ch.isalpha():
            normalized = normalize_char(ch)
            revealed.append(ch if normalized in guessed_letters else "_")
        else:
            revealed.append(ch)
    return " ".join(revealed)
