"""Command-line interface for the hangman game."""

from __future__ import annotations

import argparse
import sys

from psycho_hangman.game import Game, GuessResult
from psycho_hangman.render import mask_term, render_hangman
from psycho_hangman.utils import is_single_letter, normalize
from psycho_hangman.words import filter_concepts, load_concepts, select_concept

MESSAGES = {
    "en": {
        "title": "Terminal Psychology Hangman",
        "instructions": "Type a letter, a full word, or 'hint' / 'quit'.",
        "prompt": "Guess: ",
        "word": "Term",
        "attempts_left": "Attempts left",
        "guessed_letters": "Guessed letters",
        "correct_letter": "Correct letter.",
        "incorrect_letter": "Incorrect letter.",
        "already_letter": "You already guessed that letter.",
        "correct_word": "You guessed the term!",
        "incorrect_word": "Wrong guess.",
        "already_word": "You already tried that word.",
        "hint": "Hint",
        "hint_used": "Hint: {hint} (-1 attempt)",
        "win": "You won! The term was: {term}",
        "lose": "You lost. The term was: {term}",
        "invalid_input": "Enter a single letter, a word, 'hint', or 'quit'.",
        "no_matches": "No concepts match the selected filters.",
    },
    "es": {
        "title": "Ahorcado de Psicologia en Terminal",
        "instructions": "Escribe una letra, una palabra completa, o 'hint' / 'quit'.",
        "prompt": "Tu intento: ",
        "word": "Termino",
        "attempts_left": "Intentos restantes",
        "guessed_letters": "Letras usadas",
        "correct_letter": "Letra correcta.",
        "incorrect_letter": "Letra incorrecta.",
        "already_letter": "Ya probaste esa letra.",
        "correct_word": "Adivinaste el termino!",
        "incorrect_word": "Intento incorrecto.",
        "already_word": "Ya probaste esa palabra.",
        "hint": "Pista",
        "hint_used": "Pista: {hint} (-1 intento)",
        "win": "Ganaste! El termino era: {term}",
        "lose": "Perdiste. El termino era: {term}",
        "invalid_input": "Ingresa una letra, una palabra, 'hint' o 'quit'.",
        "no_matches": "No hay conceptos con esos filtros.",
    },
}

COLORS = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "cyan": "\033[36m",
    "bold": "\033[1m",
    "reset": "\033[0m",
}


def style(text: str, color: str, enabled: bool) -> str:
    if not enabled:
        return text
    return f"{COLORS[color]}{text}{COLORS['reset']}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bilingual terminal hangman game.")
    parser.add_argument("--lang", choices=["en", "es"], default="en")
    parser.add_argument("--category", type=str, default=None)
    parser.add_argument("--difficulty", choices=["easy", "medium", "hard"], default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--max-attempts", type=int, default=6)
    parser.add_argument("--no-color", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.max_attempts < 1:
        print("--max-attempts must be at least 1")
        return 2

    messages = MESSAGES[args.lang]
    color_enabled = not args.no_color

    concepts = load_concepts(args.lang)
    concepts = filter_concepts(concepts, args.category, args.difficulty)
    if not concepts:
        print(messages["no_matches"])
        return 1

    concept = select_concept(concepts, seed=args.seed)
    game = Game(concept, max_attempts=args.max_attempts)

    print(style(messages["title"], "bold", color_enabled))
    print(messages["instructions"])

    while True:
        print(render_hangman(game.attempts_left, game.max_attempts))
        print(f"{messages['word']}: {mask_term(concept.term, game.guessed_letters)}")
        print(f"{messages['attempts_left']}: {game.attempts_left}/{game.max_attempts}")
        if game.guessed_letters:
            guessed = ", ".join(sorted(game.guessed_letters))
            print(f"{messages['guessed_letters']}: {guessed}")

        user_input = input(messages["prompt"]).strip()
        if not user_input:
            continue

        command = user_input.lower()
        if command == "quit":
            return 0
        if command == "hint":
            hint_text = game.use_hint()
            print(style(messages["hint_used"].format(hint=hint_text), "yellow", color_enabled))
        elif is_single_letter(user_input):
            result = game.guess_letter(user_input)
            if result == GuessResult.CORRECT:
                print(style(messages["correct_letter"], "green", color_enabled))
            elif result == GuessResult.INCORRECT:
                print(style(messages["incorrect_letter"], "red", color_enabled))
            elif result == GuessResult.ALREADY:
                print(messages["already_letter"])
            else:
                print(messages["invalid_input"])
        else:
            if len(normalize(user_input)) < 2:
                print(messages["invalid_input"])
            else:
                result = game.guess_word(user_input)
                if result == GuessResult.CORRECT:
                    print(style(messages["correct_word"], "green", color_enabled))
                elif result == GuessResult.INCORRECT:
                    print(style(messages["incorrect_word"], "red", color_enabled))
                elif result == GuessResult.ALREADY:
                    print(messages["already_word"])
                else:
                    print(messages["invalid_input"])

        if game.is_won():
            print(style(messages["win"].format(term=concept.term), "green", color_enabled))
            return 0
        if game.is_lost():
            print(style(messages["lose"].format(term=concept.term), "red", color_enabled))
            return 0


if __name__ == "__main__":
    raise SystemExit(main())
