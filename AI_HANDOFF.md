# AI Handoff — AI Job Market Skill Analyzer

> Paste this file into another AI assistant to continue the project without restarting it. Verify the live repository, active pull requests, branch head, dependency versions and CI before editing.

## Continuation instruction

You are continuing `Meettala/ai-job-market-skill-analyzer`, a public MIT-licensed portfolio project owned by Meet Tala.

Do not weaken the synthetic-data boundary, deterministic rule-based extraction path, candidate-gap evidence model, parameterised SQLite storage or optional-provider validation. Read the live code, tests, `README.md`, `SECURITY.md`, `docs/architecture.md`, `docs/roadmap.md` and `docs/PORTFOLIO_PRESENTATION_GUIDE.md` before editing.

Never commit API keys, scraped restricted data, private candidate documents, employer data, customer data or confidential production details.

## Repository state

- Default branch: `main`
- Professionalisation branch: `agent/professional-repository-foundation`
- Pull request: PR #1, `Professionalize AI job market skill analyzer`
- Starting commit: `fc6e6cb0adf3b76d5617aa745bf4baf5f3be96cb`
- Stack: Python 3.10–3.12, pandas, SQLite, Streamlit, pytest, Ruff and optional OpenAI/Anthropic extraction
- Licence: MIT
- Last updated: 26 July 2026

## Product purpose

The application analyses synthetic or explicitly permitted AI/ML job postings, extracts skills, stores evidence in SQLite, produces frequency/co-occurrence and candidate-gap reports, exports JSON and provides a Streamlit dashboard.

The public repository does not claim complete or real-time labour-market coverage.

## Trust model

1. Public examples use synthetic or explicitly permitted data.
2. Deterministic taxonomy extraction works without an API key.
3. Posting text and provider output are untrusted.
4. Posting delimiter characters are escaped before provider submission.
5. Provider output must be a bounded JSON list with exactly `skill`, `category` and `evidence` string fields.
6. Invalid provider output or provider failure falls back to deterministic extraction.
7. SQL writes are parameterised, foreign keys are enabled and duplicate skills are rejected.
8. Reports are deterministic and traceable to analysed postings and candidate input.
9. Raw provider errors, keys and private data must not be exposed.
10. The project does not claim perfect extraction or immunity from every prompt-injection technique.

## Implemented professional foundation

- Added `pyproject.toml`, development requirements and Python 3.10–3.12 CI.
- Added Ruff and `pip-audit` quality gates.
- Added strict provider parsing, bounded fields, de-duplication and safe fallback.
- Added generic provider-error logging and delimiter escaping.
- Added validated parameterised SQLite storage, foreign keys and duplicate protection.
- Hardened empty frequency/co-occurrence data and candidate-gap thresholds.
- Added validated pipeline loading and guaranteed database closure.
- Added provider, database, reporting and failure-path tests.
- Reworked the Streamlit UI with safe startup/display errors and transparent synthetic-data labels.
- Added non-root Docker support and a health check.
- Added MIT licence, security policy, contribution guide and changelog.
- Added recruiter-focused README, architecture, roadmap and presentation guide.
- Added architecture and social-preview SVG assets.

## Verified status

Workflow run 26 passed on the integrated implementation:

- Python 3.10 tests;
- Python 3.11 tests;
- Python 3.12 tests;
- Ruff application/test/data linting;
- `pip-audit` against runtime requirements.

A final documentation-only CI run is required after this handoff update. Do not claim a later head is green without checking GitHub.

## Known limitations

- The public dataset is synthetic and small.
- Taxonomy extraction can miss synonyms outside its variants.
- Optional model extraction can still be imperfect after schema validation.
- Candidate skills are self-entered and not independently verified.
- Docker is suitable for demonstration, not a complete production platform.
- Real screenshots and video must be captured from a running application.

## Remaining presentation tasks

Follow `docs/PORTFOLIO_PRESENTATION_GUIDE.md` to capture a real screenshot, record a 30–60 second demo and upload the rendered social-preview PNG in GitHub settings.

## Rules for another AI

Inspect the live repository and CI before editing. Add positive, negative and edge-case tests for behavioural changes. Never fabricate benchmarks, real-market coverage, recruiter outcomes or screenshots. Keep future commercial ingestion and private candidate data in a separate governed private system.
