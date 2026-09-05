# Security Policy

## Supported version

The latest `main` branch is the supported public portfolio version.

## Reporting a vulnerability

Do not open a public issue containing API keys, private candidate information, restricted employer data or exploit details. Contact the repository owner privately with a concise reproduction and affected files.

## Security boundaries

- Public examples use synthetic or explicitly permitted data.
- Rule-based extraction is deterministic and requires no external provider.
- External provider extraction is default-off and requires `ENABLE_PROVIDER_MODE=true` plus a supported provider key; a key alone must not activate external calls.
- When provider mode is enabled, posting text is sent to the selected provider after delimiter escaping.
- Optional provider output is untrusted, schema/length validated, de-duplicated and never executed.
- Provider failures or invalid output fall back to deterministic extraction with a generic warning.
- SQL writes are parameterised, foreign keys are enabled and duplicate skills per posting are controlled.
- Raw provider errors, keys and private posting text must not be exposed in user-facing output.

## Non-goals

This repository is not a governed real-time labour-market dataset, a production multi-tenant service, an ATS score, a hiring-probability model or a guarantee of complete skill extraction. A commercial deployment requires licensed ingestion, identity, tenant isolation, managed secrets, monitoring, retention controls, governance and independent security review.
