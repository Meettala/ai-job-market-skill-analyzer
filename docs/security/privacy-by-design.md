# Privacy by design — AI Job Market Skill Analyzer

- No personal candidate data is required to run the market-side analysis.
- The candidate skill list used for the gap report is provided directly by
  the user at run time (Streamlit text input) and is not persisted beyond
  the session.
- No third-party personal data (e.g. real recruiter or applicant names) is
  collected — postings analyzed are company/role-level, not person-level.
- If real scraped postings are added later, only role-level fields should
  be stored (title, company, skills) — no personal contact details from
  postings should ever be captured.
