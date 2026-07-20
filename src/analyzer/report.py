"""
Aggregation and gap-report logic. Pure pandas/SQL — no LLM calls here,
so results are always reproducible and explainable.
"""

from __future__ import annotations

import sqlite3

import pandas as pd


def skill_frequency(conn: sqlite3.Connection) -> pd.DataFrame:
    """How many postings mention each skill, and what % of all postings that is."""
    total_postings = pd.read_sql("SELECT COUNT(*) AS n FROM postings", conn).iloc[0]["n"]
    if total_postings == 0:
        return pd.DataFrame(columns=["skill", "category", "postings_mentioning", "pct_of_postings"])

    df = pd.read_sql(
        """
        SELECT skill, category, COUNT(DISTINCT posting_id) AS postings_mentioning
        FROM posting_skills
        GROUP BY skill, category
        ORDER BY postings_mentioning DESC
        """,
        conn,
    )
    df["pct_of_postings"] = (df["postings_mentioning"] / total_postings * 100).round(1)
    return df


def skill_cooccurrence(conn: sqlite3.Connection, top_n: int = 15) -> pd.DataFrame:
    """Which skill pairs most often appear together in the same posting."""
    df = pd.read_sql("SELECT posting_id, skill FROM posting_skills", conn)
    pairs: dict[tuple[str, str], int] = {}
    for _, group in df.groupby("posting_id"):
        skills = sorted(group["skill"].unique())
        for i in range(len(skills)):
            for j in range(i + 1, len(skills)):
                key = (skills[i], skills[j])
                pairs[key] = pairs.get(key, 0) + 1

    rows = [{"skill_a": a, "skill_b": b, "co_occurrences": c} for (a, b), c in pairs.items()]
    result = pd.DataFrame(rows).sort_values("co_occurrences", ascending=False)
    return result.head(top_n).reset_index(drop=True)


def gap_report(conn: sqlite3.Connection, candidate_skills: list[str], min_pct: float = 15.0) -> dict:
    """
    Compare a candidate's skill list against market frequency.

    Returns matched skills (candidate has them, market wants them),
    missing skills (market wants them at >= min_pct of postings, candidate
    doesn't have them), and a market-relevance-ranked action list.
    """
    freq = skill_frequency(conn)
    candidate_set = {s.strip().lower() for s in candidate_skills}
    freq["candidate_has"] = freq["skill"].str.lower().isin(candidate_set)

    matched = freq[freq["candidate_has"]].sort_values("postings_mentioning", ascending=False)
    missing = freq[(~freq["candidate_has"]) & (freq["pct_of_postings"] >= min_pct)].sort_values(
        "postings_mentioning", ascending=False
    )

    return {
        "matched_skills": matched[["skill", "category", "pct_of_postings"]].to_dict("records"),
        "missing_skills": missing[["skill", "category", "pct_of_postings"]].to_dict("records"),
        "match_rate_pct": round(
            100 * len(matched) / max(len(freq[freq["pct_of_postings"] >= min_pct]), 1), 1
        ),
    }
