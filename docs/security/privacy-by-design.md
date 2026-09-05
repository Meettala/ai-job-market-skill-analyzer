# Privacy by design — Job Market Skill Analyzer

- No personal candidate data is required to run the dataset analysis.
- The entered skill list used for comparison is supplied directly by the user at run time and is not written to the SQLite posting tables by the Streamlit interface.
- The public demo postings are synthetic; no real recruiter, applicant or employer-contact personal data is included in the committed sample.
- External provider extraction is default-off. When explicitly enabled with `ENABLE_PROVIDER_MODE=true` and a provider key, posting text is sent to the selected provider, so confidential or restricted text must not be submitted unless that transfer is permitted.
- Any future real-data ingestion must use licensed or explicitly permitted sources and add appropriate provenance, minimisation, retention and governance controls before production use.
