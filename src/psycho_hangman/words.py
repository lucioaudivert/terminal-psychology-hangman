"""Load and select psychology concepts."""

from __future__ import annotations

import json
import os
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Concept:
    term: str
    hint: str
    category: str
    difficulty: str


def _data_dir() -> Path:
    env_path = os.getenv("PSYCHO_HANGMAN_DATA_PATH")
    if env_path:
        return Path(env_path)

    repo_data = Path(__file__).resolve().parents[2] / "data"
    if repo_data.exists():
        return repo_data

    package_data = Path(__file__).resolve().parent / "data"
    if package_data.exists():
        return package_data

    raise FileNotFoundError("Concepts data directory not found.")


def load_concepts(lang: str) -> list[Concept]:
    """Load concepts for the given language."""
    if lang not in {"en", "es"}:
        raise ValueError("Language must be 'en' or 'es'.")

    data_path = _data_dir() / f"concepts_{lang}.json"
    with data_path.open("r", encoding="utf-8") as handle:
        raw_items = json.load(handle)

    concepts = []
    for item in raw_items:
        concepts.append(
            Concept(
                term=item["term"],
                hint=item["hint"],
                category=item["category"].lower(),
                difficulty=item["difficulty"].lower(),
            )
        )
    return concepts


def filter_concepts(
    concepts: Iterable[Concept], category: str | None, difficulty: str | None
) -> list[Concept]:
    filtered = list(concepts)
    if category:
        category_norm = category.lower()
        filtered = [c for c in filtered if c.category == category_norm]
    if difficulty:
        difficulty_norm = difficulty.lower()
        filtered = [c for c in filtered if c.difficulty == difficulty_norm]
    return filtered


def select_concept(concepts: list[Concept], seed: int | None = None) -> Concept:
    if not concepts:
        raise ValueError("No concepts available for selection.")
    if seed is None:
        return random.choice(concepts)
    rng = random.Random(seed)
    return rng.choice(concepts)
