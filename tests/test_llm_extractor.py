import os

import pytest

from src.analyzer.extractor import extract_skills
from src.analyzer.llm_extractor import InvalidLLMExtraction, parse_llm_extraction


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


def test_provider_failure_falls_back_without_exposing_details(monkeypatch, caplog):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    def fail(_text):
        raise InvalidLLMExtraction("secret provider detail")

    monkeypatch.setattr("src.analyzer.llm_extractor.extract_skills_llm", fail)
    result = extract_skills("Python is required")

    assert any(item["skill"] == "Python" for item in result)
    assert "secret provider detail" not in caplog.text


def test_environment_is_cleaned(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    assert not os.environ.get("OPENAI_API_KEY")
