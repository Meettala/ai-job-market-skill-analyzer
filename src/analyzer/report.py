"""Deterministic aggregation and candidate gap-report logic."""

from __future__ import annotations

import sqlite3

import pandas as pd

FREQUENCY_COLUMNS = ["skill", "category", "postings_mentioning", "pct_of_postings"]
COOCCURRENCE_COLUMNS = ["skill_a", "skill_b", "co_occurrences"]


def skill_frequency(conn: sqlite3.Connection) -> pd.DataFrame:
    """Return posting frequency and percentage for every extracted skill."""
    total_postings = int(pd.read_sql("SELECT COUNT(*) AS n FROM postings", conn).iloc[0]["n"])
    if total_postings == 0:
        return pd.DataFrame(columns=FREQUENCY_COLUMNS)

    frame = pd.read_sql(
        """
        SELECT skill, category, COUNT(DISTINCT posting_id) AS postings_mentioning
        FROM posting_skills
        GROUP BY skill, category
        ORDER BY postings_mentioning DESC, skill ASC
        """,
        conn,
    )
    frame["pct_of_postings"] = (
        frame["postings_mentioning"] / total_postings * 100
    ).round(1)
    return frame


def skill_cooccurrence(conn: sqlite3.Connection, top_n: int = 15) -> pd.DataFrame:
    """Return the most frequent distinct skill pairs per posting."""
    if top_n <= 0:
        return pd.DataFrame(columns=COOCCURRENCE_COLUMNS)

    frame = pd.read_sql("SELECT posting_id, skill FROM posting_skills", conn)
    pairs: dict[tuple[str, str], int] = {}
    for _, group in frame.groupby("posting_id"):
        skills = sorted(set(group["skill"].dropna()))
        for index, skill_a in enumerate(skills):
            for skill_b in skills[index + 1 :]:
                key = (skill_a, skill_b)
                pairs[key] = pairs.get(key, 0) + 1

    rows = [
        {"skill_a": skill_a, "skill_b": skill_b, "co_occurrences": count}
        for (skill_a, skill_b), count in pairs.items()
    ]
    if not rows:
        return pd.DataFrame(columns=COOCCURRENCE_COLUMNS)

    return (
        pd.DataFrame(rows)
        .sort_values(["co_occurrences", "skill_a", "skill_b"], ascending=[False, True, True])
        .head(top_n)
        .reset_index(drop=True)
    )


def gap_report(
    conn: sqlite3.Connection,
    candidate_skills: list[str],
    min_pct: float = 15.0,
) -> dict[str, object]:
    """Compare candidate skills with evidence-backed market frequency."""
    threshold = min(max(float(min_pct), 0.0), 100.0)
    frequency = skill_frequency(conn)
    candidate_set = {
        skill.strip().casefold()
        for skill in candidate_skills
        if isinstance(skill, str) and skill.strip()
    }

    if frequency.empty:
        return {"matched_skills": [], "missing_skills": [], "match_rate_pct": 0.0}

    frequency["candidate_has"] = frequency["skill"].str.casefold().isin(candidate_set)
    relevant = frequency[frequency["pct_of_postings"] >= threshold]
    matched = relevant[relevant["candidate_has"]].sort_values(
        ["postings_mentioning", "skill"], ascending=[False, True]
    )
    missing = relevant[~relevant["candidate_has"]].sort_values(
        ["postings_mentioning", "skill"], ascending=[False, True]
    )

    denominator = len(relevant)
    match_rate = round(100 * len(matched) / denominator, 1) if denominator else 0.0
    columns = ["skill", "category", "pct_of_postings"]
    return {
        "matched_skills": matched[columns].to_dict("records"),
        "missing_skills": missing[columns].to_dict("records"),
        "match_rate_pct": match_rate,
    }
