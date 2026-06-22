#!/usr/bin/env python3
"""Download about-us page assets from Figma MCP URLs."""

import json
import re
import ssl
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
DC_FILE = Path(
    "/Users/rochellealfonso/.cursor/projects/Users-rochellealfonso-Documents-Avail/agent-tools/5b0c94fd-d45f-4d4a-a05f-212f66c44899.txt"
)

STATIC_URLS = {
    "footer/demo-decor.png": "https://www.figma.com/api/mcp/asset/5242a34d-bd00-4136-abe3-854fbd2053df",
    "footer/social-x.svg": "https://www.figma.com/api/mcp/asset/cb582e9f-d58b-4498-8157-ba550975158b",
    "footer/social-telegram.svg": "https://www.figma.com/api/mcp/asset/fb0d201b-6b3a-48f9-a928-75432a8eefb1",
    "footer/social-linkedin.svg": "https://www.figma.com/api/mcp/asset/6cfd3e2a-009b-4e1e-8c09-933bc561f737",
    "footer/social-youtube.svg": "https://www.figma.com/api/mcp/asset/015b1bf6-56f0-4bca-bde6-89aac0c61871",
    "social/twitter.svg": "https://www.figma.com/api/mcp/asset/4c17f259-8328-4dbe-bdb3-615c35120414",
    "social/linkedin.svg": "https://www.figma.com/api/mcp/asset/5ec2ef0d-d0b6-42de-ba24-ed2448c96966",
    "social/github.svg": "https://www.figma.com/api/mcp/asset/b1f2bb17-1a4b-43a7-a620-9276458c6c0a",
    "life-at-avail.jpg": "https://www.figma.com/api/mcp/asset/3140b290-1a88-4c7f-87d5-a056eb1a7278",
    "investors/longhash-ventures.png": "https://www.figma.com/api/mcp/asset/53dddb39-1c95-4817-acb6-cd39bcc84d56",
    "investors/rw3.png": "https://www.figma.com/api/mcp/asset/28899429-2099-42a4-ba63-6677024e5e92",
    "investors/logo.png": "https://www.figma.com/api/mcp/asset/20f8e2d5-afa8-438d-ac96-db264ea1798f",
    "investors/kr1.png": "https://www.figma.com/api/mcp/asset/d67cfff1-4fc1-4e67-bc13-55dbe7b6328b",
    "investors/mirana.png": "https://www.figma.com/api/mcp/asset/5e591850-e297-4dba-b768-9bdf13650574",
    "investors/altos-ventures.png": "https://www.figma.com/api/mcp/asset/8ae7b5c2-aeea-4863-bbc5-9cdf733f3368",
    "investors/hashkey-capital.png": "https://www.figma.com/api/mcp/asset/f2330a65-6b8e-4d5d-9fed-4fc8d8de2f4a",
    "investors/foresight-ventures.png": "https://www.figma.com/api/mcp/asset/0cf7b959-8c2a-447c-83a1-d0ba1ef8168d",
    "investors/superscrypt.png": "https://www.figma.com/api/mcp/asset/d2cd363f-1e81-43db-ae68-21f71caabef4",
    "investors/alliance.png": "https://www.figma.com/api/mcp/asset/15c8309e-f372-4eb8-81a8-5d314b0d2a11",
    "investors/chapter-one.png": "https://www.figma.com/api/mcp/asset/0a63765e-2e12-4bc3-8872-e9e2fe10f048",
    "investors/cyber-fund.png": "https://www.figma.com/api/mcp/asset/bb5da44d-ebf3-4a83-93a0-dcbb7574e796",
    "investors/figment-capital.png": "https://www.figma.com/api/mcp/asset/687248ff-a7ef-491a-9941-6b58432f30d2",
    "investors/dragonfly.png": "https://www.figma.com/api/mcp/asset/2dfbdc67-c19b-4288-b259-6fb6070c97bf",
    "investors/nomad-capital.png": "https://www.figma.com/api/mcp/asset/c77bcc7d-6928-4c71-875f-df715780a897",
    "investors/seven-x-ventures.png": "https://www.figma.com/api/mcp/asset/ea4bc15a-514d-44bc-9e80-f9f4498bff9a",
    "investors/founders-fund.png": "https://www.figma.com/api/mcp/asset/e9244996-97f6-4b37-a5d4-d711947ec0b4",
}


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def load_team_urls() -> dict[str, str]:
    if not DC_FILE.exists():
        return {}
    text = DC_FILE.read_text()
    urls = dict(re.findall(r'const (img\w+) = "(https://[^"]+)";', text))
    by_image: dict[str, str] = {}
    for key, url in urls.items():
        by_image[norm(key.replace("img", ""))] = url

    team = json.loads((ROOT / "team.json").read_text())
    mapping: dict[str, str] = {}
    for person in team["founders"] + team["team"]:
        image = person.get("image")
        if not image:
            continue
        frag = norm(Path(image).stem)
        url = by_image.get(frag + "png") or by_image.get(frag)
        if not url:
            for k, v in by_image.items():
                if k.startswith(frag) or frag in k:
                    url = v
                    break
        if url:
            mapping[person["slug"]] = url
    return mapping


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, context=ctx, timeout=120) as resp:
        dest.write_bytes(resp.read())


def main() -> None:
    team_urls = load_team_urls()
    for slug, url in team_urls.items():
        dest = ASSETS / "team" / f"{slug}.png"
        if dest.exists() and dest.stat().st_size > 500:
            continue
        print(f"Downloading team/{slug}.png")
        download(url, dest)

    for rel, url in STATIC_URLS.items():
        dest = ASSETS / rel
        if dest.exists() and dest.stat().st_size > 100:
            continue
        print(f"Downloading {rel}")
        download(url, dest)
    print("Done.")


if __name__ == "__main__":
    main()
