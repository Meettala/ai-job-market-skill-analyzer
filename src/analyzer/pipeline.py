"""End-to-end synthetic-data analysis pipeline."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .db import get_connection, insert_posting, insert_skills, posting_count
from .extractor import extract_skills
from .report import gap_report, skill_cooccurrence, skill_frequency

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "data" / "postings.db"
POSTINGS_PATH = ROOT / "data" / "sample_postings.json"
EXPORT_PATH = ROOT / "exports" / "analysis.json"

SAMPLE_CANDIDATE_SKILLS = [
    "Python",
    "Pandas",
    "SQL",
    "scikit-learn",
    "Git",
    "Statistics",
    "Data Visualization",
]


def run_pipeline(
    postings_path: str | Path = POSTINGS_PATH,
    db_path: str | Path = DB_PATH,
    export_path: str | Path = EXPORT_PATH,
    candidate_skills: list[str] | None = None,
) -> dict[str, Any]:
    """Analyse permitted postings and export a deterministic dataset-scoped report."""
    postings_file = Path(postings_path)
    database_file = Path(db_path)
    output_file = Path(export_path)

    postings = _load_postings(postings_file)
    if database_file.exists():
        database_file.unlink()

    conn = get_connection(database_file)
    try:
        for posting in postings:
            posting_id = insert_posting(conn, posting)
            insert_skills(conn, posting_id, extract_skills(posting["raw_text"]))

        stored_postings = posting_count(conn)
        frequency = skill_frequency(conn)
        cooccurrence = skill_cooccurrence(conn)
        gaps = gap_report(conn, candidate_skills or SAMPLE_CANDIDATE_SKILLS)
    finally:
        conn.close()

    if stored_postings != len(postings):
        raise RuntimeError("Stored posting count does not match validated input count")

    result: dict[str, Any] = {
        "postings_analyzed": stored_postings,
        "generated_from": "synthetic sample data (see data/generate_sample_postings.py)",
        "scope_note": (
            "Statistics describe only the analysed dataset; they are not representative "
            "labour-market demand, hiring probability or an ATS score."
        ),
        "skill_frequency": frequency.to_dict("records"),
        "skill_cooccurrence": cooccurrence.to_dict("records"),
        "gap_report": gaps,
        "candidate_skills_used": candidate_skills or SAMPLE_CANDIDATE_SKILLS,
    }

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def _load_postings(path: Path) -> list[dict[str, Any]]:
    try:
        value: Any = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("Posting data could not be loaded") from exc

    if not isinstance(value, list) or not value:
        raise ValueError("Posting data must be a non-empty JSON array")
    if not all(isinstance(item, dict) for item in value):
        raise ValueError("Every posting must be a JSON object")
    return value


if __name__ == "__main__":
    analysis = run_pipeline()
    print(f"Analyzed {analysis['postings_analyzed']} postings.")
    print(f"Top 5 skills: {[item['skill'] for item in analysis['skill_frequency'][:5]]}")
    print(f"Exported to {EXPORT_PATH}")
