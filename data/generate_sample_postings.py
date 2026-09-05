"""
Generate ``data/sample_postings.json`` — a SYNTHETIC AI/ML posting sample.

The public sample is hand-composed and synthetic. It is intentionally not a
real-time or representative labour-market dataset and contains no scraped job
board content.

Regenerate the committed file:
    python data/generate_sample_postings.py

Verify byte-for-byte reproducibility without rewriting it:
    python data/generate_sample_postings.py --check
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

SEED = 7
SAMPLE_COUNT = 40
SYNTHETIC_SOURCE_PREFIX = "https://example-demo-data.local/postings/"

TITLES = [
    "Junior Machine Learning Engineer",
    "AI Engineer",
    "Data Scientist, AI/ML",
    "Applied Scientist",
    "ML Engineer",
    "NLP Engineer",
    "Data Scientist",
    "AI/ML Software Engineer",
    "Machine Learning Engineer, LLM Platform",
    "Junior Data Scientist",
    "MLOps Engineer",
    "AI Research Engineer",
]

COMPANIES = [
    "Northwind Analytics", "Bluepeak AI", "Fenwick Data Systems", "Solara Labs",
    "Cascade Intelligence", "Marrow Health AI", "Ledgerline Fintech", "Pinehall Robotics",
    "Circuit & Sage", "Harborview Software", "Cobalt Insight", "Fieldstone AI",
    "Vantage Point Analytics", "Greywolf Systems", "Amberbrook AI", "Delta Compute",
    "Nightingale Diagnostics AI", "Rivergate Logistics AI", "Kettlewell Data Co", "Anthos Cloud AI",
]

LOCATIONS = ["London, UK", "Remote (UK)", "Manchester, UK", "Remote (EU)", "Berlin, Germany", "Remote"]

SENIORITIES = ["Junior", "Mid", "Junior-Mid"]

SNIPPETS = [
    "You will build and deploy machine learning models in Python, using pandas and scikit-learn for data preparation and modeling.",
    "Experience with SQL and data warehousing (e.g. Snowflake or BigQuery) required for this role.",
    "We use PyTorch and Hugging Face transformers to build and fine-tune NLP models for production.",
    "This role involves building RAG pipelines using vector databases such as Pinecone or pgvector, and working directly with the OpenAI API and Anthropic API.",
    "Familiarity with prompt engineering and LLM evaluation is a strong plus.",
    "You'll containerize services with Docker and deploy to Kubernetes on AWS (SageMaker experience preferred).",
    "Strong understanding of statistics, A/B testing, and experimentation design expected.",
    "Experience with Airflow or similar orchestration tools for ETL pipelines is preferred.",
    "You will track experiments with MLflow or Weights & Biases and monitor deployed models in production.",
    "Comfortable working with computer vision models and deep learning frameworks like TensorFlow or Keras.",
    "Version control with Git/GitHub and comfort working in an Agile team is expected.",
    "You will build dashboards in Tableau or Power BI to communicate findings to non-technical stakeholders.",
    "Hands-on experience building AI agents with LangChain or similar agent frameworks is a bonus.",
    "Solid grounding in feature engineering, model evaluation, and cross-validation techniques.",
    "Experience with GCP (Vertex AI) or Azure ML is a plus, AWS is required.",
    "You'll write production-grade Python and collaborate cross-functionally with product and engineering.",
    "Exposure to fine-tuning open-source LLMs with LoRA/PEFT is desirable but not required.",
    "CI/CD experience for ML pipelines (testing, deployment automation) is expected.",
]

INTRO = "We're looking for a {title} to join our growing AI team at {company}. This is a {seniority}-level role based in {location}."


def build_posting(i: int, rng: random.Random) -> dict[str, str]:
    title = rng.choice(TITLES)
    company = rng.choice(COMPANIES)
    location = rng.choice(LOCATIONS)
    seniority = rng.choice(SENIORITIES)
    body_snippets = rng.sample(SNIPPETS, k=rng.randint(5, 8))
    raw_text = INTRO.format(title=title, company=company, seniority=seniority, location=location)
    raw_text += " " + " ".join(body_snippets)
    return {
        "title": title,
        "company": company,
        "location": location,
        "seniority": seniority,
        "source_url": f"{SYNTHETIC_SOURCE_PREFIX}{i}",
        "retrieved_at": "2026-07-01",
        "raw_text": raw_text,
    }


def generate_postings(seed: int = SEED, count: int = SAMPLE_COUNT) -> list[dict[str, str]]:
    """Return the deterministic synthetic posting list using a local RNG."""
    rng = random.Random(seed)
    return [build_posting(i, rng) for i in range(1, count + 1)]


def render_postings(seed: int = SEED, count: int = SAMPLE_COUNT) -> str:
    """Return the exact committed JSON representation."""
    return json.dumps(generate_postings(seed=seed, count=count), indent=2)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify the committed sample only")
    args = parser.parse_args()

    out_path = Path(__file__).parent / "sample_postings.json"
    expected = render_postings()

    if args.check:
        if not out_path.exists():
            print(f"Synthetic sample is missing: {out_path}")
            return 1
        if out_path.read_text(encoding="utf-8") != expected:
            print("Synthetic sample differs from deterministic generator output")
            return 1
        print(f"Verified {SAMPLE_COUNT} deterministic synthetic postings in {out_path}")
        return 0

    out_path.write_text(expected, encoding="utf-8")
    print(f"Wrote {SAMPLE_COUNT} synthetic postings to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
