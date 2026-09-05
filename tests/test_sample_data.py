"""Synthetic sample provenance and reproducibility checks."""

from __future__ import annotations

import json
from pathlib import Path

from data.generate_sample_postings import (
    COMPANIES,
    SAMPLE_COUNT,
    SYNTHETIC_SOURCE_PREFIX,
    render_postings,
)

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_PATH = ROOT / "data" / "sample_postings.json"


def test_committed_sample_is_non_empty_schema_valid_and_synthetic():
    postings = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
    assert isinstance(postings, list)
    assert len(postings) == SAMPLE_COUNT
    assert postings

    required = {
        "title",
        "company",
        "location",
        "seniority",
        "source_url",
        "retrieved_at",
        "raw_text",
    }
    for posting in postings:
        assert set(posting) == required
        assert posting["title"].strip()
        assert posting["raw_text"].strip()
        assert posting["company"] in COMPANIES
        assert posting["source_url"].startswith(SYNTHETIC_SOURCE_PREFIX)
        assert posting["retrieved_at"] == "2026-07-01"


def test_committed_sample_is_byte_for_byte_reproducible():
    assert SAMPLE_PATH.read_text(encoding="utf-8") == render_postings()
