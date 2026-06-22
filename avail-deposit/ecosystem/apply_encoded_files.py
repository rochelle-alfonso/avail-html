#!/usr/bin/env python3
"""Fetch all chunks via use_figma MCP encoded payloads saved to logo_batches/encoded/.

Expects files: export-{chunk}.enc (full chunk) or export-{chunk}-{start}.enc (2-partner slice).
Run after MCP batch saves encoded strings to those paths.
"""

import json
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent
ENC = ROOT / "logo_batches" / "encoded"


def decode(encoded: str) -> list:
    import base64

    raw = base64.b64decode(encoded.strip())
    return json.loads(unquote(raw.decode("latin-1")))


def ingest_slice(chunk: int, start: int, arr: list) -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "save_b64_array_stdin.py"), str(chunk), str(start)],
        input=json.dumps(arr),
        text=True,
        check=True,
    )


def ingest_chunk(chunk: int, b64s: list) -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "ingest_encoded_chunk_stdin.py"), str(chunk)],
        input=json.dumps(b64s),
        text=True,
        check=True,
    )


def main() -> None:
    ENC.mkdir(parents=True, exist_ok=True)
    for path in sorted(ENC.glob("*.enc")):
        name = path.stem  # export-1 or export-0-4
        parts = name.split("-")
        if len(parts) == 2:
            chunk = int(parts[1])
            ingest_chunk(chunk, decode(path.read_text()))
        elif len(parts) == 3:
            chunk, start = int(parts[1]), int(parts[2])
            ingest_slice(chunk, start, decode(path.read_text()))
        path.unlink()
    count = len(list((ROOT / "assets" / "partners").glob("*.png")))
    print(f"PNG count: {count}")


if __name__ == "__main__":
    main()
