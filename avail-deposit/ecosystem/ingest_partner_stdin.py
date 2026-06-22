#!/usr/bin/env python3
"""Read partner JSON from stdin; save b64 file and PNG."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> None:
    chunk, idx = sys.argv[1], sys.argv[2]
    partner = json.load(sys.stdin)
    b64_dir = ROOT / "logo_batches" / "b64"
    b64_dir.mkdir(parents=True, exist_ok=True)
    (b64_dir / f"export-{chunk}-{idx}.txt").write_text(partner["b64"])
    from save_chunk import save_items

    save_items([partner])
    print(f"saved partner export-{chunk}-{idx} ({partner['name']})")


if __name__ == "__main__":
    main()
