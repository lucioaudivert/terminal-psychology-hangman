from psycho_hangman.game import Game, GuessResult
from psycho_hangman.words import Concept


def make_concept(term: str = "apego") -> Concept:
    return Concept(
        term=term,
        hint="test hint",
        category="clinica",
        difficulty="easy",
    )


def test_guess_letter_correct_does_not_cost_attempt():
    game = Game(make_concept("apego"), max_attempts=6)
    result = game.guess_letter("a")
    assert result == GuessResult.CORRECT
    assert game.attempts_left == 6


def test_guess_letter_incorrect_costs_attempt():
    game = Game(make_concept("apego"), max_attempts=6)
    result = game.guess_letter("z")
    assert result == GuessResult.INCORRECT
    assert game.attempts_left == 5


def test_guess_word_correct_wins():
    game = Game(make_concept("apego"), max_attempts=6)
    result = game.guess_word("apego")
    assert result == GuessResult.CORRECT
    assert game.is_won()


def test_guess_word_incorrect_costs_attempt():
    game = Game(make_concept("apego"), max_attempts=6)
    result = game.guess_word("ansiedad")
    assert result == GuessResult.INCORRECT
    assert game.attempts_left == 5


def test_hint_costs_attempt():
    game = Game(make_concept("apego"), max_attempts=6)
    hint = game.use_hint()
    assert hint == "test hint"
    assert game.attempts_left == 5


def test_win_condition_by_letters():
    game = Game(make_concept("apego"), max_attempts=6)
    for letter in ["a", "p", "e", "g", "o"]:
        game.guess_letter(letter)
    assert game.is_won()


def test_lose_condition_when_attempts_run_out():
    game = Game(make_concept("apego"), max_attempts=2)
    game.guess_letter("x")
    game.guess_letter("y")
    assert game.is_lost()
