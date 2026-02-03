"""Game state and rules for hangman."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from psycho_hangman.utils import normalize
from psycho_hangman.words import Concept


class GuessResult(str, Enum):
    CORRECT = "correct"
    INCORRECT = "incorrect"
    ALREADY = "already"
    INVALID = "invalid"


@dataclass
class Game:
    concept: Concept
    max_attempts: int = 6
    attempts_left: int = field(init=False)
    guessed_letters: set[str] = field(default_factory=set, init=False)
    guessed_words: set[str] = field(default_factory=set, init=False)
    hints_used: int = field(default=0, init=False)

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        self.attempts_left = self.max_attempts
        self._normalized_term = normalize(self.concept.term)

    @property
    def normalized_term(self) -> str:
        return self._normalized_term

    def is_won(self) -> bool:
        return set(self._normalized_term).issubset(self.guessed_letters)

    def is_lost(self) -> bool:
        return self.attempts_left <= 0 and not self.is_won()

    def guess_letter(self, letter: str) -> GuessResult:
        normalized = normalize(letter)
        if len(normalized) != 1:
            return GuessResult.INVALID
        if normalized in self.guessed_letters:
            return GuessResult.ALREADY

        self.guessed_letters.add(normalized)
        if normalized in self._normalized_term:
            return GuessResult.CORRECT

        self.attempts_left = max(0, self.attempts_left - 1)
        return GuessResult.INCORRECT

    def guess_word(self, word: str) -> GuessResult:
        normalized = normalize(word)
        if len(normalized) < 1:
            return GuessResult.INVALID
        if normalized in self.guessed_words:
            return GuessResult.ALREADY

        self.guessed_words.add(normalized)
        if normalized == self._normalized_term:
            self.guessed_letters.update(set(self._normalized_term))
            return GuessResult.CORRECT

        self.attempts_left = max(0, self.attempts_left - 1)
        return GuessResult.INCORRECT

    def use_hint(self) -> str:
        self.hints_used += 1
        self.attempts_left = max(0, self.attempts_left - 1)
        return self.concept.hint
