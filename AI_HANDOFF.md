# AI Handoff — AI Job Market Skill Analyzer

> Paste this file into another AI assistant to continue the project without restarting it. Always verify the live repository, active pull requests, branch head, dependency versions and CI before editing.

## Continuation instruction

You are continuing `Meettala/ai-job-market-skill-analyzer`, a public portfolio project owned by Meet Tala.

Do not weaken the synthetic-data boundary, deterministic rule-based extraction path, candidate-gap evidence model or optional-provider validation. Inspect the live code, tests, README and security documentation before changing behaviour. Add tests for material changes and update this file after code, security, dependency, deployment, documentation or portfolio work.

Never commit API keys, scraped restricted data, private candidate documents, employer data, customer data or confidential production details.

## Repository state

- Default branch: `main`
- Working branch: `agent/professional-repository-foundation`
- Starting commit: `fc6e6cb0adf3b76d5617aa745bf4baf5f3be96cb`
- Existing pull requests before this work: none
- Repository visibility: public
- Stack described by the starting README: Python, pandas, SQLite, Streamlit, pytest, optional OpenAI/Anthropic extraction
- Last updated: 26 July 2026

## Product purpose

The application analyses AI/ML job postings, extracts and ranks skills, stores results in SQLite, produces frequency/co-occurrence and candidate-gap reports, exports portfolio data and provides a Streamlit dashboard.

The public repository uses synthetic sample postings rather than scraped restricted data. That boundary must remain explicit.

## Initial audit plan

1. Inspect all extractor, database, report, pipeline, Streamlit, data-generation and test files.
2. Establish a reproducible baseline with Python 3.10–3.12 CI.
3. Add central packaging and lint configuration.
4. Verify rule-based extraction, optional provider parsing and prompt-injection handling.
5. Validate database schema, repeat-run behaviour and SQL parameterisation.
6. Validate ranking, co-occurrence and candidate-gap calculations.
7. Add malformed input, duplicate posting, empty data and provider-failure tests.
8. Improve safe user-facing errors and portfolio UI.
9. Add dependency auditing, Docker support and repository governance.
10. Rework README and add architecture, roadmap, presentation assets and a beginner-friendly portfolio guide.
11. Keep the pull request draft until every quality/security gate passes.
12. Merge only after the exact final head is green and the security/recruiter review is complete.

## Decisions to preserve

- Synthetic or explicitly permitted datasets only in the public repository.
- Deterministic no-key extraction remains a first-class mode.
- Optional provider output is untrusted and must not be executed.
- Gap-report claims must be traceable to analysed postings and the candidate skill list.
- Documentation must not claim perfect accuracy, complete market coverage or immunity from all prompt injection.
- A future paid production service should use a separate private proprietary repository with governed data ingestion and commercial controls.
