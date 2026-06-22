#!/usr/bin/env python3
"""Decode full-chunk encoded b64 array and save all partner .txt files."""

import json
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent


def decode_payload(encoded: str) -> list:
    import base64

    raw = base64.b64decode(encoded.strip())
    text = unquote(raw.decode("latin-1"))
    return json.loads(text)


def main() -> None:
    chunk = sys.argv[1]
    encoded = sys.stdin.read()
    b64s = decode_payload(encoded)
    out = ROOT / "logo_batches" / "b64"
    out.mkdir(parents=True, exist_ok=True)
    for i, b64 in enumerate(b64s):
        (out / f"export-{chunk}-{i}.txt").write_text(b64.strip())
    dest = ROOT / "logo_batches" / f"export-{chunk}.json"
    meta = json.loads(
        (ROOT / "logo_batches" / "meta" / f"export-{chunk}.json").read_text()
    )
    partners = [{**m, "b64": b} for m, b in zip(meta, b64s)]
    dest.write_text(json.dumps(partners))
    subprocess.run(
        [sys.executable, str(ROOT / "save_chunk.py"), str(dest)],
        check=True,
    )
    print(f"Chunk {chunk}: {len(b64s)} partners")


if __name__ == "__main__":
    main()
