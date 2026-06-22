#!/usr/bin/env python3
"""Build partner slug list and missing URL entries from partners.json."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def slugify(name: str) -> str:
    return re.sub(r"(^-|-$)", "", re.sub(r"[^a-z0-9]+", "-", name.lower()))


def partner_slug(name: str, tag: str, seen: dict[str, int]) -> str:
    slug = slugify(name)
    if slug in seen:
        suffix = slugify(tag) or str(seen[slug])
        slug = f"{slug}-{suffix}"
    seen[slug] = seen.get(slug, 0) + 1
    return slug


def main() -> None:
    partners = json.loads((ROOT / "partners.json").read_text())
    seen: dict[str, int] = {}
    entries = []
    for p in partners:
        slug = partner_slug(p["name"], p.get("tag") or "", seen)
        entries.append({
            "slug": slug,
            "name": p["name"],
            "tag": p.get("tag") or "",
            "logoId": p["logoId"],
        })
    (ROOT / "partner_manifest.json").write_text(json.dumps(entries, indent=2))
    print(f"Wrote {len(entries)} entries to partner_manifest.json")


if __name__ == "__main__":
    main()
