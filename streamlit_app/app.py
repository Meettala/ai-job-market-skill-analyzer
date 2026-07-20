"""
AI Job Market Skill Analyzer — Streamlit demo.

Run locally with:
    streamlit run streamlit_app/app.py
"""

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.analyzer.db import get_connection  # noqa: E402
from src.analyzer.extractor import llm_available  # noqa: E402
from src.analyzer.pipeline import DB_PATH, run_pipeline  # noqa: E402
from src.analyzer.report import gap_report, skill_cooccurrence, skill_frequency  # noqa: E402

st.set_page_config(page_title="AI Job Market Skill Analyzer", layout="wide")

st.title("AI Job Market Skill Analyzer")
st.caption(
    "Built on synthetic sample postings — no scraping used. "
    "See docs/security/safety-rules.md for why."
)

if not DB_PATH.exists():
    with st.spinner("Running pipeline for the first time..."):
        run_pipeline()

conn = get_connection(DB_PATH)

extraction_mode = "LLM-assisted + rule-based" if llm_available() else "Rule-based only (no API key configured)"
st.info(f"Skill extraction mode: **{extraction_mode}**")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Most in-demand skills")
    freq = skill_frequency(conn)
    st.bar_chart(freq.set_index("skill")["postings_mentioning"].head(15))
    st.dataframe(freq, use_container_width=True, hide_index=True)

with col2:
    st.subheader("Filter by category")
    categories = ["All"] + sorted(freq["category"].dropna().unique().tolist())
    chosen = st.selectbox("Category", categories)
    filtered = freq if chosen == "All" else freq[freq["category"] == chosen]
    st.dataframe(filtered, use_container_width=True, hide_index=True)

st.subheader("Skills that most often appear together")
cooc = skill_cooccurrence(conn)
st.dataframe(cooc, use_container_width=True, hide_index=True)

st.subheader("Your skill gap report")
st.caption("Enter your skills (comma separated) to see what's missing for this market.")
default_skills = "Python, Pandas, SQL, scikit-learn, Git, Statistics"
user_input = st.text_input("Your skills", value=default_skills)
candidate_skills = [s.strip() for s in user_input.split(",") if s.strip()]

if candidate_skills:
    report = gap_report(conn, candidate_skills)
    left, right = st.columns(2)
    with left:
        st.markdown("**✅ Matched skills**")
        st.dataframe(pd.DataFrame(report["matched_skills"]), use_container_width=True, hide_index=True)
    with right:
        st.markdown("**⚠️ Missing high-demand skills**")
        st.dataframe(pd.DataFrame(report["missing_skills"]), use_container_width=True, hide_index=True)
    st.metric("Coverage of high-demand skills", f"{report['match_rate_pct']}%")

st.divider()
st.caption(
    "Demo data is synthetic (see data/generate_sample_postings.py). "
    "Swap in a real, permitted dataset to analyze the actual market."
)
