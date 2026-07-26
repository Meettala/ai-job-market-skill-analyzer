# Architecture

## Data flow

```text
Synthetic or permitted postings
          |
          v
Posting validation
          |
          v
Deterministic taxonomy extraction
          |
          +---- optional provider ----> strict JSON validation
          |                              delimiter escaping
          |                              safe fallback
          v
Parameterised SQLite storage
          |
          v
Pandas / SQL aggregation
          |
          +---- skill frequency
          +---- skill co-occurrence
          +---- candidate gap report
          v
JSON export + Streamlit dashboard
```

## Trust boundaries

Posting text and optional provider output are untrusted. Posting text is escaped before provider submission. Provider output must be a bounded JSON list whose items contain exactly `skill`, `category` and `evidence` string fields. Invalid provider output never replaces deterministic extraction.

SQLite writes are parameterised, foreign keys are enabled and duplicate skills per posting are rejected. Reports are deterministic and contain no model-generated claims.

## Key modules

- `src/analyzer/taxonomy.py` — public skill taxonomy and variants.
- `src/analyzer/extractor.py` — deterministic extraction and safe provider fallback.
- `src/analyzer/llm_extractor.py` — optional provider calls and strict parsing.
- `src/analyzer/db.py` — validated parameterised SQLite storage.
- `src/analyzer/report.py` — deterministic frequency, co-occurrence and gap calculations.
- `src/analyzer/pipeline.py` — validated end-to-end orchestration and JSON export.
- `streamlit_app/app.py` — evidence-first portfolio interface.

## Limitations

The public sample is synthetic and does not represent complete or real-time labour-market demand. Keyword extraction can miss synonyms outside the taxonomy. Optional model extraction can still be imperfect even after schema validation. A production service requires licensed ingestion, evaluation data, observability and governance.
