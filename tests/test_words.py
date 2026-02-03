from psycho_hangman.words import filter_concepts, load_concepts, select_concept


def test_language_selection_loads_correct_dataset():
    en_terms = {c.term for c in load_concepts("en")}
    es_terms = {c.term for c in load_concepts("es")}
    assert "attachment" in en_terms
    assert "apego" in es_terms


def test_seed_deterministic_selection():
    concepts = load_concepts("en")
    first = select_concept(concepts, seed=42).term
    second = select_concept(concepts, seed=42).term
    assert first == second


def test_filter_by_category_and_difficulty():
    concepts = load_concepts("en")
    filtered = filter_concepts(concepts, category="learning", difficulty="hard")
    assert len(filtered) == 1
    assert filtered[0].term == "habituation"
