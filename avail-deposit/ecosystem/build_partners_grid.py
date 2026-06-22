#!/usr/bin/env python3
"""Generate ecosystem/index.html partner grid from partners.json."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARTNERS = ROOT / "partners.json"


def slugify(name: str) -> str:
    return re.sub(r"(^-|-$)", "", re.sub(r"[^a-z0-9]+", "-", name.lower()))


def partner_slug(name: str, tag: str, seen: dict[str, int]) -> str:
    slug = slugify(name)
    if slug in seen:
        suffix = slugify(tag) or str(seen[slug])
        slug = f"{slug}-{suffix}"
    seen[slug] = seen.get(slug, 0) + 1
    return slug


def render_partners(partners: list) -> str:
    seen: dict[str, int] = {}
    rows = []
    for p in partners:
        name = p["name"]
        tag = p.get("tag") or ""
        slug = partner_slug(name, tag, seen)
        tag_html = f'<span class="listing-card__tag">{tag}</span>' if tag else ""
        rows.append(
            f"""          <article class="listing-card" data-tag="{tag}">
            <h3 class="listing-card__name">{name}</h3>
            <div class="listing-card__logo"><img src="assets/partners/{slug}.png" alt="{name}" loading="lazy" decoding="async" /></div>
            <div class="listing-card__footer">{tag_html}</div>
          </article>"""
        )
    return "\n".join(rows)


def main() -> None:
    partners = json.loads(PARTNERS.read_text())
    grid = render_partners(partners)
    out = ROOT / "partners-grid.html"
    out.write_text(grid)
    print(f"Wrote {len(partners)} cards to {out}")


if __name__ == "__main__":
    main()
