"""
SQLite storage for job postings and extracted skills.

Kept intentionally simple (two tables) so schema, query, and aggregation
logic are all easy to read in a portfolio review.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS postings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    company TEXT,
    location TEXT,
    seniority TEXT,
    source_url TEXT,
    retrieved_at TEXT,
    raw_text TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS posting_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    posting_id INTEGER NOT NULL REFERENCES postings(id),
    skill TEXT NOT NULL,
    category TEXT,
    requirement_level TEXT DEFAULT 'unspecified', -- required | preferred | unspecified
    method TEXT DEFAULT 'rule_based'               -- rule_based | llm
);
"""


def get_connection(db_path: str | Path) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA)
    return conn


def insert_posting(conn: sqlite3.Connection, posting: dict) -> int:
    cur = conn.execute(
        """INSERT INTO postings (title, company, location, seniority, source_url, retrieved_at, raw_text)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            posting["title"],
            posting.get("company"),
            posting.get("location"),
            posting.get("seniority"),
            posting.get("source_url"),
            posting.get("retrieved_at"),
            posting["raw_text"],
        ),
    )
    conn.commit()
    return cur.lastrowid


def insert_skills(conn: sqlite3.Connection, posting_id: int, skills: list[dict]) -> None:
    conn.executemany(
        """INSERT INTO posting_skills (posting_id, skill, category, requirement_level, method)
           VALUES (?, ?, ?, ?, ?)""",
        [
            (
                posting_id,
                s["skill"],
                s.get("category"),
                s.get("requirement_level", "unspecified"),
                s.get("method", "rule_based"),
            )
            for s in skills
        ],
    )
    conn.commit()
