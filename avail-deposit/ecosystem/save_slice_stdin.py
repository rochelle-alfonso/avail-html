#!/usr/bin/env python3
"""Save a partner slice JSON array from stdin."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> None:
    chunk, start = sys.argv[1], sys.argv[2]
    data = json.load(sys.stdin)
    out = ROOT / "logo_batches" / "slices" / f"export-{chunk}-{start}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data))
    print(f"Saved {len(data)} partners -> {out}")


if __name__ == "__main__":
    main()
