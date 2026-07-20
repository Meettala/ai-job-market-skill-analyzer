"""
End-to-end pipeline: load postings -> extract skills -> store in SQLite ->
export aggregated results as JSON (used by both the Streamlit app and the
static Next.js dashboard on the portfolio site).

Usage:
    python -m src.analyzer.pipeline
"""

from __future__ import annotations

import json
from pathlib import Path

from .db import get_connection, insert_posting, insert_skills
from .extractor import extract_skills
from .report import gap_report, skill_cooccurrence, skill_frequency

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "data" / "postings.db"
POSTINGS_PATH = ROOT / "data" / "sample_postings.json"
EXPORT_PATH = ROOT / "exports" / "analysis.json"

# Example candidate profile — swap for a real one when wiring this up to
# JobPilot AI's evidence bank later.
SAMPLE_CANDIDATE_SKILLS = [
    "Python", "Pandas", "SQL", "scikit-learn", "Git", "Statistics", "Data Visualization",
]


def run_pipeline() -> dict:
    if DB_PATH.exists():
        DB_PATH.unlink()  # rebuild fresh each run for a demo-clean state

    conn = get_connection(DB_PATH)
    postings = json.loads(POSTINGS_PATH.read_text())

    for posting in postings:
        posting_id = insert_posting(conn, posting)
        skills = extract_skills(posting["raw_text"])
        insert_skills(conn, posting_id, skills)

    freq = skill_frequency(conn)
    cooc = skill_cooccurrence(conn)
    gaps = gap_report(conn, SAMPLE_CANDIDATE_SKILLS)

    result = {
        "postings_analyzed": len(postings),
        "generated_from": "synthetic sample data (see data/generate_sample_postings.py)",
        "skill_frequency": freq.to_dict("records"),
        "skill_cooccurrence": cooc.to_dict("records"),
        "gap_report": gaps,
        "candidate_skills_used": SAMPLE_CANDIDATE_SKILLS,
    }

    EXPORT_PATH.parent.mkdir(exist_ok=True)
    EXPORT_PATH.write_text(json.dumps(result, indent=2))
    conn.close()
    return result


if __name__ == "__main__":
    result = run_pipeline()
    print(f"Analyzed {result['postings_analyzed']} postings.")
    print(f"Top 5 skills: {[s['skill'] for s in result['skill_frequency'][:5]]}")
    print(f"Exported to {EXPORT_PATH}")
