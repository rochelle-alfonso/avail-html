#!/usr/bin/env python3
"""Save slug->b64 JSON from a file to b64_cache and PNGs."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "logo_batches" / "b64_cache"


def save(name: str, data: dict) -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    (CACHE / f"{name}.json").write_text(json.dumps(data))
    proc = subprocess.run(
        [sys.executable, str(ROOT / "save_b64_map_stdin.py")],
        input=json.dumps(data),
        text=True,
        capture_output=True,
    )
    print(proc.stdout.strip() or proc.stderr.strip())


def main() -> None:
    path = Path(sys.argv[1])
    name = sys.argv[2] if len(sys.argv) > 2 else path.stem
    save(name, json.loads(path.read_text()))


if __name__ == "__main__":
    main()
