from psycho_hangman.utils import is_single_letter, normalize, normalize_char


def test_normalize_accents():
    assert normalize("áéíóúü ñ") == "aeiouun"


def test_normalize_char_enye():
    assert normalize_char("Ñ") == "n"


def test_is_single_letter():
    assert is_single_letter("á")
    assert not is_single_letter("ab")
