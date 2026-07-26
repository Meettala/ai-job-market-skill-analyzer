# Changelog

## [Unreleased]

### Added

- Python 3.10–3.12 CI, Ruff and dependency auditing.
- Central `pyproject.toml` and development requirements.
- Strict optional-provider JSON validation and safe fallback.
- Posting delimiter escaping and bounded extraction fields.
- SQLite foreign keys, validation and duplicate-skill protection.
- Reporting edge-case and provider failure tests.
- Accessible Streamlit portfolio interface.
- Non-root Docker image and health check.
- MIT licence, security policy, contribution guide, architecture and AI handoff.

### Changed

- Provider failures now emit a generic warning instead of raw error details.
- Gap reporting now handles empty datasets and thresholds deterministically.
- Co-occurrence reporting safely handles zero-pair datasets.
- Pipeline input loading and database cleanup are validated.

## [0.1.0] - 2026-07-20

- Initial synthetic-data AI job market skill analyser.
