# Changelog

All notable changes to PyUI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Phase 0: Project setup and foundations
  - `pyproject.toml` with hatchling build system
  - Package skeleton: `pyui` importable with `__version__`
  - `exceptions.py`: `PyUIError`, `CompilerError`, `ComponentError`, `ThemeError`, `PluginError`
  - `App` and `Page` base classes
  - `BaseComponent` with full chainable API
  - `Button`, `Text`, `Heading` starter components
  - `ReactiveVar`, `reactive()`, `computed()`, `Store` state system
  - CLI entry point with stub commands
  - `structlog` logging setup
  - Phase 0 unit tests (6 tests)
  - GitHub Actions: `test.yml`, `publish.yml`
  - `pre-commit` hooks: `ruff`, `mypy`, trailing whitespace
