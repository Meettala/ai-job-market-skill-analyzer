# Changelog

## [Unreleased]

### Added

- Python 3.10–3.12 CI, Ruff, `pip check` and dependency auditing.
- Central `pyproject.toml` and development requirements.
- Strict optional-provider JSON validation and safe fallback.
- Posting delimiter escaping and bounded extraction fields.
- SQLite foreign keys, validation and duplicate-skill protection.
- True SQLite posting-count helper and denominator regression coverage.
- Nine-case labelled deterministic extraction regression set.
- Deterministic synthetic-sample byte-for-byte verification.
- End-to-end temporary-DB/JSON-export pipeline integration test.
- Committed ESCO artefact structure/count/ambiguity verification tool and tests.
- Non-root Docker build, user, Streamlit health and homepage CI smoke.
- MIT licence, security policy, contribution guide, architecture and AI handoff.

### Changed

- Public reporting language is dataset-scoped rather than framed as general market demand or candidate deficiency.
- Streamlit now displays the true posting count rather than the maximum per-skill mention count.
- Deterministic taxonomy matching is phrase-boundary aware and no longer treats ambiguous `CV` as Computer Vision.
- Provider mode is explicit and default-off; a provider key alone no longer changes the extraction path.
- ESCO documentation now reflects its actual role as a reference/lookup vocabulary rather than the active default extractor.
- Provider failures emit a generic warning instead of raw error details.
- Entered-skill comparison handles empty datasets and thresholds deterministically and is documented as literal rather than a capability/hiring score.
- Co-occurrence reporting safely handles zero-pair datasets.
- Pipeline input loading, stored-posting count and database cleanup are validated.

## [0.1.0] - 2026-07-20

- Initial synthetic-data AI job market skill analyser.
