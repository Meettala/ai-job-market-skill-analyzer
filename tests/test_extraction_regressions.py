"""Small labelled regression set for deterministic taxonomy extraction."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.analyzer.extractor import extract_skills_rule_based

CASES_PATH = Path(__file__).parent / "fixtures" / "extraction_regressions.json"
CASES = json.loads(CASES_PATH.read_text(encoding="utf-8"))


@pytest.mark.parametrize("case", CASES, ids=[case["id"] for case in CASES])
def test_deterministic_extraction_regression_set(case):
    actual = sorted(item["skill"] for item in extract_skills_rule_based(case["text"]))
    assert actual == sorted(case["expected_skills"])


def test_regression_set_has_required_scope():
    assert len(CASES) == 9
    assert {case["id"] for case in CASES} == {
        "python",
        "sql-postgresql",
        "scikit-synonym",
        "docker-kubernetes",
        "cloud",
        "rag-llm",
        "visualisation-variant",
        "no-supported-skill",
        "ambiguous-noisy-short-tokens",
    }
