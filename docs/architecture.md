# Architecture

## Data flow

```text
Synthetic or explicitly permitted postings
          |
          v
Posting validation
          |
          v
Curated deterministic AI/ML taxonomy extraction
          |
          +---- explicit optional provider ----> strict bounded JSON validation
          |                                      delimiter escaping
          |                                      safe fallback
          v
Parameterised SQLite storage
          |
          v
Deterministic pandas / SQL aggregation
          |
          +---- skill frequency in analysed postings
          +---- recurring skill co-occurrence
          +---- entered-skill comparison
          v
JSON export + Streamlit dashboard
```

## Trust boundaries

Posting text and optional provider output are untrusted. External provider extraction is default-off and requires both `ENABLE_PROVIDER_MODE=true` and a supported provider key. A secret present in the environment by itself must not change the extraction path.

When provider mode is enabled, posting text is escaped before provider submission. Provider output must be a bounded JSON list whose items contain exactly `skill`, `category` and `evidence` string fields. Invalid provider output never replaces deterministic extraction and is never executed.

SQLite writes are parameterised, foreign keys are enabled and duplicate skills per posting are rejected. Posting frequency uses the true number of rows in `postings` as its denominator and counts distinct posting IDs per skill.

Reports are deterministic and dataset-scoped. The entered-skill comparison is a literal label comparison; it is not a capability assessment, ATS score or hiring-probability estimate.

## ESCO reference vocabulary boundary

`data/esco-vocabulary.json.gz` is a separately attributed ESCO reference artefact. `src/analyzer/esco_vocabulary.py` validates its structure/count metadata and supports exact surface-form lookup, including ambiguous labels that map to multiple concept URIs.

The ESCO artefact is **not** the active default extractor. The deterministic extraction path remains the curated taxonomy in `src/analyzer/taxonomy.py`. This avoids an unbounded all-ESCO phrase matcher whose ambiguity/performance characteristics have not been evaluated.

## Key modules

- `src/analyzer/taxonomy.py` — curated AI/ML skill taxonomy and variants.
- `src/analyzer/extractor.py` — deterministic boundary-aware extraction and safe provider fallback.
- `src/analyzer/provider_config.py` — explicit provider activation boundary.
- `src/analyzer/llm_extractor.py` — optional provider calls and strict parsing.
- `src/analyzer/db.py` — validated parameterised SQLite storage and true posting count.
- `src/analyzer/report.py` — deterministic dataset-scoped frequency, co-occurrence and entered-skill calculations.
- `src/analyzer/pipeline.py` — validated end-to-end orchestration and JSON export.
- `src/analyzer/esco_vocabulary.py` — ESCO reference artefact validation and lookup.
- `streamlit_app/app.py` — dataset-scoped portfolio interface.

## Limitations

The public sample is synthetic and non-representative. Keyword/phrase extraction can miss synonyms outside the curated taxonomy. Optional provider extraction can still be imperfect after schema validation. The ESCO reference artefact is not evidence of all-domain extraction or market demand. A production service requires licensed ingestion, provenance/freshness metadata, deduplication, evaluation data, observability, privacy controls and governance.
