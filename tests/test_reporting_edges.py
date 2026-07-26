import sqlite3

import pytest

from src.analyzer.db import get_connection, insert_posting, insert_skills
from src.analyzer.report import gap_report, skill_cooccurrence, skill_frequency


def make_connection(tmp_path):
    return get_connection(tmp_path / "test.db")


def test_empty_reporting_is_safe(tmp_path):
    conn = make_connection(tmp_path)
    try:
        assert skill_frequency(conn).empty
        assert skill_cooccurrence(conn).empty
        assert gap_report(conn, ["Python"]) == {
            "matched_skills": [],
            "missing_skills": [],
            "match_rate_pct": 0.0,
        }
    finally:
        conn.close()


def test_duplicate_skills_are_ignored_per_posting(tmp_path):
    conn = make_connection(tmp_path)
    try:
        posting_id = insert_posting(
            conn,
            {"title": "AI Engineer", "raw_text": "Python Python"},
        )
        insert_skills(
            conn,
            posting_id,
            [
                {"skill": "Python", "category": "Programming"},
                {"skill": "Python", "category": "Programming"},
            ],
        )
        count = conn.execute("SELECT COUNT(*) FROM posting_skills").fetchone()[0]
        assert count == 1
    finally:
        conn.close()


def test_foreign_keys_are_enforced(tmp_path):
    conn = make_connection(tmp_path)
    try:
        with pytest.raises(sqlite3.IntegrityError):
            insert_skills(conn, 999, [{"skill": "Python", "category": "Programming"}])
    finally:
        conn.close()


def test_gap_report_uses_market_threshold(tmp_path):
    conn = make_connection(tmp_path)
    try:
        first = insert_posting(conn, {"title": "Role 1", "raw_text": "Python SQL"})
        second = insert_posting(conn, {"title": "Role 2", "raw_text": "Python"})
        insert_skills(
            conn,
            first,
            [
                {"skill": "Python", "category": "Programming"},
                {"skill": "SQL", "category": "Data"},
            ],
        )
        insert_skills(
            conn,
            second,
            [{"skill": "Python", "category": "Programming"}],
        )

        report = gap_report(conn, [" python "], min_pct=60)
        assert [item["skill"] for item in report["matched_skills"]] == ["Python"]
        assert report["missing_skills"] == []
        assert report["match_rate_pct"] == 100.0
    finally:
        conn.close()


def test_cooccurrence_handles_single_skill_postings(tmp_path):
    conn = make_connection(tmp_path)
    try:
        posting_id = insert_posting(conn, {"title": "Role", "raw_text": "Python"})
        insert_skills(conn, posting_id, [{"skill": "Python", "category": "Programming"}])
        assert skill_cooccurrence(conn).empty
    finally:
        conn.close()
