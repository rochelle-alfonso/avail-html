#!/usr/bin/env python3
"""Download events page assets from Figma MCP URLs."""

import ssl
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"

FIGMA_URLS = {
    "hero-banner.webp": "https://www.figma.com/api/mcp/asset/8dd46b1c-66df-4ab4-bb38-2649cfcd6340",
    "upcoming/kbw.jpg": "https://www.figma.com/api/mcp/asset/b8eac2bc-c2e8-4ba8-888b-dd31bddb182a",
    "upcoming/token2049.jpg": "https://www.figma.com/api/mcp/asset/e5ddda61-4d78-423a-b576-58559a5a5974",
    "upcoming/devcon8.jpg": "https://www.figma.com/api/mcp/asset/28cdda15-31a4-4c11-b596-8b84a1555efd",
    "past/consensus-miami.jpg": "https://www.figma.com/api/mcp/asset/efbc3e30-4345-436b-8b4b-edf88f0b363b",
    "past/ethcc.webp": "https://www.figma.com/api/mcp/asset/fd806f8c-6d05-4d5c-823f-4e74a563b08a",
    "past/consensus-hk.webp": "https://www.figma.com/api/mcp/asset/b415546e-f15e-4078-8587-76768cf134bd",
    "past/solana-breakpoint.webp": "https://www.figma.com/api/mcp/asset/c8d5f359-b099-443c-a0d1-7c3567d786aa",
    "past/devcon.webp": "https://www.figma.com/api/mcp/asset/da726e2a-a246-4e41-a496-3f4a2be255a0",
    "past/token2049.webp": "https://www.figma.com/api/mcp/asset/92855ff5-2210-4b38-9ba1-dfc8bd260526",
    "footer/demo-decor.png": "https://www.figma.com/api/mcp/asset/e9df3606-13b6-4c3d-ad72-38c50df1c9f6",
    "footer/social-x.svg": "https://www.figma.com/api/mcp/asset/7a327964-f369-4d25-b203-0d531aa5070e",
    "footer/social-telegram.svg": "https://www.figma.com/api/mcp/asset/8f21582a-11d1-4ecd-890d-547037092662",
    "footer/social-linkedin.svg": "https://www.figma.com/api/mcp/asset/18a865e1-0e6e-4504-9a43-93619b783d50",
    "footer/social-youtube.svg": "https://www.figma.com/api/mcp/asset/4a2eb3c4-2012-48de-a47b-adcee0186c58",
}


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
        dest.write_bytes(resp.read())


def main() -> None:
    for rel, url in FIGMA_URLS.items():
        dest = ASSETS / rel
        if dest.exists() and dest.stat().st_size > 100:
            continue
        print(f"Downloading {rel}")
        download(url, dest)
    print("Done.")


if __name__ == "__main__":
    main()
