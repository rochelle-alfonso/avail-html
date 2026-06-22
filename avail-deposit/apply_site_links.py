#!/usr/bin/env python3
"""Apply site-wide navigation links to all index.html pages."""

from __future__ import annotations

import re
from pathlib import Path

from site_urls import external, internal, marketing_home

ROOT = Path(__file__).resolve().parent
PAGES = [
    ROOT / "index.html",
    ROOT / "nexus" / "index.html",
    ROOT / "da" / "index.html",
    ROOT / "ecosystem" / "index.html",
    ROOT / "events" / "index.html",
    ROOT / "about-us" / "index.html",
    ROOT / "terms" / "index.html",
    ROOT / "whitepaper" / "index.html",
]


def page_key(path: Path) -> str:
    if path.parent == ROOT:
        return ""
    return path.parent.name


def set_href(html: str, pattern: str, href: str) -> str:
    return re.sub(pattern, rf'href="{href}"', html, count=1)


def patch_nav_and_footer(html: str, pg: str) -> str:
    d = lambda k: internal(pg, k)
    e = external
    home = marketing_home(pg)

    # Logo → marketing homepage
    html = re.sub(
        r'(<a )href="[^"]*"(\s+class="nav-logo")',
        rf'\1href="{home}"\2',
        html,
        count=1,
    )

    # Shared nav / mobile / dropdown internals
    replacements = [
        (r'(<a href=")[^"]*(" class="nav-dropdown__link" role="menuitem">User Onboarding)', rf'\1{d("deposits")}\2'),
        (r'(<a href=")[^"]*(" class="nav-dropdown__link" role="menuitem">Multi-Chain Solutions)', rf'\1{d("nexus")}\2'),
        (r'(<a href=")[^"]*(" class="nav-dropdown__link" role="menuitem">Data Availability)', rf'\1{d("da")}\2'),
        (r'(<a href=")[^"]*(" class="nav-dropdown__link" role="menuitem"[^>]*>Avail FastBridge)', rf'\1{e("fastbridge")}\2'),
        (r'(<a href=")[^"]*(" class="nav-dropdown__link" role="menuitem">Avail Deposits)', rf'\1{d("deposits")}\2'),
        (r'(<a href=")[^"]*(" class="nav-dropdown__link" role="menuitem">Avail Nexus)', rf'\1{d("nexus")}\2'),
        (r'(<a href=")[^"]*(" class="nav-dropdown__link" role="menuitem">Avail DA)', rf'\1{d("da")}\2'),
        (r'(<a href=")[^"]*(" class="nav-dropdown__link" role="menuitem">Avail Atomic)', rf'\1{e("atomic")}\2'),
        (r'(<a href=")[^"]*(" class="nav-links__item">Ecosystem)', rf'\1{d("ecosystem")}\2'),
        (r'(<a href=")[^"]*(" class="nav-links__item">Docs)', rf'\1{e("docs")}\2'),
        (r'(<a href=")[^"]*(" class="nav-links__item">Blog)', rf'\1{e("blog")}\2'),
        (r'(<a href=")[^"]*(" class="mobile-menu__sublink">User Onboarding)', rf'\1{d("deposits")}\2'),
        (r'(<a href=")[^"]*(" class="mobile-menu__sublink">Multi-Chain Solutions)', rf'\1{d("nexus")}\2'),
        (r'(<a href=")[^"]*(" class="mobile-menu__sublink">Data Availability)', rf'\1{d("da")}\2'),
        (r'(<a href=")[^"]*(" class="mobile-menu__sublink"[^>]*>Avail FastBridge)', rf'\1{e("fastbridge")}\2'),
        (r'(<a href=")[^"]*(" class="mobile-menu__sublink">Avail Deposits)', rf'\1{d("deposits")}\2'),
        (r'(<a href=")[^"]*(" class="mobile-menu__sublink">Avail Nexus)', rf'\1{d("nexus")}\2'),
        (r'(<a href=")[^"]*(" class="mobile-menu__sublink">Avail DA)', rf'\1{d("da")}\2'),
        (r'(<a href=")[^"]*(" class="mobile-menu__sublink">Avail Atomic)', rf'\1{e("atomic")}\2'),
        (r'(<a href=")[^"]*(" class="mobile-menu__link">Ecosystem)', rf'\1{d("ecosystem")}\2'),
        (r'(<a href=")[^"]*(" class="mobile-menu__link">Docs)', rf'\1{e("docs")}\2'),
        (r'(<a href=")[^"]*(" class="mobile-menu__link">Blog)', rf'\1{e("blog")}\2'),
        (r'(<a href=")[^"]*(" class="btn btn-primary nav-header__cta">Build with Avail)', rf'\1{e("docs_nexus")}\2'),
        (r'(<a href=")[^"]*(" class="btn btn-primary mobile-menu__cta">Build with Avail)', rf'\1{e("docs_nexus")}\2'),
        (r'(<a href=")[^"]*(" class="btn btn-primary site-footer__btn">Schedule A Demo)', rf'\1{e("calendly")}\2'),
        (r'(<a href=")[^"]*(" class="site-footer__nav-link">Home)', rf'\1{home}\2'),
        (r'(<a href=")[^"]*(" class="site-footer__nav-link"[^>]*>Home)', rf'\1{home}\2'),
        (r'(<a href=")[^"]*(" class="site-footer__nav-link">About us)', rf'\1{d("about")}\2'),
        (r'(<a href=")[^"]*(" class="site-footer__nav-link">Nexus)', rf'\1{d("nexus")}\2'),
        (r'(<a href=")[^"]*(" class="site-footer__nav-link">DA)', rf'\1{d("da")}\2'),
        (r'(<a href=")[^"]*(" class="site-footer__nav-link">Careers)', rf'\1{e("careers")}\2'),
        (r'(<a href=")[^"]*(" class="site-footer__nav-link">Blog)', rf'\1{e("blog")}\2'),
        (r'(<a href=")[^"]*(" class="site-footer__nav-link">Ecosystem)', rf'\1{d("ecosystem")}\2'),
        (r'(<a href=")[^"]*(" class="site-footer__nav-link">T&amp;C)', rf'\1{d("terms")}\2'),
        (r'(<a href=")[^"]*(" class="site-footer__nav-link">Whitepaper)', rf'\1{d("whitepaper")}\2'),
        (r'(<a href=")[^"]*(" class="site-footer__nav-link">Docs)', rf'\1{e("docs")}\2'),
        (r'(<a href=")[^"]*(" class="site-footer__nav-link">Discord)', rf'\1{e("discord")}\2'),
        (r'(<a href=")[^"]*(" class="site-footer__nav-link">GitHub)', rf'\1{e("github")}\2'),
        (r'(<a href=")[^"]*(" class="site-footer__nav-link">Brand Assets)', rf'\1{e("brand")}\2'),
        (r'(<a href=")[^"]*(" class="site-footer__nav-link">X \(Twitter\))', rf'\1{e("twitter")}\2'),
        (r'(<a href=")[^"]*(" class="site-footer__nav-link">LinkedIn)', rf'\1{e("linkedin")}\2'),
        (r'(<a href=")[^"]*(" class="site-footer__nav-link">Telegram)', rf'\1{e("telegram")}\2'),
        (r'(<a href=")[^"]*(" class="site-footer__nav-link">YouTube)', rf'\1{e("youtube")}\2'),
    ]

    for pattern, repl in replacements:
        html = re.sub(pattern, repl, html)

    # Footer Events link (matches availproject.org footer nav)
    if 'class="site-footer__nav-link">Events' not in html:
        html = re.sub(
            r'(<li><a href="[^"]*" class="site-footer__nav-link">Ecosystem</a></li>\n)',
            rf'\1                <li><a href="{d("events")}" class="site-footer__nav-link">Events</a></li>\n',
            html,
            count=1,
        )
    else:
        html = re.sub(
            r'(<a href=")[^"]*(" class="site-footer__nav-link">Events)',
            rf'\1{d("events")}\2',
            html,
        )

    # Events page home link
    html = re.sub(
        r'(<a href=")[^"]*(" class="nav-links__item">Home)',
        rf'\1{home}\2',
        html,
        count=1,
    )
    html = re.sub(
        r'(<a href=")[^"]*(" class="mobile-menu__link">Home)',
        rf'\1{home}\2',
        html,
        count=1,
    )

    return html


def patch_page_ctas(html: str, pg: str) -> str:
    d = lambda k: internal(pg, k)
    e = external

    if pg == "":
        html = re.sub(r'(<a href=")[^"]*(" class="btn btn-primary">Book Evaluation Call)', rf'\1{e("calendly")}\2', html)
        html = re.sub(r'(<a href=")[^"]*(" class="btn btn-secondary">See it in Action)', rf'\1{e("deposit_demo")}\2', html)
        html = re.sub(r'(<a href=")[^"]*(" class="btn btn-secondary btn-sm">Add Deposits)', rf'\1{e("docs_deposit")}\2', html)
        html = re.sub(r'(<a href=")[^"]*(" class="btn btn-secondary btn-sm">Get in Touch)', rf'\1{e("calendly")}\2', html)
        html = re.sub(r'(<a href=")[^"]*(" class="btn btn-secondary btn-sm">Explore AI Skills)', rf'\1{e("ai_skills")}\2', html)

    if pg == "nexus":
        html = re.sub(r'(<a href=")[^"]*(" class="btn btn-primary">Explore the Docs)', rf'\1{e("docs_nexus")}\2', html)
        html = re.sub(r'(<a href=")[^"]*(" class="btn btn-secondary">Schedule a Demo)', rf'\1{e("calendly")}\2', html)
        html = re.sub(r'(<a href=")[^"]*(" class="btn btn-secondary">Learn More)', rf'\1{e("docs_nexus")}\2', html)
        html = re.sub(r'(<a href=")[^"]*(" class="btn btn-secondary">Avail Deposits)', rf'\1{d("deposits")}\2', html)
        html = re.sub(r'(<a href=")[^"]*(" class="btn btn-primary"[^>]*>Bridge Now)', rf'\1{e("fastbridge")}\2', html)
        html = re.sub(r'(<a href=")[^"]*(" class="btn btn-primary">Read Documentation)', rf'\1{e("docs_nexus")}\2', html)
        html = re.sub(r'(<a href=")[^"]*(" class="btn btn-secondary">Contact Us)', rf'\1{e("contact")}\2', html)

    if pg == "da":
        html = re.sub(r'(<a href=")[^"]*(" class="btn btn-primary">Build With Avail)', rf'\1{e("docs")}\2', html)
        html = re.sub(r'(<a href=")[^"]*(" class="btn btn-secondary">Talk to Us)', rf'\1{e("contact")}\2', html)

    if pg == "ecosystem":
        html = re.sub(r'(<a href=")[^"]*(" class="btn btn-primary btn-sm">Build With Us)', rf'\1{e("contact")}\2', html)
        html = re.sub(r'(<a href=")[^"]*(" class="featured-card")', rf'\1{d("nexus")}\2', html, count=3)
        html = re.sub(r'(<a href=")[^"]*(" class="blog-card__media")', rf'\1{e("blog")}\2', html)
        html = re.sub(r'(<a href=")[^"]*(">Avail Empowers TRON)', rf'\1{e("blog")}\2', html)
        html = re.sub(r'(<a href=")[^"]*(">Avail Expands to Monad)', rf'\1{e("blog")}\2', html)
        html = re.sub(r'(<a href=")[^"]*(">How Clober Unlocked)', rf'\1{e("blog")}\2', html)

    if pg == "about-us":
        html = re.sub(r'(<a href=")[^"]*(" class="btn btn-primary life-at-avail__cta">View Careers)', rf'\1{e("careers")}\2', html)
        html = re.sub(
            r'(<a href=")[^"]*(" class="person-card__social" aria-label="X">)',
            rf'\1{e("twitter")}\2',
            html,
        )
        html = re.sub(
            r'(<a href=")[^"]*(" class="person-card__social" aria-label="LinkedIn">)',
            rf'\1{e("linkedin")}\2',
            html,
        )
        html = re.sub(
            r'(<a href=")[^"]*(" class="person-card__social" aria-label="GitHub">)',
            rf'\1{e("github")}\2',
            html,
        )

    if pg == "events":
        html = patch_events_footer(html, pg)

    return html


def patch_events_footer(html: str, pg: str) -> str:
    d = lambda k: internal(pg, k)
    e = external
    home = marketing_home(pg)

    events_links = [
        (r'(<a href=")[^"]*(">Home</a>)', rf'\1{home}\2'),
        (r'(<a href=")[^"]*(">Nexus</a>)', rf'\1{d("nexus")}\2'),
        (r'(<a href=")[^"]*(">DA</a>)', rf'\1{d("da")}\2'),
        (r'(<a href=")[^"]*(">Token</a>)', rf'\1{e("token")}\2'),
        (r'(<a href=")[^"]*(">About Us</a>)', rf'\1{d("about")}\2'),
        (r'(<a href=")[^"]*(">Blog</a>)', rf'\1{e("blog")}\2'),
        (r'(<a href=")[^"]*(">Docs</a>)', rf'\1{e("docs")}\2'),
        (r'(<a href=")[^"]*(">Whitepaper</a>)', rf'\1{d("whitepaper")}\2'),
        (r'(<a href=")[^"]*(">Careers</a>)', rf'\1{e("careers")}\2'),
        (r'(<a href=")[^"]*(">Privacy Policy</a>)', rf'\1{e("privacy")}\2'),
        (r'(<a href=")[^"]*(">T &amp; C</a>)', rf'\1{d("terms")}\2'),
        (r'(<a href=")[^"]*(">Discord</a>)', rf'\1{e("discord")}\2'),
        (r'(<a href=")[^"]*(">Github</a>)', rf'\1{e("github")}\2'),
        (r'(<a href=")[^"]*(">Brand Assets</a>)', rf'\1{e("brand")}\2'),
        (r'(<a href=")[^"]*(" class="events-footer__demo-btn">Pick a Time Slot)', rf'\1{e("calendly")}\2'),
        (r'(<a href=")[^"]*(" aria-label="X"><img src="assets/footer/social-x.svg")', rf'\1{e("twitter")}\2'),
        (r'(<a href=")[^"]*(" aria-label="Telegram"><img src="assets/footer/social-telegram.svg")', rf'\1{e("telegram")}\2'),
        (r'(<a href=")[^"]*(" aria-label="LinkedIn"><img src="assets/footer/social-linkedin.svg")', rf'\1{e("linkedin")}\2'),
        (r'(<a href=")[^"]*(" aria-label="YouTube"><img src="assets/footer/social-youtube.svg")', rf'\1{e("youtube")}\2'),
    ]
    for pattern, repl in events_links:
        html = re.sub(pattern, repl, html)

    return html


def patch_current_page_links(html: str, pg: str) -> str:
    if pg == "terms":
        html = re.sub(
            r'(<a href=")[^"]*(" class="site-footer__nav-link" aria-current="page">T&amp;C)',
            r'\1./\2',
            html,
            count=1,
        )
    if pg == "about-us":
        html = re.sub(
            r'(<a href=")[^"]*(" class="site-footer__nav-link" aria-current="page">About us)',
            r'\1./\2',
            html,
            count=1,
        )
    if pg == "events":
        html = re.sub(
            r'(<a href=")[^"]*(" aria-current="page">Events</a>)',
            r'\1./\2',
            html,
            count=1,
        )
        html = re.sub(
            r'(<a href=")[^"]*(" class="site-footer__nav-link" aria-current="page">Events)',
            r'\1./\2',
            html,
            count=1,
        )
    return html


def is_internal_navigation(href: str) -> bool:
    """Relative paths and local dev servers — navigate in the same tab."""
    if href.startswith(("#", "/", "./", "../")):
        return True
    return bool(re.match(r"https?://(localhost|127\.0\.0\.1)(:\d+)?", href))


def strip_internal_new_tab(html: str) -> str:
    """Remove target=_blank from same-site navigation links."""

    def repl(match: re.Match[str]) -> str:
        tag = match.group(0)
        href = match.group(1)
        if not is_internal_navigation(href):
            return tag
        tag = re.sub(r'\s*target="_blank"', "", tag)
        tag = re.sub(r'\s*rel="noopener noreferrer"', "", tag)
        return tag

    return re.sub(r'<a href="([^"]+)"[^>]*>', repl, html)


def add_external_attrs(html: str) -> str:
    """Open external links in a new tab (not same-site pages)."""

    def repl(match: re.Match[str]) -> str:
        tag = match.group(0)
        href = match.group(1)
        if is_internal_navigation(href):
            return tag
        if href.startswith(("http://", "https://")) and "target=" not in tag:
            if tag.endswith(">"):
                return tag[:-1] + ' target="_blank" rel="noopener noreferrer">'
        return tag

    return re.sub(r'<a href="(https?://[^"]+)"[^>]*>', repl, html)


def main() -> None:
    for path in PAGES:
        pg = page_key(path)
        html = path.read_text()
        html = patch_nav_and_footer(html, pg)
        html = patch_page_ctas(html, pg)
        html = patch_current_page_links(html, pg)
        html = add_external_attrs(html)
        html = strip_internal_new_tab(html)
        path.write_text(html)
        remaining = html.count('href="#"')
        print(f"{path.relative_to(ROOT)}: updated ({remaining} placeholder links left)")


if __name__ == "__main__":
    main()
