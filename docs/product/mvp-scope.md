# MVP scope — Job Market Skill Analyzer

## In scope
- Load a defined set of job postings (synthetic demo data, or an explicitly permitted dataset).
- Extract skills per posting with the curated rule-based path; optionally supplement it only when provider mode is explicitly enabled and a provider key is configured.
- Store postings and extracted skills in SQLite.
- Aggregate dataset-scoped skill frequency and skill co-occurrence.
- Compare literal entered skill labels with recurring extracted terms from the analysed dataset.
- Present results through Streamlit and JSON export.

The comparison is not a capability assessment, ATS score or hiring-probability estimate, and sample frequency is not representative labour-market demand.

## Explicitly out of scope for MVP
- Live scraping of any job platform.
- Live or representative labour-market demand claims.
- Storing personal candidate data long-term.
- ATS scoring, hiring probability or inferred candidate capability.
- Real-time market monitoring / alerts.
- Multi-user auth (this is a single-operator analysis tool, not a SaaS).
