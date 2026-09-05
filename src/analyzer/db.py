"""SQLite storage for job postings and extracted skills."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

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
    posting_id INTEGER NOT NULL REFERENCES postings(id) ON DELETE CASCADE,
    skill TEXT NOT NULL,
    category TEXT,
    requirement_level TEXT NOT NULL DEFAULT 'unspecified'
        CHECK (requirement_level IN ('required', 'preferred', 'unspecified')),
    method TEXT NOT NULL DEFAULT 'rule_based'
        CHECK (method IN ('rule_based', 'llm')),
    UNIQUE(posting_id, skill)
);
"""


def get_connection(db_path: str | Path) -> sqlite3.Connection:
    """Open a configured SQLite connection and ensure the schema exists."""
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    return conn


def posting_count(conn: sqlite3.Connection) -> int:
    """Return the true number of stored postings."""
    row = conn.execute("SELECT COUNT(*) FROM postings").fetchone()
    return int(row[0]) if row else 0


def insert_posting(conn: sqlite3.Connection, posting: dict[str, Any]) -> int:
    """Validate and insert one posting using parameterised SQL."""
    title = _required_text(posting.get("title"), "title")
    raw_text = _required_text(posting.get("raw_text"), "raw_text")
    cursor = conn.execute(
        """INSERT INTO postings
           (title, company, location, seniority, source_url, retrieved_at, raw_text)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            title,
            _optional_text(posting.get("company")),
            _optional_text(posting.get("location")),
            _optional_text(posting.get("seniority")),
            _optional_text(posting.get("source_url")),
            _optional_text(posting.get("retrieved_at")),
            raw_text,
        ),
    )
    conn.commit()
    if cursor.lastrowid is None:
        raise RuntimeError("SQLite did not return a posting identifier")
    return int(cursor.lastrowid)


def insert_skills(
    conn: sqlite3.Connection,
    posting_id: int,
    skills: list[dict[str, Any]],
) -> None:
    """Insert validated, de-duplicated skills for a known posting."""
    rows: list[tuple[int, str, str | None, str, str]] = []
    seen: set[str] = set()
    for skill in skills:
        name = _required_text(skill.get("skill"), "skill")
        key = name.casefold()
        if key in seen:
            continue
        seen.add(key)

        requirement = skill.get("requirement_level", "unspecified")
        method = skill.get("method", "rule_based")
        if requirement not in {"required", "preferred", "unspecified"}:
            raise ValueError("Unsupported requirement level")
        if method not in {"rule_based", "llm"}:
            raise ValueError("Unsupported extraction method")

        rows.append(
            (
                posting_id,
                name,
                _optional_text(skill.get("category")),
                requirement,
                method,
            )
        )

    conn.executemany(
        """INSERT OR IGNORE INTO posting_skills
           (posting_id, skill, category, requirement_level, method)
           VALUES (?, ?, ?, ?, ?)""",
        rows,
    )
    conn.commit()


def _required_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def _optional_text(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("Optional text fields must be strings or null")
    normalized = value.strip()
    return normalized or None
