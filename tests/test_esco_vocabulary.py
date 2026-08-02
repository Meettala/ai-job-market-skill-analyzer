"""Tests for the shared ESCO vocabulary loader."""

from src.analyzer.esco_vocabulary import (
    attribution,
    isco_major_group,
    label_index,
    load_vocabulary,
    lookup_label,
    normalize_label,
)


def test_covers_every_field_not_just_ai_ml():
    vocabulary = load_vocabulary()
    assert vocabulary["counts"]["iscoMajorGroups"] == 10
    assert vocabulary["counts"]["occupations"] > 2500
    groups = {o["iscoPath"][0] for o in vocabulary["occupations"].values() if o["iscoPath"]}
    assert len(groups) == 10


def test_includes_non_technical_occupations():
    labels = {o["preferredLabel"] for o in load_vocabulary()["occupations"].values()}
    for occupation in ("plumber", "chef", "hairdresser", "midwife"):
        assert occupation in labels, f"{occupation} missing from vocabulary"


def test_attribution_is_available_for_display():
    text = attribution()
    assert "ESCO" in text
    assert "CC BY 4.0" in text


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
