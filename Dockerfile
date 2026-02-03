FROM python:3.11-slim

WORKDIR /app

COPY src/ /app/src/
COPY data/ /app/data/
COPY pyproject.toml README.md /app/

ENV PYTHONPATH=/app/src
ENV PSYCHO_HANGMAN_DATA_PATH=/app/data

ENTRYPOINT ["python", "-m", "psycho_hangman.cli"]
