#!/usr/bin/env python3
"""Save batch-N.json from stdin: {"id": 16, "data": [...]}."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BATCHES = ROOT / "logo_batches"


def main() -> None:
    payload = json.load(sys.stdin)
    batch_id = payload["id"]
    (BATCHES / f"batch-{batch_id}.json").write_text(json.dumps(payload["data"]))
    print(f"Saved batch-{batch_id}.json ({len(payload['data'])} items)")


if __name__ == "__main__":
    main()
