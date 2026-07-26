# Security Policy

## Supported version

The latest `main` branch is the supported public portfolio version.

## Reporting a vulnerability

Do not open a public issue containing API keys, private candidate information, restricted employer data or exploit details. Contact the repository owner privately with a concise reproduction and affected files.

## Security boundaries

- Public examples use synthetic or explicitly permitted data.
- Rule-based extraction is deterministic and requires no external provider.
- Optional provider output is untrusted and validated before use.
- Posting text is escaped before being placed inside provider delimiters.
- SQL writes are parameterised and foreign keys are enabled.
- The application never executes provider-generated code or unrestricted SQL.
- Raw provider errors, keys and private posting text must not be exposed in user-facing output.

## Non-goals

This repository is not a governed real-time labour-market dataset, a production multi-tenant service or a guarantee of complete skill-market accuracy. A commercial deployment requires licensed ingestion, identity, tenant isolation, secrets management, monitoring, retention controls and independent security review.
