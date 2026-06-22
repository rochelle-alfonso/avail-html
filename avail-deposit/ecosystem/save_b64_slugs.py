#!/usr/bin/env python3
"""Save slug->b64 dict from Figma MCP to logo_batches/b64_slugs/."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
B64_DIR = ROOT / "logo_batches" / "b64_slugs"


def main() -> None:
    payload = json.load(sys.stdin)
    B64_DIR.mkdir(parents=True, exist_ok=True)
    for slug, b64 in payload.items():
        if not b64:
            print(f"empty b64 for {slug}", file=sys.stderr)
            continue
        (B64_DIR / f"{slug}.txt").write_text(b64)
        print(slug)


if __name__ == "__main__":
    main()
