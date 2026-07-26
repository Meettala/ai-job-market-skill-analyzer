"""Skill extraction from job posting text."""

from __future__ import annotations

import logging
import os
import re

from .taxonomy import SKILL_TAXONOMY

LOGGER = logging.getLogger(__name__)


def _normalize(text: str) -> str:
    return f" {re.sub(r'[^a-z0-9+./#& ]', ' ', text.lower())} "


def extract_skills_rule_based(text: str) -> list[dict[str, str]]:
    """Return deterministic taxonomy matches with source evidence."""
    normalized = _normalize(text)
    found: list[dict[str, str]] = []
    for category, skills in SKILL_TAXONOMY.items():
        for skill, variants in skills.items():
            for variant in variants:
                if variant in normalized:
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
    return bool(os.environ.get("OPENAI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY"))


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
