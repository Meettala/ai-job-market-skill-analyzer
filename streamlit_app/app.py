"""Portfolio Streamlit interface for the Job Market Skill Analyzer."""

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

from src.analyzer.db import get_connection, posting_count
from src.analyzer.extractor import llm_available
from src.analyzer.pipeline import DB_PATH, run_pipeline
from src.analyzer.report import gap_report, skill_cooccurrence, skill_frequency

st.set_page_config(
    page_title="Job Market Skill Analyzer",
    page_icon="📊",
    layout="wide",
)

st.title("Job Market Skill Analyzer")
st.caption(
    "Dataset-scoped skill frequency and entered-skill comparison using a synthetic, "
    "non-representative sample of AI/ML postings. No web scraping or restricted employer "
    "data is used in this public demo."
)

with st.expander("How this demo works", expanded=False):
    st.markdown(
        """
        1. Synthetic AI/ML job postings are processed locally.
        2. A curated deterministic taxonomy extracts known skills without a key.
        3. Provider extraction is explicit, validated and falls back safely.
        4. SQLite/pandas calculate dataset-scoped frequency and co-occurrence.
        5. Entered skills are compared with recurring extracted sample terms.
        6. Bundled ESCO is a reference/lookup vocabulary, not the active extractor.
        """
    )

try:
    if not DB_PATH.exists():
        with st.spinner("Preparing the synthetic sample dataset..."):
            run_pipeline()
except (OSError, ValueError, RuntimeError):
    st.error(
        "The demonstration dataset could not be prepared. Check the local files and try again."
    )
    st.stop()

mode = (
    "Explicitly enabled provider-assisted + deterministic rule-based"
    if llm_available()
    else "Deterministic rule-based (provider disabled or unavailable)"
)
st.info(f"Extraction mode: **{mode}**")

try:
    connection = get_connection(DB_PATH)
    try:
        frequency = skill_frequency(connection)
        cooccurrence = skill_cooccurrence(connection)
        total_postings = posting_count(connection)

        if frequency.empty:
            st.warning("No skill evidence is available in the current dataset.")
            st.stop()

        metric_one, metric_two, metric_three = st.columns(3)
        metric_one.metric("Synthetic postings", total_postings)
        metric_two.metric("Distinct extracted skills", len(frequency))
        metric_three.metric("Most frequent sample skill", str(frequency.iloc[0]["skill"]))

        left_column, right_column = st.columns([2, 1])
        with left_column:
            st.subheader("Most frequent skills in this sample")
            st.bar_chart(frequency.set_index("skill")["postings_mentioning"].head(15))
            st.dataframe(frequency, use_container_width=True, hide_index=True)

        with right_column:
            st.subheader("Explore by category")
            categories = ["All", *sorted(frequency["category"].dropna().unique().tolist())]
            chosen = st.selectbox("Skill category", categories)
            filtered = frequency if chosen == "All" else frequency[frequency["category"] == chosen]
            st.dataframe(filtered, use_container_width=True, hide_index=True)

        st.subheader("Recurring skill combinations in the analysed sample")
        if cooccurrence.empty:
            st.caption("No repeated skill pairs are present in the current sample.")
        else:
            st.dataframe(cooccurrence, use_container_width=True, hide_index=True)

        st.subheader("Entered-skill comparison")
        st.caption(
            "Enter comma-separated skill labels. This literal comparison uses only recurring "
            "terms extracted from the analysed sample; it does not verify capability, predict "
            "hiring, or produce an ATS score."
        )
        default_skills = "Python, Pandas, SQL, scikit-learn, Git, Statistics"
        user_input = st.text_input(
            "Entered skills",
            value=default_skills,
            max_chars=1000,
        )
        candidate_skills = [item.strip() for item in user_input.split(",") if item.strip()]

        if candidate_skills:
            report = gap_report(connection, candidate_skills)
            matched_column, missing_column = st.columns(2)
            with matched_column:
                st.markdown("**Recurring sample skills also present in entered skills**")
                st.dataframe(
                    pd.DataFrame(report["matched_skills"]),
                    use_container_width=True,
                    hide_index=True,
                )
            with missing_column:
                st.markdown("**Recurring sample skills not present in entered skills**")
                st.dataframe(
                    pd.DataFrame(report["missing_skills"]),
                    use_container_width=True,
                    hide_index=True,
                )
            st.metric(
                "Coverage of recurring sample skills",
                f"{report['match_rate_pct']}%",
            )
        else:
            st.warning("Enter at least one skill to calculate the comparison.")
    finally:
        connection.close()
except (OSError, ValueError, RuntimeError):
    st.error("The analysis could not be displayed safely. Rebuild the demo data and try again.")

st.divider()
st.caption(
    "Portfolio demonstration only. The sample is synthetic and non-representative; results "
    "describe only the analysed postings and are not UK-wide market statistics, hiring "
    "probabilities, capability assessments or ATS scores. Use only licensed or explicitly "
    "permitted data in future work."
)
