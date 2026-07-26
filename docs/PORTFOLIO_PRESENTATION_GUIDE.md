# Portfolio Presentation Guide

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m src.analyzer.pipeline
streamlit run streamlit_app/app.py
```

Open `http://localhost:8501`.

## Screenshot checklist

Capture one clean desktop screenshot showing:

- the project title and synthetic-data statement;
- extraction mode;
- demand metrics and skill chart;
- candidate gap report;
- no browser bookmarks, personal tabs, API keys or terminal secrets.

Save the real image as `docs/assets/app-screenshot.png` and add it to the README only after verifying that it contains no private data.

## Demo video

Record a 30–60 second walkthrough:

1. Explain that the public sample is synthetic.
2. Show the demand chart and category filter.
3. Change the candidate skill list.
4. Show matched and missing skills.
5. Mention deterministic no-key mode, validated optional provider extraction and CI.

## GitHub social preview

Convert `docs/assets/social-preview.svg` to a 1280×640 PNG. In GitHub, open **Settings → General → Social preview → Edit**, then upload the PNG.

## Suggested repository description

> Safety-first Python and Streamlit analyser for synthetic AI job postings, skill demand and evidence-backed candidate gap reports.

Suggested topics: `python`, `streamlit`, `pandas`, `sqlite`, `llm`, `job-market`, `data-analysis`, `portfolio`.

## CV wording

> Built a safety-first AI job market skill analyser using Python, pandas, SQLite and Streamlit; implemented deterministic and validated optional LLM extraction, evidence-backed gap reporting, multi-version tests, CI, dependency auditing and Docker deployment.

## Interview explanation

Describe the project as a reproducible analysis pipeline, not a live-market claim. Emphasise the synthetic-data boundary, parameterised SQL, deterministic reporting, strict provider validation, safe fallback and transparent limitations.

## Instructions for another AI

Read `AI_HANDOFF.md`, verify the live branch and CI, then help capture real presentation media. Never fabricate screenshots, benchmark results, recruiter outcomes or real-market coverage.
