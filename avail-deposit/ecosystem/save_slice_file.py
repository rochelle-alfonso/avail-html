#!/usr/bin/env python3
"""Save MCP b64 slice JSON file and extract to per-partner .txt files."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> None:
    chunk, start, src = sys.argv[1], sys.argv[2], sys.argv[3]
    arr = json.loads(Path(src).read_text())
    subprocess.run(
        [sys.executable, str(ROOT / "save_b64_array_stdin.py"), chunk, start],
        input=json.dumps(arr),
        text=True,
        check=True,
    )


if __name__ == "__main__":
    main()
