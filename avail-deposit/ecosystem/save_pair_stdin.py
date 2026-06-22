#!/usr/bin/env python3
"""Save pair JSON from stdin to b64_cache/pair-{idx}.json and optionally flush."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "logo_batches" / "b64_cache"


def main() -> None:
    idx = int(sys.argv[1])
    flush = "--flush" in sys.argv
    data = json.load(sys.stdin)
    CACHE.mkdir(parents=True, exist_ok=True)
    dest = CACHE / f"pair_{idx:02d}.json"
    dest.write_text(json.dumps(data))
    print(f"Saved {dest.name} ({len(data)} slugs)")
    if flush:
        subprocess.run([sys.executable, str(ROOT / "flush_b64_cache.py")], check=True)


if __name__ == "__main__":
    main()
