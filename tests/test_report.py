import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.analyzer.db import get_connection, insert_posting, insert_skills
from src.analyzer.report import gap_report, skill_frequency


def _seed(conn):
    pid1 = insert_posting(conn, {"title": "A", "raw_text": "x"})
    insert_skills(conn, pid1, [
        {"skill": "Python", "category": "Programming"},
        {"skill": "SQL", "category": "Programming"},
    ])
    pid2 = insert_posting(conn, {"title": "B", "raw_text": "y"})
    insert_skills(conn, pid2, [{"skill": "Python", "category": "Programming"}])


def test_skill_frequency(tmp_path):
    conn = get_connection(tmp_path / "t.db")
    _seed(conn)
    freq = skill_frequency(conn)
    python_row = freq[freq["skill"] == "Python"].iloc[0]
    assert python_row["postings_mentioning"] == 2
    assert python_row["pct_of_postings"] == 100.0


def test_gap_report_matches_and_misses(tmp_path):
    conn = get_connection(tmp_path / "t.db")
    _seed(conn)
    result = gap_report(conn, candidate_skills=["Python"], min_pct=0)
    matched = {s["skill"] for s in result["matched_skills"]}
    missing = {s["skill"] for s in result["missing_skills"]}
    assert "Python" in matched
    assert "SQL" in missing
