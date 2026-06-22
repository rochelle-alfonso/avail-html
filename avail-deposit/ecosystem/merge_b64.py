#!/usr/bin/env python3
"""Merge slug->b64 JSON from stdin into fetched_b64.json and save PNGs."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STORE = ROOT / "logo_batches" / "fetched_b64.json"


def main() -> None:
    new = json.load(sys.stdin)
    all_data = json.loads(STORE.read_text()) if STORE.exists() else {}
    all_data.update(new)
    STORE.write_text(json.dumps(all_data))
    proc = subprocess.run(
        [sys.executable, str(ROOT / "save_b64_map_stdin.py")],
        input=json.dumps(new),
        text=True,
        capture_output=True,
    )
    print(proc.stdout.strip() or proc.stderr.strip())
    print(f"Store total: {len(all_data)} slugs")


if __name__ == "__main__":
    main()
