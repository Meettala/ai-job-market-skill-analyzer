# Contributing

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest
ruff check src streamlit_app tests data
```

On Windows, activate with `.venv\Scripts\activate`.

## Required standards

- Keep public data synthetic or explicitly permitted.
- Preserve deterministic no-key extraction.
- Treat provider output and posting text as untrusted.
- Use parameterised SQL only.
- Add positive, negative and edge-case tests for behavioural changes.
- Do not commit keys, candidate documents, restricted datasets or generated databases.
- Keep documentation claims traceable to code, tests or measured evidence.

All pull requests must pass Python 3.10–3.12 tests, Ruff and dependency auditing.
