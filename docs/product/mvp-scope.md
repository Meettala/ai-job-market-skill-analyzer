# MVP scope — AI Job Market Skill Analyzer

## In scope
- Load a set of job postings (synthetic demo data, or a permitted dataset).
- Extract skills per posting (rule-based always; LLM-assisted when a key
  is configured).
- Store postings + extracted skills in SQLite.
- Aggregate: skill frequency, skill co-occurrence.
- Gap report: compare a candidate's skill list against market frequency.
- Two front ends: Streamlit (interactive/local) and a static results view
  on the portfolio site (public link, no server needed).

## Explicitly out of scope for MVP
- Live scraping of any job platform.
- Storing personal candidate data long-term.
- Real-time market monitoring / alerts (future roadmap item).
- Multi-user auth (this is a single-operator analysis tool, not a SaaS).
