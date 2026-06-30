#!/usr/bin/env python3
"""Generate about-us/index.html from team.json."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SOCIAL_ICONS = {
    "twitter": ("social/twitter.svg", "X"),
    "linkedin": ("social/linkedin.svg", "LinkedIn"),
    "github": ("social/github.svg", "GitHub"),
}

INVESTORS = [
    ("longhash-ventures", "LongHash Ventures"),
    ("rw3", "RW3"),
    ("logo", "Investor"),
    ("kr1", "KR1"),
    ("mirana", "Mirana"),
    ("altos-ventures", "Altos Ventures"),
    ("hashkey-capital", "HashKey Capital"),
    ("foresight-ventures", "Foresight Ventures"),
    ("superscrypt", "Superscrypt"),
    ("alliance", "Alliance"),
    ("chapter-one", "Chapter One"),
    ("cyber-fund", "Cyber Fund"),
    ("figment-capital", "Figment Capital"),
    ("dragonfly", "DragonFly"),
    ("nomad-capital", "Nomad Capital"),
    ("seven-x-ventures", "Seven X Ventures"),
    ("founders-fund", "Founders Fund"),
]

NAV_HTML = """  <header class="nav-header">
    <a href="#" class="nav-logo" aria-label="Avail home">
      <img src="../assets/logo-mark.svg" alt="" class="nav-logo__mark" width="30" height="30">
      <img src="../assets/logo-wordmark.svg" alt="avail" class="nav-logo__wordmark" width="57" height="21">
    </a>

    <div class="nav-pill">
      <nav class="nav-links" aria-label="Primary">
        <a href="#" class="nav-links__item">Solutions</a>
        <a href="#" class="nav-links__item">Products</a>
        <a href="../ecosystem/" class="nav-links__item">Ecosystem</a>
        <a href="#" class="nav-links__item">Docs</a>
        <a href="#" class="nav-links__item">Blog</a>
      </nav>

      <button type="button" class="nav-menu" aria-expanded="false" aria-controls="mobile-menu" aria-label="Open menu">
        <span class="nav-menu__icon" aria-hidden="true"></span>
        <span class="nav-menu__label">Menu</span>
      </button>

      <a href="#" class="btn btn-primary nav-header__cta">Build with Avail</a>
    </div>
  </header>

  <div class="mobile-menu" id="mobile-menu" hidden>
    <nav class="mobile-menu__nav" aria-label="Mobile">
      <a href="#" class="mobile-menu__link">Solutions</a>
      <a href="#" class="mobile-menu__link">Products</a>
      <a href="../ecosystem/" class="mobile-menu__link">Ecosystem</a>
      <a href="#" class="mobile-menu__link">Docs</a>
      <a href="#" class="mobile-menu__link">Blog</a>
      <a href="#" class="btn btn-primary mobile-menu__cta">Build with Avail</a>
    </nav>
  </div>"""

FOOTER_HTML = """  <footer class="site-footer" aria-label="Footer">
    <div class="site-footer__inner">
      <div class="site-footer__top">
        <div class="site-footer__cta">
          <h2 class="site-footer__headline">Have questions?</h2>
          <p class="site-footer__subcopy">Get in touch with us and understand exactly what we do</p>
          <a href="#" class="btn btn-primary site-footer__btn">Schedule A Demo</a>
          <p class="site-footer__copyright">Copyright © Avail Project. All rights reserved.</p>
        </div>

        <nav class="site-footer__nav" aria-label="Footer navigation">
          <div class="site-footer__nav-group site-footer__nav-group--pages">
            <div class="site-footer__nav-columns">
              <div class="site-footer__nav-subgroup">
                <p class="site-footer__nav-heading">Pages</p>
                <ul class="site-footer__nav-list">
                <li><a href="#" class="site-footer__nav-link">Home</a></li>
                <li><a href="#" class="site-footer__nav-link" aria-current="page">About us</a></li>
                <li><a href="../nexus/" class="site-footer__nav-link">Nexus</a></li>
                <li><a href="../da/" class="site-footer__nav-link">DA</a></li>
                <li><a href="#" class="site-footer__nav-link">Careers</a></li>
              </ul>
              </div>
              <ul class="site-footer__nav-list site-footer__nav-list--pages-right">
                <li><a href="#" class="site-footer__nav-link">Blog</a></li>
                <li><a href="../ecosystem/" class="site-footer__nav-link">Ecosystem</a></li>
                <li><a href="#" class="site-footer__nav-link">T&amp;C</a></li>
                <li><a href="#" class="site-footer__nav-link">Whitepaper</a></li>
              </ul>
            </div>
          </div>

          <div class="site-footer__nav-group site-footer__nav-group--support-press">
            <div class="site-footer__nav-subgroup">
              <p class="site-footer__nav-heading">Support</p>
              <ul class="site-footer__nav-list">
                <li><a href="#" class="site-footer__nav-link">Docs</a></li>
                <li><a href="#" class="site-footer__nav-link">Discord</a></li>
                <li><a href="#" class="site-footer__nav-link">GitHub</a></li>
              </ul>
            </div>
            <div class="site-footer__nav-subgroup">
              <p class="site-footer__nav-heading">Press Kit</p>
              <ul class="site-footer__nav-list">
                <li><a href="#" class="site-footer__nav-link">Brand Assets</a></li>
              </ul>
            </div>
          </div>

          <div class="site-footer__nav-group site-footer__nav-group--socials">
            <p class="site-footer__nav-heading">Socials</p>
            <ul class="site-footer__nav-list">
              <li><a href="#" class="site-footer__nav-link">X (Twitter)</a></li>
              <li><a href="#" class="site-footer__nav-link">LinkedIn</a></li>
              <li><a href="#" class="site-footer__nav-link">Telegram</a></li>
              <li><a href="#" class="site-footer__nav-link">YouTube</a></li>
            </ul>
          </div>
        </nav>
      </div>

      <div class="site-footer__logo" aria-hidden="true">
        <img src="../assets/footer/avail-wordmark.png" alt="" class="site-footer__logo-img" width="832" height="203" loading="lazy" decoding="async">
      </div>
    </div>
  </footer>"""


def socials_html(socials: list[str]) -> str:
    if not socials:
        return ""
    items = []
    for s in socials:
        if s not in SOCIAL_ICONS:
            continue
        icon, label = SOCIAL_ICONS[s]
        items.append(
            f'<a href="#" class="person-card__social" aria-label="{label}">'
            f'<img src="assets/{icon}" alt="" width="24" height="24" /></a>'
        )
    return f'<div class="person-card__socials">{"".join(items)}</div>'


def founder_card(person: dict) -> str:
    return f"""            <article class="person-card person-card--founder">
              <div class="person-card__photo">
                <img src="assets/team/{person['slug']}.png" alt="{person['name']}" loading="lazy" decoding="async" />
              </div>
              {socials_html(person.get('socials', []))}
              <div class="person-card__info">
                <h3 class="person-card__name">{person['name']}</h3>
                <p class="person-card__title">{person['title']}</p>
              </div>
            </article>"""


def team_card(person: dict) -> str:
    name_parts = person["name"].split(" ", 1)
    if len(name_parts) == 2:
        name_html = f'<span class="person-card__name-line">{name_parts[0]}</span><span class="person-card__name-line">{name_parts[1]}</span>'
    else:
        name_html = f'<span class="person-card__name-line">{person["name"]}</span>'
    return f"""            <article class="person-card person-card--team">
              <div class="person-card__photo">
                <img src="assets/team/{person['slug']}.png" alt="{person['name']}" loading="lazy" decoding="async" />
              </div>
              {socials_html(person.get('socials', []))}
              <div class="person-card__info">
                <h3 class="person-card__name">{name_html}</h3>
                <p class="person-card__title">{person['title']}</p>
              </div>
            </article>"""


def investors_marquee() -> str:
    items = []
    for slug, name in INVESTORS * 2:
        items.append(
            f'<span class="marquee__item investors__item">'
            f'<img src="assets/investors/{slug}.png" alt="{name}" loading="lazy" decoding="async" />'
            f"</span>"
        )
    return "\n".join(items)


def main() -> None:
    data = json.loads((ROOT / "team.json").read_text())
    founders = "\n".join(founder_card(p) for p in data["founders"])
    team = "\n".join(team_card(p) for p in data["team"])
    investors = investors_marquee()

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>About Us — Avail</title>
  <meta name="description" content="Meet the Avail team building the future of modular blockchain infrastructure." />
  <link rel="icon" type="image/png" href="../assets/logo-mark.svg" />
  <link rel="stylesheet" href="style.css" />
</head>
<body>
  <div class="page-shell">
    <div class="page-bg" aria-hidden="true">
      <canvas class="page-bg__canvas"></canvas>
    </div>

{NAV_HTML}

    <main>
      <section class="hero hero--about">
        <div class="wrap hero--about__inner">
          <h1 class="hero--about__title">About Us</h1>
          <p class="hero--about__text">Avail started as a research project inside Polygon, born from the recognition that blockchain ecosystems needed scalability. We started Avail with this vision. We believe it must be delivered with the utmost speed, accessibility, and performant freedom for applications to scale and provide users unfettered access.</p>
        </div>
      </section>

      <section class="team-panel">
        <div class="wrap">
          <div class="team-panel__section">
            <h2 class="team-panel__heading">Founders</h2>
            <div class="founders-grid">
{founders}
            </div>
          </div>
          <div class="team-panel__section">
            <h2 class="team-panel__heading">Team</h2>
            <div class="team-grid">
{team}
            </div>
          </div>
        </div>
      </section>

      <section class="values">
        <div class="wrap values__inner">
          <h2 class="section-title">Values &amp; Philosophy</h2>
          <p class="values__text">At Avail, our culture is built on accountability, curiosity, and ambition. We empower our team to take ownership, challenge assumptions, and embrace open debate because better ideas emerge when every voice is heard. We put culture before credentials, valuing people who strengthen our team for the long run. By thinking big and staying grounded in real-world usage, we build with vision while learning continuously through experimentation. This is how we work together: humble, ambitious, and always looking ahead.</p>
        </div>
      </section>

      <section class="backed-by">
        <div class="wrap">
          <h2 class="section-title">Backed By</h2>
          <div class="marquee investors-marquee" style="--speed: 55s">
            <div class="marquee__track">
{investors}
            </div>
          </div>
        </div>
      </section>

      <section class="life-at-avail">
        <div class="wrap life-at-avail__inner">
          <div class="life-at-avail__media">
            <img src="assets/life-at-avail.jpg" alt="" loading="lazy" decoding="async" />
          </div>
          <div class="life-at-avail__copy">
            <h2 class="life-at-avail__title">Life at Avail</h2>
            <p class="life-at-avail__text">We are a remote-first company with the team residing across multiple locations and geographies. We empower our teams to take control of their work schedules and ownership of their passion projects. Skill expansion, fostering continuous personal and professional growth, is key to life at Avail.</p>
            <p class="life-at-avail__text">Join us from anywhere in the world to help build the future multichain world.</p>
            <a href="#" class="btn btn-primary life-at-avail__cta">View Careers</a>
          </div>
        </div>
      </section>
    </main>

{FOOTER_HTML}
  </div>

  <script src="../halftone-background.js?v=2"></script>
  <script>
    (function () {{
      var toggle = document.querySelector('.nav-menu');
      var menu = document.getElementById('mobile-menu');
      if (toggle && menu) {{
        toggle.addEventListener('click', function () {{
          var isOpen = toggle.getAttribute('aria-expanded') === 'true';
          toggle.setAttribute('aria-expanded', String(!isOpen));
          toggle.setAttribute('aria-label', isOpen ? 'Open menu' : 'Close menu');
          menu.hidden = isOpen;
          document.body.classList.toggle('menu-open', !isOpen);
        }});
      }}
    }})();
  </script>
</body>
</html>
"""
    (ROOT / "index.html").write_text(html)
    print("Wrote index.html")


if __name__ == "__main__":
    main()
