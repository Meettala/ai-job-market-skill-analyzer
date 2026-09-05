import os

import pytest

from src.analyzer.extractor import extract_skills, llm_available
from src.analyzer.llm_extractor import (
    InvalidLLMExtraction,
    extract_skills_llm,
    parse_llm_extraction,
)


def test_parse_valid_provider_output():
    result = parse_llm_extraction(
        '[{"skill":"Python","category":"Programming","evidence":"Python"}]'
    )
    assert result == [
        {
            "skill": "Python",
            "category": "Programming",
            "evidence": "Python",
            "method": "llm",
        }
    ]


@pytest.mark.parametrize(
    "raw",
    [
        "not json",
        "{}",
        "[]",
        '[{"skill":"Python"}]',
        '[{"skill":123,"category":"Programming","evidence":"Python"}]',
        '[{"skill":"","category":"Programming","evidence":"Python"}]',
        '[{"skill":"Python","category":"Programming","evidence":"Python","code":"run"}]',
    ],
)
def test_rejects_malformed_provider_output(raw):
    with pytest.raises(InvalidLLMExtraction):
        parse_llm_extraction(raw)


def test_deduplicates_provider_skills_case_insensitively():
    result = parse_llm_extraction(
        """[
        {"skill":"Python","category":"Programming","evidence":"Python"},
        {"skill":"python","category":"Programming","evidence":"python"}
        ]"""
    )
    assert len(result) == 1


@pytest.mark.parametrize(
    ("flag", "key_name", "expected"),
    [
        (None, None, False),
        (None, "OPENAI_API_KEY", False),
        ("false", "OPENAI_API_KEY", False),
        ("true", None, False),
        ("true", "OPENAI_API_KEY", True),
        ("TRUE", "ANTHROPIC_API_KEY", True),
        ("1", "OPENAI_API_KEY", True),
    ],
)
def test_provider_activation_truth_table(monkeypatch, flag, key_name, expected):
    monkeypatch.delenv("ENABLE_PROVIDER_MODE", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    if flag is not None:
        monkeypatch.setenv("ENABLE_PROVIDER_MODE", flag)
    if key_name is not None:
        monkeypatch.setenv(key_name, "test-key")
    assert llm_available() is expected


def test_key_alone_does_not_enable_direct_provider_call(monkeypatch):
    monkeypatch.delenv("ENABLE_PROVIDER_MODE", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    assert extract_skills_llm("Python") == []


def test_provider_failure_falls_back_without_exposing_details(monkeypatch, caplog):
    monkeypatch.setenv("ENABLE_PROVIDER_MODE", "true")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    def fail(_text):
        raise InvalidLLMExtraction("secret provider detail")

    monkeypatch.setattr("src.analyzer.llm_extractor.extract_skills_llm", fail)
    result = extract_skills("Python is required")

    assert any(item["skill"] == "Python" for item in result)
    assert "secret provider detail" not in caplog.text


def test_environment_is_cleaned(monkeypatch):
    monkeypatch.delenv("ENABLE_PROVIDER_MODE", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    assert not os.environ.get("OPENAI_API_KEY")
