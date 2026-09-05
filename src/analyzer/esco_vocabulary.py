"""Reference loader and lookup utilities for the bundled ESCO vocabulary.

The compressed artefact in ``data/esco-vocabulary.json.gz`` is a broad ESCO
reference vocabulary covering occupations and skills across all ten ISCO-08
major groups. It is useful for exact label lookup, attribution and future
mapping work.

It does *not* replace the active deterministic extractor. The default no-key
extraction path in ``extractor.py`` still uses the curated AI/ML taxonomy in
``taxonomy.py``. JR04 keeps that distinction explicit rather than adding an
unbounded matcher across the full ESCO vocabulary.

Licensing: the artefact has its own attribution/licensing boundary separate
from the repository's MIT-licensed source code. See ATTRIBUTION.md.
"""

from __future__ import annotations

import gzip
import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

ARTEFACT_PATH = Path(__file__).resolve().parents[2] / "data" / "esco-vocabulary.json.gz"

_REQUIRED_TOP_LEVEL_FIELDS = {
    "source",
    "sourceUrl",
    "licence",
    "attribution",
    "generatedBy",
    "method",
    "scopeNote",
    "counts",
    "occupations",
    "skills",
}

_NON_LABEL_CHARS = re.compile(r"[^a-z0-9+.#/ -]")
_PARENTHETICAL = re.compile(r"\([^)]*\)")
_WHITESPACE = re.compile(r"\s+")


@lru_cache(maxsize=1)
def load_vocabulary() -> dict[str, Any]:
    """Load, validate and memoise the committed ESCO artefact."""
    if not ARTEFACT_PATH.exists():
        raise FileNotFoundError(
            f"ESCO vocabulary artefact not found at {ARTEFACT_PATH}. "
            "Regenerate it with tools/build_esco_vocabulary.py."
        )
    with gzip.open(ARTEFACT_PATH, "rt", encoding="utf-8") as handle:
        vocabulary: Any = json.load(handle)
    validate_vocabulary(vocabulary)
    return vocabulary


def validate_vocabulary(vocabulary: Any) -> None:
    """Validate structural invariants used by the repository."""
    if not isinstance(vocabulary, dict):
        raise ValueError("ESCO vocabulary must be a JSON object")

    missing = _REQUIRED_TOP_LEVEL_FIELDS - set(vocabulary)
    if missing:
        raise ValueError(f"ESCO vocabulary missing required fields: {sorted(missing)}")

    attribution_text = vocabulary["attribution"]
    scope_text = vocabulary["scopeNote"]
    if not isinstance(attribution_text, str) or not attribution_text.strip():
        raise ValueError("ESCO vocabulary attribution must be a non-empty string")
    if not isinstance(scope_text, str) or not scope_text.strip():
        raise ValueError("ESCO vocabulary scope note must be a non-empty string")

    occupations = vocabulary["occupations"]
    skills = vocabulary["skills"]
    counts = vocabulary["counts"]
    if not isinstance(occupations, dict) or not isinstance(skills, dict):
        raise ValueError("ESCO occupations and skills must be JSON objects keyed by URI")
    if not isinstance(counts, dict):
        raise ValueError("ESCO counts must be a JSON object")

    _validate_uri_mapping("occupation", occupations)
    _validate_uri_mapping("skill", skills)

    groups = {o["iscoPath"][0] for o in occupations.values() if o.get("iscoPath")}
    expected_counts = {
        "occupations": len(occupations),
        "skills": len(skills),
        "iscoMajorGroups": len(groups),
    }
    for key, actual in expected_counts.items():
        if counts.get(key) != actual:
            raise ValueError(
                f"ESCO counts.{key}={counts.get(key)!r} does not match committed data {actual}"
            )


def _validate_uri_mapping(label: str, concepts: dict[str, Any]) -> None:
    uris: list[str] = []
    for key, concept in concepts.items():
        if not isinstance(key, str) or not isinstance(concept, dict):
            raise ValueError(f"ESCO {label} entries must be URI-keyed objects")
        uri = concept.get("uri")
        if uri != key:
            raise ValueError(f"ESCO {label} key does not match its uri field: {key}")
        uris.append(uri)
    if len(uris) != len(set(uris)):
        raise ValueError(f"ESCO {label} concept URIs must be unique")


def artifact_summary() -> dict[str, int]:
    """Return reproducible counts derived from the committed artefact itself."""
    vocabulary = load_vocabulary()
    occupations = vocabulary["occupations"]
    skills = vocabulary["skills"]
    groups = {o["iscoPath"][0] for o in occupations.values() if o.get("iscoPath")}
    return {
        "occupations": len(occupations),
        "skills": len(skills),
        "essential_skill_links": sum(
            len(o.get("essentialSkills", [])) for o in occupations.values()
        ),
        "skill_alternative_labels": sum(
            len(s.get("alternativeLabels", [])) for s in skills.values()
        ),
        "occupation_alternative_labels": sum(
            len(o.get("alternativeLabels", [])) for o in occupations.values()
        ),
        "isco_major_groups": len(groups),
        "ambiguous_surface_forms": sum(1 for uris in label_index().values() if len(uris) > 1),
    }


def attribution() -> str:
    """Return the attribution text stored in the artefact."""
    return load_vocabulary()["attribution"]


def scope_note() -> str:
    """Return the scope note stored in the artefact."""
    return load_vocabulary()["scopeNote"]


def normalize_label(label: str) -> str:
    lowered = _PARENTHETICAL.sub(" ", label.lower())
    cleaned = _NON_LABEL_CHARS.sub(" ", lowered)
    return _WHITESPACE.sub(" ", cleaned).strip()


@lru_cache(maxsize=1)
def label_index() -> dict[str, tuple[str, ...]]:
    """Map normalized surface forms to every ESCO concept URI using that form."""
    vocabulary = load_vocabulary()
    index: dict[str, list[str]] = {}

    def add(label: str, uri: str) -> None:
        key = normalize_label(label)
        if len(key) < 2:
            return
        bucket = index.setdefault(key, [])
        if uri not in bucket:
            bucket.append(uri)

    for concept in vocabulary["skills"].values():
        add(concept["preferredLabel"], concept["uri"])
        for alternative in concept["alternativeLabels"]:
            add(alternative, concept["uri"])

    for occupation in vocabulary["occupations"].values():
        add(occupation["preferredLabel"], occupation["uri"])
        for alternative in occupation["alternativeLabels"]:
            add(alternative, occupation["uri"])

    return {key: tuple(value) for key, value in index.items()}


def lookup_label(label: str) -> tuple[str, ...]:
    """Exact surface-form lookup. Returns every concept using that form."""
    return label_index().get(normalize_label(label), ())


def isco_major_group(occupation_uri: str) -> str | None:
    """Return the top-level ISCO group for one occupation URI."""
    occupation = load_vocabulary()["occupations"].get(occupation_uri)
    if not occupation or not occupation["iscoPath"]:
        return None
    return occupation["iscoPath"][0]


def skill_label(skill_uri: str) -> str | None:
    skill = load_vocabulary()["skills"].get(skill_uri)
    return skill["preferredLabel"] if skill else None
