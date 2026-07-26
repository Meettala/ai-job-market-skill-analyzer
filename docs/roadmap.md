# Roadmap

## Completed portfolio foundation

- Deterministic taxonomy extraction.
- Validated optional provider extraction and safe fallback.
- SQLite storage and pandas/SQL reporting.
- Candidate gap report and Streamlit dashboard.
- Multi-version tests, linting, dependency auditing and Docker support.

## Next evaluation work

1. Build a labelled extraction dataset with expected skills and evidence spans.
2. Measure precision, recall and duplicate rates for taxonomy and provider modes.
3. Calibrate taxonomy variants and candidate-skill normalisation.
4. Add reproducible benchmark reports rather than anecdotal accuracy claims.

## Future product work

- Licensed job-feed ingestion with source and retention controls.
- Dataset provenance, freshness and deduplication metadata.
- Time-series skill trends and location/seniority filters.
- Candidate evidence bank integration with consent and privacy controls.
- Authentication, tenant isolation, managed secrets and audit logging.
- Monitoring for provider cost, latency, failures and extraction drift.

A paid production service should be developed in a separate private proprietary repository with governed data access and commercial controls.
