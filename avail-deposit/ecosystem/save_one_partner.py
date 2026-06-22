#!/usr/bin/env python3
"""Save single partner JSON object to logo_batches/slices/batch-{N}-p{I}.json."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SLICES = ROOT / "logo_batches" / "slices"


def main() -> None:
    batch_id, partner_idx = sys.argv[1], sys.argv[2]
    item = json.load(sys.stdin)
    SLICES.mkdir(parents=True, exist_ok=True)
    dest = SLICES / f"batch-{batch_id}-p{partner_idx}.json"
    dest.write_text(json.dumps(item))
    print(dest)


if __name__ == "__main__":
    main()
