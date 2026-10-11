# My First Python Project

This is a simple Python project starter that includes:
- a package structure
- a command-line interface (CLI)
- a test file
- project configuration via `pyproject.toml`

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
python -m my_first_python_project
```

Example output:

```bash
Hello, World!
```

You can also pass a name:

```bash
python -m my_first_python_project GitHub
```

## Running tests

```bash
pytest
```
