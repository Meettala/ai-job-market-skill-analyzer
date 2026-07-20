import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.analyzer.extractor import extract_skills_rule_based


def test_extracts_known_skill():
    text = "We use Python and PyTorch to build NLP models with the OpenAI API."
    skills = {s["skill"] for s in extract_skills_rule_based(text)}
    assert "Python" in skills
    assert "PyTorch" in skills
    assert "NLP" in skills
    assert "LLM APIs" in skills


def test_no_false_match_on_unrelated_text():
    text = "We are hiring a barista with excellent customer service skills."
    skills = extract_skills_rule_based(text)
    assert skills == []


def test_case_insensitive():
    text = "PYTHON and pandas experience required."
    skills = {s["skill"] for s in extract_skills_rule_based(text)}
    assert "Python" in skills
    assert "Pandas" in skills
