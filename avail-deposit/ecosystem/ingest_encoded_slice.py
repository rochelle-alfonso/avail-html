#!/usr/bin/env python3
"""Decode btoa(unescape(encodeURIComponent(JSON))) slice from MCP and save."""

import json
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent


def decode_payload(encoded: str) -> list:
    # Reverse: btoa(unescape(encodeURIComponent(JSON.stringify(slice))))
    import base64

    raw = base64.b64decode(encoded)
    text = unquote(raw.decode("latin-1"))
    return json.loads(text)


def main() -> None:
    chunk, start, encoded = sys.argv[1], sys.argv[2], sys.argv[3]
    arr = decode_payload(encoded)
    SLICES = ROOT / "logo_batches" / "slices"
    SLICES.mkdir(parents=True, exist_ok=True)
    (SLICES / f"export-{chunk}-{start}.json").write_text(json.dumps(arr))
    subprocess.run(
        [sys.executable, str(ROOT / "save_b64_array_stdin.py"), chunk, start],
        input=json.dumps(arr),
        text=True,
        check=True,
    )
    print(f"Saved slice export-{chunk}-{start} ({len(arr)} partners)")


if __name__ == "__main__":
    main()
