#!/usr/bin/env python3
"""Save all JSON files from logo_batches/b64_cache/ via save_b64_map_stdin.py."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "logo_batches" / "b64_cache"


def main() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    files = sorted(CACHE.glob("*.json"))
    if not files:
        print("No cached b64 files")
        return
    for path in files:
        data = json.loads(path.read_text())
        proc = subprocess.run(
            [sys.executable, str(ROOT / "save_b64_map_stdin.py")],
            input=json.dumps(data),
            text=True,
            capture_output=True,
        )
        print(proc.stdout.strip() or proc.stderr.strip())
    print(f"Flushed {len(files)} cache files")


if __name__ == "__main__":
    main()
