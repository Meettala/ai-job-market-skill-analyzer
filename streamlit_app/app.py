"""Portfolio Streamlit interface for the AI Job Market Skill Analyzer."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# Streamlit Community Cloud executes this file from ``streamlit_app`` and installs
# ``requirements.txt`` without necessarily installing the local package. Add the
# repository root explicitly so the source package remains importable in both
# local and hosted execution environments.
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from src.analyzer.db import get_connection
from src.analyzer.extractor import llm_available
from src.analyzer.pipeline import DB_PATH, run_pipeline
from src.analyzer.report import gap_report, skill_cooccurrence, skill_frequency

st.set_page_config(
    page_title="AI Job Market Skill Analyzer",
    page_icon="📊",
    layout="wide",
)

st.title("AI Job Market Skill Analyzer")
st.caption(
    "Evidence-based skill demand and candidate-gap analysis using synthetic sample postings. "
    "No web scraping or restricted employer data is used in this public demo."
)

with st.expander("How this demo works", expanded=False):
    st.markdown(
        """
        1. Synthetic AI/ML job postings are processed locally.
        2. A deterministic taxonomy extracts known skills without an API key.
        3. Optional provider extraction is validated and falls back safely.
        4. SQLite and pandas calculate skill frequency, co-occurrence and candidate gaps.
        """
    )

try:
    if not DB_PATH.exists():
        with st.spinner("Preparing the synthetic market dataset..."):
            run_pipeline()
except (OSError, ValueError, RuntimeError):
    st.error(
        "The demonstration dataset could not be prepared. Check the local files and try again."
    )
    st.stop()

mode = "Validated LLM-assisted + rule-based" if llm_available() else "Deterministic rule-based"
st.info(f"Extraction mode: **{mode}**")

try:
    connection = get_connection(DB_PATH)
    try:
        frequency = skill_frequency(connection)
        cooccurrence = skill_cooccurrence(connection)

        if frequency.empty:
            st.warning("No skill evidence is available in the current dataset.")
            st.stop()

        metric_one, metric_two, metric_three = st.columns(3)
        metric_one.metric("Synthetic postings", int(frequency["postings_mentioning"].max()))
        metric_two.metric("Distinct skills", len(frequency))
        metric_three.metric("Top skill", str(frequency.iloc[0]["skill"]))

        left_column, right_column = st.columns([2, 1])
        with left_column:
            st.subheader("Most in-demand skills")
            st.bar_chart(frequency.set_index("skill")["postings_mentioning"].head(15))
            st.dataframe(frequency, use_container_width=True, hide_index=True)

        with right_column:
            st.subheader("Explore by category")
            categories = ["All", *sorted(frequency["category"].dropna().unique().tolist())]
            chosen = st.selectbox("Skill category", categories)
            filtered = frequency if chosen == "All" else frequency[frequency["category"] == chosen]
            st.dataframe(filtered, use_container_width=True, hide_index=True)

        st.subheader("Common skill combinations")
        if cooccurrence.empty:
            st.caption("No repeated skill pairs are present in the current sample.")
        else:
            st.dataframe(cooccurrence, use_container_width=True, hide_index=True)

        st.subheader("Candidate skill-gap report")
        st.caption(
            "Enter comma-separated skills. Results are calculated only from the analysed sample."
        )
        default_skills = "Python, Pandas, SQL, scikit-learn, Git, Statistics"
        user_input = st.text_input(
            "Candidate skills",
            value=default_skills,
            max_chars=1000,
        )
        candidate_skills = [item.strip() for item in user_input.split(",") if item.strip()]

        if candidate_skills:
            report = gap_report(connection, candidate_skills)
            matched_column, missing_column = st.columns(2)
            with matched_column:
                st.markdown("**Matched market skills**")
                st.dataframe(
                    pd.DataFrame(report["matched_skills"]),
                    use_container_width=True,
                    hide_index=True,
                )
            with missing_column:
                st.markdown("**Missing high-demand skills**")
                st.dataframe(
                    pd.DataFrame(report["missing_skills"]),
                    use_container_width=True,
                    hide_index=True,
                )
            st.metric("Coverage of high-demand skills", f"{report['match_rate_pct']}%")
        else:
            st.warning("Enter at least one skill to calculate a gap report.")
    finally:
        connection.close()
except (OSError, ValueError, RuntimeError):
    st.error("The analysis could not be displayed safely. Rebuild the demo data and try again.")

st.divider()
st.caption(
    "Portfolio demonstration only. The sample is synthetic and does not represent complete or "
    "real-time labour-market coverage. Use only licensed or explicitly permitted data in "
    "future work."
)
