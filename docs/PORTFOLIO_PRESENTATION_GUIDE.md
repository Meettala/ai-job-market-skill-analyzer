# Portfolio Presentation Guide

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python data/generate_sample_postings.py --check
ENABLE_PROVIDER_MODE=false python -m src.analyzer.pipeline
streamlit run streamlit_app/app.py
```

Open `http://localhost:8501`.

## Screenshot checklist

Capture one clean desktop screenshot showing:

- the project title and synthetic/non-representative data statement;
- deterministic extraction mode;
- the true synthetic posting count;
- the “Most frequent skills in this sample” chart/table;
- the entered-skill comparison wording;
- no browser bookmarks, personal tabs, API keys, terminal secrets or private data.

Save a real image as `docs/assets/app-screenshot.png` and add it to the README only after verifying that it contains no private information. Do not reconstruct or fabricate a screenshot.

## Demo video

Record a 30–60 second walkthrough:

1. Explain that the public sample contains deterministic synthetic AI/ML postings and is not representative market data.
2. Show the posting count and sample-scoped frequency chart.
3. Change the entered skill list.
4. Explain that “not present in entered skills” is not proof of a capability gap.
5. Mention parameterised SQLite, duplicate protection, explicit default-off provider mode, CI and Docker verification.
6. If discussing ESCO, describe it as a validated reference/lookup artefact rather than the active extractor.

## GitHub social preview

Convert `docs/assets/social-preview.svg` to a 1280×640 PNG. In GitHub, open **Settings → General → Social preview → Edit**, then upload the PNG.

## Suggested repository description

> Python/SQLite skill-analysis pipeline for synthetic job-posting data with deterministic extraction, Streamlit reporting and safe optional LLM parsing.

Suggested topics: `python`, `pandas`, `sqlite`, `streamlit`, `data-analysis`, `job-market`, `esco`, `data-pipeline`. Add `llm` only while optional provider extraction remains a meaningful documented feature.

## CV wording direction

Use measured repository evidence, for example: Python/SQLite pipeline design, deterministic aggregation, synthetic-data governance, ESCO artefact validation, multi-version tests, dependency auditing and non-root Docker verification. Do not describe the sample as real market demand or the entered-skill comparison as a capability/hiring score.

## Interview explanation

Describe the project as a reproducible dataset-analysis pipeline, not a live-market product. Emphasise denominator correctness, parameterised SQLite writes, duplicate protection, deterministic taxonomy extraction, the ESCO reference-versus-active-extractor distinction, explicit optional-provider privacy boundaries and transparent limitations.

## Instructions for another AI

Read `AI_HANDOFF.md`, verify the live branch and exact-head CI, then help capture real presentation media. Never fabricate screenshots, benchmark results, recruiter outcomes, deployment status or representative market claims.
