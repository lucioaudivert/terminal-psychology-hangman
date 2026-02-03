# Terminal Psychology Hangman

A bilingual hangman game for the terminal using psychology concepts. Default language is English, with Spanish available.

Note: public sanitized portfolio sample.

**Features**
- CLI hangman with progressive reveal
- Language selection: English or Spanish
- Filters by category and difficulty
- Optional deterministic selection with `--seed`
- Accent-insensitive matching for Spanish terms

**Quick Start**
1. `python -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -e .[dev]`
4. `psycho-hangman`

**Usage**
- `psycho-hangman`
- `psycho-hangman --lang es`
- `psycho-hangman --category cognitive --difficulty hard`
- `psycho-hangman --seed 42 --max-attempts 8`
- `psycho-hangman --no-color`

**Gameplay Commands**
- Single letter guess
- Full word guess
- `hint` costs 1 attempt
- `quit` exits

**Data**
- English concepts: `data/concepts_en.json`
- Spanish concepts: `data/concepts_es.json`

**Tests**
- `pytest`

**Docker**
- `docker build -t psycho-hangman .`
- `docker run -it --rm psycho-hangman`
