#!/usr/bin/env python3
"""Merge batch slice payloads and save via save_batches_stdin."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> None:
    batch_id = int(sys.argv[1])
    items = []
    for path in sys.argv[2:]:
        payload = json.loads(Path(path).read_text())
        if isinstance(payload, dict) and "data" in payload:
            items.extend(payload["data"])
        elif isinstance(payload, list):
            items.extend(payload)
    proc = subprocess.run(
        [sys.executable, str(ROOT / "save_batches_stdin.py")],
        input=json.dumps({"id": batch_id, "data": items}),
        text=True,
        capture_output=True,
    )
    print(proc.stdout.strip() or proc.stderr.strip())


if __name__ == "__main__":
    main()
