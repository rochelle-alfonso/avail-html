#!/usr/bin/env python3
"""Write batch-N.json from two slice payloads (each {id, data} or {id, slice, data})."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BATCHES = ROOT / "logo_batches"


def main() -> None:
    batch_id = int(sys.argv[1])
    slices = json.load(sys.stdin)
    items = []
    for s in slices:
        items.extend(s["data"])
    (BATCHES / f"batch-{batch_id}.json").write_text(json.dumps(items))
    print(f"Wrote batch-{batch_id}.json ({len(items)} items)")


if __name__ == "__main__":
    main()
