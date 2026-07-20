# Safety rules — AI Job Market Skill Analyzer

1. No scraping of job platforms whose terms disallow it. This MVP uses
   synthetic sample data (see `data/generate_sample_postings.py`) instead
   of live scraping. Real data sources are only added via approved,
   permitted means (a licensed dataset, or an approved search API later).
2. Every posting stored keeps its `source_url` and `retrieved_at` date, so
   provenance is always visible — even for demo data, which is clearly
   labeled as synthetic wherever it's shown (dashboard footer, README,
   pipeline output).
3. LLM-assisted extraction treats posting text as untrusted input: the
   text is delimited and the model is explicitly instructed not to follow
   instructions found inside it (see `llm_extractor.py`).
4. No LLM key is required for the tool to work. Rule-based extraction is
   the default and only path unless a key is explicitly configured.
5. API keys are never committed — see `.env.example` and `.gitignore`.
