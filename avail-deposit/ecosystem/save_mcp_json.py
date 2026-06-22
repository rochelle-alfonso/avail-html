#!/usr/bin/env python3
"""Save MCP JSON payload from file: slug map, batch payload, or batch slice."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> None:
    path = Path(sys.argv[1])
    payload = json.loads(path.read_text())
    if "id" in payload and "data" in payload and all(
        isinstance(x, dict) and "name" in x for x in payload["data"]
    ):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "save_batches_stdin.py")],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
        )
    else:
        proc = subprocess.run(
            [sys.executable, str(ROOT / "apply_b64_json.py")],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
        )
    print(proc.stdout.strip() or proc.stderr.strip())
    print(f"PNG count: {len(list((ROOT / 'assets' / 'partners').glob('*.png')))}")


if __name__ == "__main__":
    main()
