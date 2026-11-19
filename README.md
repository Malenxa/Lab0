# Lab 0: Fundamentals of Continuous Integration

This repository contains the implementation of a data preprocessing library and its Command Line Interface (CLI), along with unit and integration tests following Continuous Integration (CI) and MLOps best practices.

## Project Structure

```text
.
├── pyproject.toml
├── pytest.ini
├── README.md
├── src/
│   ├── __init__.py
│   ├── cli.py
│   └── preprocessing.py
├── tests/
│   ├── __init__.py
│   ├── test_cli.py
│   └── test_logic.py
└── uv.lock
```

## Setup and Installation

This project uses `uv` to manage the virtual environment and dependencies (`click`, `black`, `pylint`, `pytest`, `pytest-cov`).

1. Clone the repository:
   ```bash
   git clone https://github.com/Malenxa/Lab0.git
   cd Lab0
   ```

2. Sync the virtual environment and install dependencies:
   ```bash
   uv sync
   ```

## CLI Usage

All CLI commands are organized into four groups under `cli`: `clean`, `numeric`, `text`, and `struct`. Run commands from the project root using `uv run`:

```bash
uv run python -m src.cli --help
```

### Examples by Group

* **Clean (`clean`):**
  ```bash
  uv run python -m src.cli clean remove-missing a "" b c
  uv run python -m src.cli clean fill-missing a "" b --fill-value N/A
  ```

* **Numeric (`numeric`):**
  ```bash
  uv run python -m src.cli numeric normalize 10 20 30 --min-val 0 --max-val 10
  uv run python -m src.cli numeric standardize 10 20 30
  uv run python -m src.cli numeric clip -- -2 0.5 3 --min-val 0 --max-val 1
  uv run python -m src.cli numeric to-integers 10 hello 25 3.5
  uv run python -m src.cli numeric log-scale -- -5 0 1 10 100
  ```

* **Text (`text`):**
  ```bash
  uv run python -m src.cli text tokenize "Hello, World 2026!"
  uv run python -m src.cli text remove-punctuation "Hello, World #1!"
  uv run python -m src.cli text remove-stopwords "The quick brown fox" -s the -s fox
  ```

* **Struct (`struct`):**
  ```bash
  uv run python -m src.cli struct shuffle a b c d --seed 42
  uv run python -m src.cli struct flatten "[[1, 2], [3, 4]]"
  uv run python -m src.cli struct unique-values a b a c b
  ```

## Code Quality and Testing

* **Linting (`pylint`):**
  ```bash
  uv run python -m pylint src/*.py tests/*.py
  ```

* **Formatting (`black`):**
  ```bash
  uv run black src/*.py tests/*.py
  ```

* **Unit & Integration Tests (`pytest`):**
  ```bash
  uv run python -m pytest -v
  ```

* **Test Coverage (`pytest-cov`):**
  ```bash
  uv run python -m pytest -v --cov=src
  ```