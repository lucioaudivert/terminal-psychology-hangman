from psycho_hangman.render import mask_term


def test_mask_reveals_accented_letters():
    term = "proyección"
    masked = mask_term(term, {"o"})
    assert "o" in masked
    assert "ó" in masked
    assert masked.count("_") >= 1
