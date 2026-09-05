#!/usr/bin/env python3
"""Validate and print counts from the committed ESCO artefact without rebuilding it."""

from __future__ import annotations

import json

from src.analyzer.esco_vocabulary import artifact_summary, load_vocabulary


def main() -> int:
    vocabulary = load_vocabulary()
    summary = artifact_summary()
    output = {
        **summary,
        "attribution_present": bool(vocabulary["attribution"].strip()),
        "scope_note_present": bool(vocabulary["scopeNote"].strip()),
        "licence": vocabulary["licence"],
        "generated_by": vocabulary["generatedBy"],
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
