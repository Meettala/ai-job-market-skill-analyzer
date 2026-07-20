"""
Generates data/sample_postings.json — a SYNTHETIC set of AI/ML job
postings for demo purposes only.

Why synthetic: the MVP safety rules (see docs/security/safety-rules.md)
rule out scraping platforms whose terms disallow it, and no approved
search API is wired up yet (that's Version 2 in the roadmap). So this
demo ships with realistic, hand-composed postings rather than real
scraped listings, clearly labeled as such everywhere they're shown.

To use real data instead: replace data/sample_postings.json with postings
from a permitted source (e.g. a public dataset you're licensed to use, or
your own approved API integration later) in the same shape, and everything
downstream (extraction, storage, dashboard) works unchanged.
"""

import json
import random
from pathlib import Path

random.seed(7)

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

def build_posting(i: int) -> dict:
    title = random.choice(TITLES)
    company = random.choice(COMPANIES)
    location = random.choice(LOCATIONS)
    seniority = random.choice(SENIORITIES)
    body_snippets = random.sample(SNIPPETS, k=random.randint(5, 8))
    raw_text = INTRO.format(title=title, company=company, seniority=seniority, location=location)
    raw_text += " " + " ".join(body_snippets)
    return {
        "title": title,
        "company": company,
        "location": location,
        "seniority": seniority,
        "source_url": f"https://example-demo-data.local/postings/{i}",
        "retrieved_at": "2026-07-01",
        "raw_text": raw_text,
    }

def main():
    postings = [build_posting(i) for i in range(1, 41)]
    out_path = Path(__file__).parent / "sample_postings.json"
    out_path.write_text(json.dumps(postings, indent=2))
    print(f"Wrote {len(postings)} synthetic postings to {out_path}")

if __name__ == "__main__":
    main()
