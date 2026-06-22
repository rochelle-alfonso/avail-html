#!/usr/bin/env python3
"""Save partner logo batches from Figma shared plugin data (via stdin JSON array)."""

import json
import sys
from pathlib import Path

from save_logo_batch import slugify  # noqa: F401 — re-export for convenience

ROOT = Path(__file__).resolve().parent
BATCHES = ROOT / "logo_batches"


def save_batch(batch_id: str, data: list) -> None:
    BATCHES.mkdir(exist_ok=True)
    (BATCHES / f"batch-{batch_id}.json").write_text(json.dumps(data))
    print(f"Wrote batch-{batch_id}.json ({len(data)} partners)")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: export_batches.py <batch-id>  (reads JSON from stdin)")
        sys.exit(1)
    batch_id = sys.argv[1]
    data = json.load(sys.stdin)
    save_batch(batch_id, data)


if __name__ == "__main__":
    main()
