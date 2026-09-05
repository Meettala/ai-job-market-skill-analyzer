# Safety rules — Job Market Skill Analyzer

1. No scraping of job platforms whose terms disallow it. This MVP uses synthetic sample data (see `data/generate_sample_postings.py`) instead of live scraping. Real data sources may only be added through explicitly permitted or licensed ingestion with appropriate provenance controls.
2. Every posting stored keeps its `source_url` and `retrieved_at` date, so provenance remains visible. Demo data uses synthetic source URLs and is labelled synthetic in the dashboard, README and pipeline output.
3. Optional provider extraction treats posting text as untrusted input: the text is delimiter-escaped and the model is instructed not to follow instructions found inside it (see `llm_extractor.py`).
4. No provider is required for the tool to work. Deterministic rule-based extraction is the default. External provider calls require both `ENABLE_PROVIDER_MODE=true` and a supported provider key; a key alone must not activate them.
5. Provider output is bounded, schema-validated, de-duplicated and never executed. Invalid output or provider failure falls back to deterministic results with a generic warning.
6. API keys are never committed — see `.env.example` and `.gitignore`.
7. Dataset frequency is not presented as representative market demand, and entered-skill comparison is not presented as candidate capability, ATS scoring or hiring probability.
