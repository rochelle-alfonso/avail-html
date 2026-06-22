#!/usr/bin/env python3
"""Pull partner logo batches from Figma shared plugin data via stdin JSON."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BATCHES = ROOT / "logo_batches"
BATCHES.mkdir(exist_ok=True)


def main() -> None:
    payload = json.load(sys.stdin)
    if isinstance(payload, dict) and "id" in payload and "data" in payload:
        payload = [payload]
    for entry in payload:
        batch_id = entry["id"]
        (BATCHES / f"batch-{batch_id}.json").write_text(json.dumps(entry["data"]))
        print(f"Saved batch-{batch_id}.json ({len(entry['data'])} logos)")


if __name__ == "__main__":
    main()
