"""
Shared ESCO vocabulary.

This replaces the hand-written ``SKILL_TAXONOMY``, which held roughly sixty
AI/ML terms grouped into categories like "ML/DL Frameworks" and "LLM / GenAI".
That taxonomy could only describe AI and data roles, which made the analyzer
useless for the labour market as a whole.

The artefact in ``data/esco-vocabulary.json.gz`` covers every field of work:
2,909 occupations across all ten ISCO-08 major groups, 12,549 skills, and the
occupation-to-skill relationships between them. It is byte-identical to the
copy JobPilot AI reads, and the ESCO URI is the join key between the two
applications. Neither imports the other's code.

Licensing: the artefact is CC BY 4.0, not MIT. See ATTRIBUTION.md. The
attribution must remain visible to end users, so ``attribution()`` exists to
be rendered in the interface rather than merely stored on disk.
"""

from __future__ import annotations

import gzip
import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

ARTEFACT_PATH = Path(__file__).resolve().parents[2] / "data" / "esco-vocabulary.json.gz"

_NON_LABEL_CHARS = re.compile(r"[^a-z0-9+.#/ -]")
_PARENTHETICAL = re.compile(r"\([^)]*\)")
_WHITESPACE = re.compile(r"\s+")


@lru_cache(maxsize=1)
def load_vocabulary() -> dict[str, Any]:
    """Load and memoise the artefact. It is about 4 MB compressed."""
    if not ARTEFACT_PATH.exists():
        raise FileNotFoundError(
            f"ESCO vocabulary artefact not found at {ARTEFACT_PATH}. "
            "Regenerate it with tools/build_esco_vocabulary.py."
        )
    with gzip.open(ARTEFACT_PATH, "rt", encoding="utf-8") as handle:
        return json.load(handle)


def attribution() -> str:
    """
    Attribution text that must be shown to users, not merely kept in a file.
    CC BY 4.0 obliges the notice to travel with the data into the product.
    """
    return load_vocabulary()["attribution"]


def scope_note() -> str:
    """Honest statement of what the vocabulary does and does not cover well."""
    return load_vocabulary()["scopeNote"]


def normalize_label(label: str) -> str:
    lowered = _PARENTHETICAL.sub(" ", label.lower())
    cleaned = _NON_LABEL_CHARS.sub(" ", lowered)
    return _WHITESPACE.sub(" ", cleaned).strip()


@lru_cache(maxsize=1)
def label_index() -> dict[str, tuple[str, ...]]:
    """
    Map every normalised surface form onto the concept URIs that use it.

    A surface form can legitimately belong to several concepts, so every match
    is returned rather than one being silently chosen. Disambiguation needs
    surrounding context and is the caller's responsibility.
    """
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
    """
    The top-level ISCO group for an occupation, e.g. "Craft and related trades
    workers". Demand figures are reported per group so that a skill trending in
    one part of the labour market is not presented as trending everywhere.
    """
    occupation = load_vocabulary()["occupations"].get(occupation_uri)
    if not occupation or not occupation["iscoPath"]:
        return None
    return occupation["iscoPath"][0]


def skill_label(skill_uri: str) -> str | None:
    skill = load_vocabulary()["skills"].get(skill_uri)
    return skill["preferredLabel"] if skill else None
