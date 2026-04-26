# Contributing to Zolt

Thank you for your interest in contributing! 🎉

## Setup

```bash
git clone https://github.com/12errh/zolt
cd zolt
pip install -e ".[dev]"
pre-commit install
```

## Running Tests

```bash
pytest             # All tests
pytest -k unit     # Unit tests only
pytest --cov=pyui  # With coverage
```

## Code Style

We use `ruff` for linting and formatting:

```bash
ruff check src/ tests/
ruff format src/ tests/
```

## Type Checking

```bash
mypy src/
```

## Pull Requests

1. Fork the repo and create a branch: `git checkout -b feat/my-feature`
2. Write tests for new code
3. Ensure all checks pass (`pytest`, `ruff`, `mypy`)
4. Open a PR against `main` branch

## Reporting Issues

Use GitHub Issues. Include:
- Zolt version (`zolt --version`)
- Python version
- OS
- Minimal reproduction code

## Code of Conduct

Be kind, inclusive, and constructive. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
