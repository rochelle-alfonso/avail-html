#!/usr/bin/env python3
"""Save slug->b64 JSON file via save_b64_map_stdin."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> None:
    path = Path(sys.argv[1])
    data = json.loads(path.read_text())
    proc = subprocess.run(
        [sys.executable, str(ROOT / "save_b64_map_stdin.py")],
        input=json.dumps(data),
        text=True,
        capture_output=True,
    )
    print(proc.stdout.strip() or proc.stderr.strip())


if __name__ == "__main__":
    main()
