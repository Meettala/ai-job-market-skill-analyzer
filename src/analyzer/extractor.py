"""
Skill extraction from job posting text.

Two extractors are provided:

- extract_skills_rule_based(): zero-dependency keyword matcher against the
  taxonomy. Always available, always deterministic, no API key needed.
- extract_skills_llm(): optional, only used when OPENAI_API_KEY or
  ANTHROPIC_API_KEY is set (see llm_extractor.py). Produces a broader,
  more flexible skill list including terms outside the fixed taxonomy.

extract_skills() picks whichever is available so the pipeline degrades
gracefully instead of failing when no key is configured.
"""

from __future__ import annotations

import os
import re

from .taxonomy import SKILL_TAXONOMY, skill_category


def _normalize(text: str) -> str:
    return f" {re.sub(r'[^a-z0-9+./#& ]', ' ', text.lower())} "


def extract_skills_rule_based(text: str) -> list[dict]:
    """Deterministic keyword match. Returns list of {skill, category, evidence}."""
    normalized = _normalize(text)
    found = []
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


def extract_skills(text: str) -> list[dict]:
    """
    Preferred entry point. Uses rule-based extraction always (fast, free,
    reliable baseline), and layers in LLM extraction on top when a key is
    configured, for skills the fixed taxonomy would otherwise miss.
    """
    results = extract_skills_rule_based(text)

    if llm_available():
        from .llm_extractor import extract_skills_llm  # imported lazily

        seen = {r["skill"] for r in results}
        try:
            llm_results = extract_skills_llm(text)
            for r in llm_results:
                if r["skill"] not in seen:
                    results.append(r)
                    seen.add(r["skill"])
        except Exception as exc:  # never let an LLM hiccup break the pipeline
            print(f"[extractor] LLM extraction skipped after error: {exc}")

    return results
