# AI Job Market Skill Analyzer

A safety-first Python and Streamlit application that extracts skills from permitted AI/ML job postings, ranks market demand, analyses skill co-occurrence and produces an evidence-backed candidate gap report.

![Architecture](docs/assets/architecture.svg)

## Why this project exists

Career roadmaps often rely on generic advice. This project demonstrates how to turn a defined posting dataset into reproducible skill-demand evidence while keeping the public demo safe, transparent and useful without an API key.

The repository uses synthetic sample postings rather than scraped restricted data. It does not claim complete or real-time labour-market coverage.

## Engineering highlights

- Deterministic no-key taxonomy extraction.
- Optional OpenAI or Anthropic extraction with strict JSON validation.
- Untrusted posting text escaped before provider submission.
- Generic safe fallback after provider or parsing failure.
- Parameterised SQLite storage with foreign keys and duplicate protection.
- Deterministic pandas/SQL frequency, co-occurrence and candidate-gap reports.
- Empty-data, malformed-input, duplicate-skill and provider-failure tests.
- Python 3.10–3.12 CI, Ruff and dependency auditing.
- Accessible Streamlit interface and non-root Docker image.

## Architecture

```text
Synthetic or permitted postings
          |
          v
Validation + deterministic extraction
          |
          +---- optional provider ----> strict bounded JSON validation
          |                              safe fallback
          v
Parameterised SQLite storage
          |
          v
Pandas / SQL reporting
          |
          +---- demand frequency
          +---- skill pairs
          +---- candidate gaps
          v
JSON export + Streamlit dashboard
```

See [`docs/architecture.md`](docs/architecture.md) for the detailed trust model.

## Quick start

Requirements: Python 3.10 or later.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m src.analyzer.pipeline
streamlit run streamlit_app/app.py
```

On Windows, activate the environment with:

```powershell
.venv\Scripts\activate
```

Open `http://localhost:8501`.

## Optional provider extraction

Install one optional provider package:

```bash
python -m pip install "openai>=1.0,<3.0"
# or
python -m pip install "anthropic>=0.30,<1.0"
```

Set `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` in your local environment. Never commit credentials. Posting excerpts may be sent to the configured provider, so do not submit confidential or restricted data.

The rule-based path remains available when no key is configured or when provider output fails validation.

## Verification

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
ruff check src streamlit_app tests data
pip-audit -r requirements.txt
```

GitHub Actions runs the tests on Python 3.10, 3.11 and 3.12, then runs Ruff and dependency auditing.

## Docker demo

```bash
docker build -t ai-job-market-skill-analyzer .
docker run --rm -p 8501:8501 ai-job-market-skill-analyzer
```

The container runs as a non-root user and includes a health check. Provider credentials must be passed at runtime, never baked into the image.

## Safety and data policy

- Public sample postings are synthetic.
- Use only licensed or explicitly permitted datasets.
- Provider output is untrusted and never executed.
- SQL is parameterised.
- Gap-report claims are calculated from the analysed dataset.
- The project does not claim perfect extraction, complete market coverage or immunity from every prompt-injection technique.

See [`SECURITY.md`](SECURITY.md) and the existing documents under `docs/security/`.

## Known limitations

- Keyword extraction can miss synonyms outside the taxonomy.
- The synthetic sample is small and not a live market feed.
- Optional model extraction can still be imperfect after schema validation.
- Candidate skills are self-entered and are not independently verified.
- A production service requires licensed ingestion, identity, monitoring and governance.

## Portfolio evidence

This project demonstrates Python, pandas, SQLite, Streamlit, optional LLM integration, validation, safe fallback, prompt-injection awareness, automated testing, CI, dependency security and Docker packaging.

Presentation instructions and CV/interview wording are in [`docs/PORTFOLIO_PRESENTATION_GUIDE.md`](docs/PORTFOLIO_PRESENTATION_GUIDE.md).

## Licence

MIT. See [`LICENSE`](LICENSE).

## Author

Built by [Meet Tala](https://github.com/Meettala).
