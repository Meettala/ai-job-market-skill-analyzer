"""Current end-to-end integration evidence for the deterministic pipeline."""

from __future__ import annotations

import json

from src.analyzer.db import get_connection, insert_skills, posting_count
from src.analyzer.pipeline import run_pipeline


def _posting(number: int, text: str) -> dict[str, str]:
    return {
        "title": f"Synthetic role {number}",
        "company": f"Synthetic Company {number}",
        "location": "Remote",
        "seniority": "Junior",
        "source_url": f"https://example-demo-data.local/integration/{number}",
        "retrieved_at": "2026-09-05",
        "raw_text": text,
    }


def test_end_to_end_pipeline_is_deterministic_and_dataset_scoped(tmp_path, monkeypatch):
    monkeypatch.setenv("ENABLE_PROVIDER_MODE", "false")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    postings = [
        _posting(1, "Python Python and SQL with Docker"),
        _posting(2, "Python and Kubernetes"),
        _posting(3, "PostgreSQL and Docker"),
    ]
    postings_path = tmp_path / "postings.json"
    postings_path.write_text(json.dumps(postings), encoding="utf-8")

    first_db = tmp_path / "first.db"
    first_export = tmp_path / "first.json"
    first = run_pipeline(
        postings_path=postings_path,
        db_path=first_db,
        export_path=first_export,
        candidate_skills=["Python", "SQL"],
    )

    second = run_pipeline(
        postings_path=postings_path,
        db_path=tmp_path / "second.db",
        export_path=tmp_path / "second.json",
        candidate_skills=["Python", "SQL"],
    )

    assert first["postings_analyzed"] == 3
    assert first["skill_frequency"] == second["skill_frequency"]
    assert first["skill_cooccurrence"] == second["skill_cooccurrence"]
    assert first["gap_report"] == second["gap_report"]
    assert json.loads(first_export.read_text(encoding="utf-8")) == first
    assert "not representative labour-market demand" in first["scope_note"]

    conn = get_connection(first_db)
    try:
        assert posting_count(conn) == 3
        python_row = next(row for row in first["skill_frequency"] if row["skill"] == "Python")
        sql_row = next(row for row in first["skill_frequency"] if row["skill"] == "SQL")
        assert python_row["postings_mentioning"] == 2
        assert python_row["pct_of_postings"] == 66.7
        assert sql_row["postings_mentioning"] == 2
        assert sql_row["pct_of_postings"] == 66.7

        first_posting_id = conn.execute("SELECT MIN(id) FROM postings").fetchone()[0]
        before = conn.execute(
            "SELECT COUNT(*) FROM posting_skills WHERE posting_id = ? AND skill = ?",
            (first_posting_id, "Python"),
        ).fetchone()[0]
        insert_skills(
            conn,
            first_posting_id,
            [
                {"skill": "Python", "category": "Programming"},
                {"skill": "Python", "category": "Programming"},
            ],
        )
        after = conn.execute(
            "SELECT COUNT(*) FROM posting_skills WHERE posting_id = ? AND skill = ?",
            (first_posting_id, "Python"),
        ).fetchone()[0]
        assert before == after == 1
    finally:
        conn.close()

    first_db.unlink()
