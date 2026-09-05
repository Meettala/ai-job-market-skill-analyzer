"""Skill extraction from job posting text."""

from __future__ import annotations

import logging
import re

from .provider_config import provider_available
from .taxonomy import SKILL_TAXONOMY

LOGGER = logging.getLogger(__name__)


def _normalize(text: str) -> str:
    """Normalize text while preserving punctuation used by technical skill names."""
    return f" {re.sub(r'[^a-z0-9+./#& -]', ' ', text.lower())} "


def _matches_variant(normalized_text: str, variant: str) -> bool:
    """Match one taxonomy variant as a bounded phrase, not an arbitrary substring."""
    needle = variant.strip().lower()
    if not needle:
        return False

    prefix = r"(?<![a-z0-9])" if needle[0].isalnum() else ""
    suffix = r"(?![a-z0-9])" if needle[-1].isalnum() else ""
    return re.search(f"{prefix}{re.escape(needle)}{suffix}", normalized_text) is not None


def extract_skills_rule_based(text: str) -> list[dict[str, str]]:
    """Return deterministic curated-taxonomy matches with source evidence."""
    normalized = _normalize(text)
    found: list[dict[str, str]] = []
    for category, skills in SKILL_TAXONOMY.items():
        for skill, variants in skills.items():
            for variant in variants:
                if _matches_variant(normalized, variant):
                    found.append(
                        {
                            "skill": skill,
                            "category": category,
                            "evidence": variant.strip(),
                            "method": "rule_based",
                        }
                    )
                    break
    return found


def llm_available() -> bool:
    """Compatibility name for the explicitly enabled optional-provider mode."""
    return provider_available()


def extract_skills(text: str) -> list[dict[str, str]]:
    """Combine deterministic extraction with validated optional provider results."""
    results = extract_skills_rule_based(text)

    if llm_available():
        from .llm_extractor import extract_skills_llm

        seen = {result["skill"].casefold() for result in results}
        try:
            for result in extract_skills_llm(text):
                key = result["skill"].casefold()
                if key not in seen:
                    results.append(result)
                    seen.add(key)
        except (ImportError, RuntimeError, ValueError, TimeoutError):
            LOGGER.warning("Provider extraction failed; continuing with rule-based results")

    return results
