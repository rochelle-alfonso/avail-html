#!/usr/bin/env python3
import base64
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "logo_batches"
OUT.mkdir(exist_ok=True)


def slugify(name: str) -> str:
    return re.sub(r"(^-|-$)", "", re.sub(r"[^a-z0-9]+", "-", name.lower()))


def main() -> None:
    batch_id = sys.argv[1]
    data = json.load(sys.stdin)
    (OUT / f"batch-{batch_id}.json").write_text(json.dumps(data))
    partners_dir = ROOT / "assets" / "partners"
    partners_dir.mkdir(parents=True, exist_ok=True)
    seen = set()
    for item in data:
        name = item["name"]
        slug = slugify(name)
        if slug in seen:
            slug = f"{slug}-{batch_id}"
        seen.add(slug)
        dest = partners_dir / f"{slug}.png"
        dest.write_bytes(base64.b64decode(item["b64"]))
    print(f"Saved batch {batch_id}: {len(data)} logos")


if __name__ == "__main__":
    main()
