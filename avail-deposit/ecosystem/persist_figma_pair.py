#!/usr/bin/env python3
"""Write slug->b64 JSON from stdin to b64_cache and save PNGs."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "logo_batches" / "b64_cache"


def main() -> None:
    name = sys.argv[1] if len(sys.argv) > 1 else "pair_auto"
    data = json.load(sys.stdin)
    CACHE.mkdir(parents=True, exist_ok=True)
    dest = CACHE / f"{name}.json"
    dest.write_text(json.dumps(data))
    proc = subprocess.run(
        [sys.executable, str(ROOT / "save_b64_map_stdin.py")],
        input=json.dumps(data),
        text=True,
        capture_output=True,
    )
    print(proc.stdout.strip() or proc.stderr.strip())


if __name__ == "__main__":
    main()
