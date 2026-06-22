"""Site-wide link targets for avail-deposit (mirrors availproject.org structure)."""

from __future__ import annotations

import os
from pathlib import PurePosixPath

# Internal page folder names (empty string = deposits landing at site root)
INTERNAL_PAGES = {
    "home": "",  # deposits page at /
    "deposits": "",
    "nexus": "nexus",
    "da": "da",
    "ecosystem": "ecosystem",
    "events": "events",
    "about": "about-us",
    "terms": "terms",
    "whitepaper": "whitepaper",
}

EXTERNAL = {
    "site_home": "../avail-website/",
    "deposit_site": "../avail-deposit",
    "docs": "https://docs.availproject.org/",
    "docs_nexus": "https://docs.availproject.org/docs/nexus/quickstart",
    "docs_deposit": "https://docs.availproject.org/docs/nexus/nexus-ui-elements/components/deposit",
    "blog": "https://blog.availproject.org/",
    "careers": "https://avail.keka.com/careers",
    "contact": "https://availproject.org/contact",
    "discord": "https://discord.com/invite/AvailProject",
    "github": "https://github.com/availproject",
    "brand": "https://availproject.org/brand",
    "calendly": "https://calendly.com/d/cwfp-t3y-gt2/avail-discovery-call",
    "deposit_demo": "https://nexus-deposit.availproject.org/",
    "fastbridge": "https://fastbridge.availproject.org/",
    "atomic": "https://docs.availproject.org/",
    "ai_skills": "https://docs.availproject.org/docs/nexus/nexus-ui-elements/skills/nexus-elements-deposit",
    "twitter": "https://x.com/AvailProject",
    "linkedin": "https://www.linkedin.com/company/availproject/",
    "telegram": "https://t.me/availproject",
    "youtube": "https://www.youtube.com/@AvailProject",
    "privacy": "https://avail-project.notion.site/Privacy-Policy-e5f47df2f3a64055a7966bbaabe9a2eb",
    "token": "https://availproject.org/token",
}


def internal(from_page: str, to_key: str) -> str:
    """Relative href from one page folder to another."""
    to_folder = INTERNAL_PAGES[to_key]
    fr = from_page or "."
    to = to_folder or "."
    rel = os.path.relpath(to, fr)
    rel = PurePosixPath(rel).as_posix()
    if to_folder:
        return rel + ("" if rel.endswith("/") else "/")
    if rel in (".", ""):
        return "./"
    return rel + ("" if rel.endswith("/") else "/")


def marketing_home(from_page: str) -> str:
    """Relative path from an avail-deposit page to the marketing homepage."""
    depth = 1 if not from_page else 2
    return "../" * depth + "avail-website/"


def external(key: str) -> str:
    return EXTERNAL[key]


def deposit_page(path: str = "") -> str:
    """Absolute URL to a page on the deposit site (localhost:8848)."""
    base = EXTERNAL["deposit_site"].rstrip("/")
    if not path:
        return f"{base}/"
    return f"{base}/{path.strip('/')}/"
