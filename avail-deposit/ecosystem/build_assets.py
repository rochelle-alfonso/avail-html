#!/usr/bin/env python3
"""Download ecosystem page assets from Figma MCP URLs and decode exported partner logos."""

import base64
import json
import os
import re
import ssl
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"

FIGMA_URLS = {
    "hero-panel.png": "https://www.figma.com/api/mcp/asset/650b72fc-0753-4b1f-be57-d4a463b005e5",
    "decor/pixel-tl.png": "https://www.figma.com/api/mcp/asset/22d3353e-aa7c-40ca-910c-6a511bb109fd",
    "decor/pixel-br.png": "https://www.figma.com/api/mcp/asset/5bdd4739-e3cc-4175-a1ab-3a6df51040bc",
    "decor/pixel-tr.png": "https://www.figma.com/api/mcp/asset/6dd1ea8d-7da1-4cd7-b813-d3d6e648dc46",
    "decor/badge-notch.png": "https://www.figma.com/api/mcp/asset/bc04deac-4db4-449d-849f-c68b24dc6e5a",
    "featured/monad.png": "https://www.figma.com/api/mcp/asset/76274db7-7eb9-499d-a029-197674d848f0",
    "featured/clober.png": "https://www.figma.com/api/mcp/asset/22dfece5-8e3d-467e-8b3c-e3ae89eba16e",
    "featured/farcaster.png": "https://www.figma.com/api/mcp/asset/7c30e39a-3043-484b-9f22-9b5692689cf1",
    "integrations/bean-logo.png": "https://www.figma.com/api/mcp/asset/32c3f18e-b164-4abb-8196-42001b51d06b",
    "integrations/bean.jpg": "https://www.figma.com/api/mcp/asset/d5ab5565-8ddd-4556-9064-dc3ee66be3df",
    "integrations/kalqix-logo.png": "https://www.figma.com/api/mcp/asset/3a7025d7-a590-4182-90f1-f8c07120750b",
    "integrations/kalqix.jpg": "https://www.figma.com/api/mcp/asset/7b28377b-2c82-4429-a825-6eb9437a2ddd",
    "integrations/farcaster-logo.png": "https://www.figma.com/api/mcp/asset/ee50d462-752b-4518-975f-ff09513a4974",
    "integrations/farcaster.jpg": "https://www.figma.com/api/mcp/asset/6e047dcc-fd04-479a-a514-320fc4330040",
    "integrations/sxt-logo.png": "https://www.figma.com/api/mcp/asset/810ef78f-d5a1-4d4d-8521-eb4bf15cff4c",
    "integrations/sxt.jpg": "https://www.figma.com/api/mcp/asset/02fd64e0-7e92-4545-b848-a4602cf3cbcb",
    "spotlight/clober-logo.png": "https://www.figma.com/api/mcp/asset/a8ef527f-5369-4e20-853f-96b348839d84",
    "spotlight/video-thumb.jpg": "https://www.figma.com/api/mcp/asset/5c9a2a1f-2f7c-452e-9de2-05c0b7d87732",
    "spotlight/play.svg": "https://www.figma.com/api/mcp/asset/73324810-99ff-44ad-8363-9d8ab2012ac4",
    "blogs/blog-1.jpg": "https://www.figma.com/api/mcp/asset/0b38c7ff-c66e-4ea0-9c86-949efe358c10",
    "blogs/blog-2.jpg": "https://www.figma.com/api/mcp/asset/345cef5b-facd-4701-810c-1fa343a3c8fd",
    "blogs/blog-3.jpg": "https://www.figma.com/api/mcp/asset/a31f005d-06a5-4476-86ed-156b04f30bdc",
    "testimonials/pingme.svg": "https://www.figma.com/api/mcp/asset/66d00eaa-b035-4374-9137-72a4df7bb55f",
    "testimonials/kalqix.png": "https://www.figma.com/api/mcp/asset/270815ea-89fe-4c9a-b5c5-5b5ddd16f6d5",
    "testimonials/atlantis.png": "https://www.figma.com/api/mcp/asset/da2994d6-a741-46f2-90fe-f8c0287ba906",
    "testimonials/bean.png": "https://www.figma.com/api/mcp/asset/0bfdec75-50c2-4e4a-a4bc-5a00117093ce",
    "testimonials/clober.png": "https://www.figma.com/api/mcp/asset/79a40af1-73f1-44e0-a201-327d1bb626ba",
    "testimonials/quickswap.webp": "https://www.figma.com/api/mcp/asset/dead8b3d-190e-4fe5-8f52-cad673b8f285",
    "testimonials/pixel-br.png": "https://www.figma.com/api/mcp/asset/e77ae944-76df-4003-a9d6-143f256a2ab2",
    "testimonials/pixel-tl.png": "https://www.figma.com/api/mcp/asset/d3cb803a-f2ba-4733-bf01-aafc3066b563",
    "testimonials/arrow-prev.svg": "https://www.figma.com/api/mcp/asset/213a6a29-7caa-4e4a-9d63-6061dda2634c",
    "testimonials/arrow-next.svg": "https://www.figma.com/api/mcp/asset/397c2eee-9fa7-41ec-83da-203136050029",
}


def slugify(name: str) -> str:
    return re.sub(r"(^-|-$)", "", re.sub(r"[^a-z0-9]+", "-", name.lower()))


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
        dest.write_bytes(resp.read())


def save_b64_png(b64: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(base64.b64decode(b64))


def main() -> None:
    for rel, url in FIGMA_URLS.items():
        dest = ASSETS / rel
        if not dest.exists():
            print(f"Downloading {rel}")
            download(url, dest)

    batches_dir = ROOT / "logo_batches"
    if batches_dir.exists():
        seen = set()
        for batch_file in sorted(batches_dir.glob("batch-*.json")):
            items = json.loads(batch_file.read_text())
            for item in items:
                name = item["name"]
                slug = slugify(name)
                if slug in seen:
                    slug = f"{slug}-{slugify(item.get('tag') or 'alt')}"
                seen.add(slug)
                dest = ASSETS / "partners" / f"{slug}.png"
                if not dest.exists():
                    save_b64_png(item["b64"], dest)
                    print(f"Saved partner logo {slug}.png")


if __name__ == "__main__":
    main()
