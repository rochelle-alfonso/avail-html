#!/usr/bin/env python3
"""Apply slug->b64 JSON from stdin: save txt files and PNGs."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> None:
    data = json.load(sys.stdin)
    for script in ("save_b64_slugs.py", "save_b64_map_stdin.py"):
        proc = subprocess.run(
            [sys.executable, str(ROOT / script)],
            input=json.dumps(data),
            text=True,
            capture_output=True,
        )
        print(proc.stdout.strip() or proc.stderr.strip())


if __name__ == "__main__":
    main()
