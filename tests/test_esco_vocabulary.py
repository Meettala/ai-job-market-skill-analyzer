"""Tests for the committed ESCO reference vocabulary."""

from __future__ import annotations

import pytest

import src.analyzer.esco_vocabulary as esco
from src.analyzer.esco_vocabulary import (
    artifact_summary,
    attribution,
    isco_major_group,
    label_index,
    load_vocabulary,
    lookup_label,
    normalize_label,
    scope_note,
)

EXPECTED_SUMMARY = {
    "occupations": 2909,
    "skills": 12549,
    "essential_skill_links": 59509,
    "skill_alternative_labels": 78713,
    "occupation_alternative_labels": 29722,
    "isco_major_groups": 10,
}


def test_committed_artifact_structure_and_documented_counts():
    vocabulary = load_vocabulary()
    assert vocabulary["attribution"].strip()
    assert vocabulary["scopeNote"].strip()
    summary = artifact_summary()
    for key, expected in EXPECTED_SUMMARY.items():
        assert summary[key] == expected
    assert vocabulary["counts"]["occupations"] == EXPECTED_SUMMARY["occupations"]
    assert vocabulary["counts"]["skills"] == EXPECTED_SUMMARY["skills"]
    assert vocabulary["counts"]["iscoMajorGroups"] == 10


def test_covers_all_ten_isco_major_groups():
    vocabulary = load_vocabulary()
    groups = {o["iscoPath"][0] for o in vocabulary["occupations"].values() if o["iscoPath"]}
    assert len(groups) == 10


def test_uri_key_invariants_have_no_duplicates():
    vocabulary = load_vocabulary()
    for collection_name in ("occupations", "skills"):
        concepts = vocabulary[collection_name]
        uris = [concept["uri"] for concept in concepts.values()]
        assert len(uris) == len(set(uris))
        assert all(key == concept["uri"] for key, concept in concepts.items())


def test_includes_non_technical_occupations_as_reference_data():
    labels = {o["preferredLabel"] for o in load_vocabulary()["occupations"].values()}
    for occupation in ("plumber", "chef", "hairdresser", "midwife"):
        assert occupation in labels, f"{occupation} missing from vocabulary"


def test_attribution_and_scope_note_are_available_for_display():
    assert "ESCO" in attribution()
    assert "CC BY 4.0" in attribution()
    assert scope_note().strip()


def test_lookup_label_preserves_ambiguous_concepts():
    ambiguous = next((item for item in label_index().items() if len(item[1]) > 1), None)
    assert ambiguous is not None
    label, uris = ambiguous
    assert lookup_label(label) == uris
    assert len(uris) > 1


def test_synonyms_resolve_to_concepts():
    assert len(label_index()) > 50_000
    assert lookup_label("gas fitter")
    assert lookup_label("Gas Fitter") == lookup_label("gas fitter")


def test_normalize_label_strips_parentheticals_and_case():
    assert normalize_label("Python (computer programming)") == "python"


def test_isco_major_group_resolves():
    vocabulary = load_vocabulary()
    plumber = next(
        o for o in vocabulary["occupations"].values() if o["preferredLabel"] == "plumber"
    )
    assert isco_major_group(plumber["uri"]) == "Craft and related trades workers"


def test_unknown_uri_returns_none():
    assert isco_major_group("http://example.invalid/not-a-real-uri") is None


def test_missing_artifact_failure_is_clear(monkeypatch, tmp_path):
    esco.load_vocabulary.cache_clear()
    esco.label_index.cache_clear()
    monkeypatch.setattr(esco, "ARTEFACT_PATH", tmp_path / "missing-esco.json.gz")
    with pytest.raises(FileNotFoundError, match="ESCO vocabulary artefact not found"):
        esco.load_vocabulary()
    esco.load_vocabulary.cache_clear()
    esco.label_index.cache_clear()
