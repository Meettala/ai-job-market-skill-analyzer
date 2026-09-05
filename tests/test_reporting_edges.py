import sqlite3

import pytest

from src.analyzer.db import get_connection, insert_posting, insert_skills, posting_count
from src.analyzer.report import gap_report, skill_cooccurrence, skill_frequency


def make_connection(tmp_path):
    return get_connection(tmp_path / "test.db")


def test_empty_reporting_is_safe(tmp_path):
    conn = make_connection(tmp_path)
    try:
        assert posting_count(conn) == 0
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


def test_posting_count_is_independent_of_most_frequent_skill(tmp_path):
    conn = make_connection(tmp_path)
    try:
        first = insert_posting(conn, {"title": "Role 1", "raw_text": "Python Python"})
        insert_posting(conn, {"title": "Role 2", "raw_text": "No supported skills"})
        third = insert_posting(conn, {"title": "Role 3", "raw_text": "SQL"})
        insert_skills(
            conn,
            first,
            [
                {"skill": "Python", "category": "Programming"},
                {"skill": "Python", "category": "Programming"},
            ],
        )
        insert_skills(conn, third, [{"skill": "SQL", "category": "Programming"}])

        frequency = skill_frequency(conn)
        assert posting_count(conn) == 3
        assert int(frequency["postings_mentioning"].max()) == 1
        python_row = frequency[frequency["skill"] == "Python"].iloc[0]
        assert python_row["postings_mentioning"] == 1
        assert python_row["pct_of_postings"] == 33.3
    finally:
        conn.close()


def test_foreign_keys_are_enforced(tmp_path):
    conn = make_connection(tmp_path)
    try:
        with pytest.raises(sqlite3.IntegrityError):
            insert_skills(conn, 999, [{"skill": "Python", "category": "Programming"}])
    finally:
        conn.close()


def test_gap_report_uses_dataset_threshold_and_literal_entered_skills(tmp_path):
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


def test_gap_report_percentage_denominator_is_recurring_skill_set(tmp_path):
    conn = make_connection(tmp_path)
    try:
        first = insert_posting(conn, {"title": "Role 1", "raw_text": "Python SQL"})
        second = insert_posting(conn, {"title": "Role 2", "raw_text": "Python Docker"})
        insert_skills(
            conn,
            first,
            [
                {"skill": "Python", "category": "Programming"},
                {"skill": "SQL", "category": "Programming"},
            ],
        )
        insert_skills(
            conn,
            second,
            [
                {"skill": "Python", "category": "Programming"},
                {"skill": "Docker", "category": "MLOps"},
            ],
        )

        report = gap_report(conn, ["Python"], min_pct=50)
        assert {item["skill"] for item in report["matched_skills"]} == {"Python"}
        assert {item["skill"] for item in report["missing_skills"]} == {"Docker", "SQL"}
        assert report["match_rate_pct"] == 33.3
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
