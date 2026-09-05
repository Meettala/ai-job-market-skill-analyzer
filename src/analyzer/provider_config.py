"""Configuration boundary for optional external-provider extraction."""

from __future__ import annotations

import os

_TRUE_VALUES = {"1", "true", "yes", "on"}


def provider_mode_enabled() -> bool:
    """Return whether optional provider extraction was explicitly enabled."""
    return os.environ.get("ENABLE_PROVIDER_MODE", "").strip().casefold() in _TRUE_VALUES


def provider_key_available() -> bool:
    """Return whether a supported provider credential is present."""
    return bool(os.environ.get("OPENAI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY"))


def provider_available() -> bool:
    """Provider calls require both explicit opt-in and a provider credential."""
    return provider_mode_enabled() and provider_key_available()
