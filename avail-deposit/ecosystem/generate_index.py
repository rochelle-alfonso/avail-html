#!/usr/bin/env python3
"""Generate ecosystem/index.html from partners.json and static section templates."""

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


def partners_grid(partners: list) -> str:
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
    partners = json.loads((ROOT / "partners.json").read_text())
    grid = partners_grid(partners)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Ecosystem — Avail</title>
  <meta name="description" content="Discover the growing network of chains, applications, and infrastructure building with Avail." />
  <link rel="icon" type="image/png" href="../assets/logo-mark.svg" />
  <link rel="stylesheet" href="style.css" />
  <link rel="stylesheet" href="../nav.css" />
</head>
<body>
  <div class="page-shell">
    <div class="page-bg" aria-hidden="true">
      <canvas class="page-bg__canvas"></canvas>
    </div>

  <header class="nav-header">
    <a href="#" class="nav-logo" aria-label="Avail home">
      <img src="../assets/logo-mark.svg" alt="" class="nav-logo__mark" width="30" height="30">
      <img src="../assets/logo-wordmark.svg" alt="avail" class="nav-logo__wordmark" width="57" height="21">
    </a>

    <div class="nav-pill">
      <nav class="nav-links" aria-label="Primary">
        <div class="nav-dropdown">
          <button type="button" class="nav-links__trigger" aria-haspopup="true" aria-expanded="false" id="nav-solutions-trigger" aria-controls="nav-solutions-menu">Solutions</button>
          <div class="nav-dropdown__menu" id="nav-solutions-menu" role="menu" aria-labelledby="nav-solutions-trigger">
            <div class="nav-dropdown__section">
              <p class="nav-dropdown__heading">App Developers</p>
              <a href="#" class="nav-dropdown__link" role="menuitem">User Onboarding</a>
              <a href="#" class="nav-dropdown__link" role="menuitem">Multi-Chain Solutions</a>
            </div>
            <div class="nav-dropdown__section">
              <p class="nav-dropdown__heading">Blockchain Developers</p>
              <a href="#" class="nav-dropdown__link" role="menuitem">Data Availability</a>
            </div>
          </div>
        </div>
        <div class="nav-dropdown">
          <button type="button" class="nav-links__trigger" aria-haspopup="true" aria-expanded="false" id="nav-products-trigger" aria-controls="nav-products-menu">Products</button>
          <div class="nav-dropdown__menu nav-dropdown__menu--products" id="nav-products-menu" role="menu" aria-labelledby="nav-products-trigger">
            <a href="#" class="nav-dropdown__link" role="menuitem">Avail FastBridge</a>
            <a href="#" class="nav-dropdown__link" role="menuitem">Avail Deposits</a>
            <a href="#" class="nav-dropdown__link" role="menuitem">Avail Nexus</a>
            <a href="#" class="nav-dropdown__link" role="menuitem">Avail DA</a>
            <a href="#" class="nav-dropdown__link" role="menuitem">Avail Atomic</a>
          </div>
        </div>
        <a href="#" class="nav-links__item nav-links__item--active">Ecosystem</a>
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
      <details class="mobile-menu__details">
        <summary class="mobile-menu__link">Solutions</summary>
        <div class="mobile-menu__sub">
          <p class="mobile-menu__heading">App Developers</p>
          <a href="#" class="mobile-menu__sublink">User Onboarding</a>
          <a href="#" class="mobile-menu__sublink">Multi-Chain Solutions</a>
          <p class="mobile-menu__heading">Blockchain Developers</p>
          <a href="#" class="mobile-menu__sublink">Data Availability</a>
        </div>
      </details>
      <details class="mobile-menu__details">
        <summary class="mobile-menu__link">Products</summary>
        <div class="mobile-menu__sub">
          <a href="#" class="mobile-menu__sublink">Avail FastBridge</a>
          <a href="#" class="mobile-menu__sublink">Avail Deposits</a>
          <a href="#" class="mobile-menu__sublink">Avail Nexus</a>
          <a href="#" class="mobile-menu__sublink">Avail DA</a>
          <a href="#" class="mobile-menu__sublink">Avail Atomic</a>
        </div>
      </details>
      <a href="#" class="mobile-menu__link">Ecosystem</a>
      <a href="#" class="mobile-menu__link">Docs</a>
      <a href="#" class="mobile-menu__link">Blog</a>
      <a href="#" class="btn btn-primary mobile-menu__cta">Build with Avail</a>
    </nav>
  </div>

  <main>
    <section class="hero hero--ecosystem">
      <div class="wrap hero--ecosystem__inner">
        <div class="hero__copy">
          <p class="hero__eyebrow">Explore the</p>
          <h1 class="hero__title hero__title--display">Avail Ecosystem</h1>
          <p class="hero__text">Discover the growing network of chains, applications, and infrastructure building with Avail.</p>
        </div>
        <div class="hero__panel">
          <img src="assets/hero-panel.png" alt="" width="400" height="300" />
        </div>
      </div>
    </section>

    <section class="featured-partners">
      <div class="wrap">
        <h2 class="section-title">Featured Partners</h2>
        <div class="featured-grid">
          <a href="#" class="featured-card">
            <img src="assets/decor/pixel-tl.png" alt="" class="featured-card__pixel featured-card__pixel--tl" aria-hidden="true" />
            <span class="category-badge category-badge--white"><span>Chains</span></span>
            <img src="assets/featured/monad.png" alt="Monad" class="featured-card__logo" />
            <p class="featured-card__text">Instantly connect apps on Monad to over 13 chains with Avail Nexus.</p>
          </a>
          <a href="#" class="featured-card">
            <img src="assets/decor/pixel-br.png" alt="" class="featured-card__pixel featured-card__pixel--br" aria-hidden="true" />
            <span class="category-badge category-badge--white"><span>Apps</span></span>
            <img src="assets/featured/clober.png" alt="Clober" class="featured-card__logo" />
            <p class="featured-card__text">Fully onchain order book DEX routing orders to the best liquidity via Avail Nexus.</p>
          </a>
          <a href="#" class="featured-card">
            <img src="assets/decor/pixel-tr.png" alt="" class="featured-card__pixel featured-card__pixel--tr" aria-hidden="true" />
            <span class="category-badge category-badge--white"><span>Chains</span></span>
            <img src="assets/featured/farcaster.png" alt="Farcaster" class="featured-card__logo" />
            <p class="featured-card__text">Social media re-born onchain and powered by Avail.</p>
          </a>
        </div>
      </div>
    </section>

    <section class="integrations">
      <div class="wrap">
        <h2 class="section-title">Featured Nexus Integrations</h2>
        <article class="integration">
          <div class="integration__content">
            <div class="badge"><span class="badge__text">DEX</span></div>
            <img src="assets/integrations/bean-logo.png" alt="Bean Exchange" class="integration__logo" />
            <h3 class="integration__title">Unified Access to Spot &amp; Perps on Monad</h3>
            <p class="integration__text">One flow. One interface. Users and liquidity from 13+ ecosystems.</p>
            <p class="integration__text">Avail Nexus enables instant access to Bean on Monad even if your assets are on other blockchains.</p>
          </div>
          <div class="integration__media"><img loading="lazy" decoding="async" src="assets/integrations/bean.jpg" alt="" /></div>
        </article>
        <article class="integration integration--reverse">
          <div class="integration__content">
            <div class="badge"><span class="badge__text">DEX</span></div>
            <img src="assets/integrations/kalqix-logo.png" alt="KalqiX" class="integration__logo" />
            <h3 class="integration__title">High-Speed Trades &amp; Unified Liquidity</h3>
            <p class="integration__text">Fast, frictionless spot and perps trading on KalqiX. No bridges, fragmented balances, or gas tokens involved.</p>
            <p class="integration__text">Powered by Avail Nexus and Avail DA.</p>
          </div>
          <div class="integration__media"><img loading="lazy" decoding="async" src="assets/integrations/kalqix.jpg" alt="" /></div>
        </article>
      </div>
    </section>

    <section class="integrations integrations--da">
      <div class="wrap">
        <h2 class="section-title">Featured DA Integrations</h2>
        <article class="integration">
          <div class="integration__content">
            <div class="badge"><span class="badge__text">Chain</span></div>
            <img src="assets/integrations/farcaster-logo.png" alt="Farcaster" class="integration__logo" />
            <h3 class="integration__title">High performance chain for SocialFi</h3>
            <p class="integration__text">Decentralized Social, where new and better forms of interaction become possible.</p>
          </div>
          <div class="integration__media"><img loading="lazy" decoding="async" src="assets/integrations/farcaster.jpg" alt="" /></div>
        </article>
        <article class="integration integration--reverse">
          <div class="integration__content">
            <div class="badge"><span class="badge__text">Chain</span></div>
            <img src="assets/integrations/sxt-logo.png" alt="Space and Time" class="integration__logo" />
            <h3 class="integration__title">A blockchain for ZK-proven data</h3>
            <p class="integration__text">A decentralized database that witnesses data from onchain and offchain sources, secures it, and stores it for devs to query using Proof of SQL, SXT's ZK coprocessor.</p>
          </div>
          <div class="integration__media"><img loading="lazy" decoding="async" src="assets/integrations/sxt.jpg" alt="" /></div>
        </article>
      </div>
    </section>

    <section class="spotlight">
      <div class="wrap">
        <h2 class="section-title">Spotlight of the Month</h2>
        <div class="spotlight__panel">
          <img src="assets/spotlight/clober-logo.png" alt="Clober" class="spotlight__logo" />
          <p class="spotlight__quote">By integrating Avail Nexus, Clober becomes an 'Omnichain Liquidity Layer', pulling in liquidity from 13+ chains straight into Monad.</p>
          <div class="spotlight__video">
            <img src="assets/spotlight/video-thumb.jpg" alt="" loading="lazy" decoding="async" />
            <button type="button" class="spotlight__play" aria-label="Play video">
              <img src="assets/spotlight/play.svg" alt="" width="68" height="48" />
            </button>
          </div>
        </div>
        <div class="spotlight__cta">
          <a href="#" class="btn btn-primary btn-sm">Build With Us</a>
        </div>
      </div>
    </section>

    <section class="blogs">
      <div class="wrap">
        <h2 class="section-title">Featured Partnership Blogs</h2>
        <div class="blogs-grid">
          <article class="blog-card">
            <a href="#" class="blog-card__media"><img src="assets/blogs/blog-1.jpg" alt="" loading="lazy" decoding="async" /></a>
            <div class="blog-card__body">
              <h3 class="blog-card__title"><a href="#">Avail Empowers TRON dApps with Cross-Chain Liquidity and Market Access</a></h3>
              <p class="blog-card__meta"><span>By Shailey Singh</span><span>3 min read</span></p>
            </div>
          </article>
          <article class="blog-card">
            <a href="#" class="blog-card__media"><img src="assets/blogs/blog-2.jpg" alt="" loading="lazy" decoding="async" /></a>
            <div class="blog-card__body">
              <h3 class="blog-card__title"><a href="#">Avail Expands to Monad Testnet: Powering the Next-Gen Multichain Apps</a></h3>
              <p class="blog-card__meta"><span>By Andria Efstathiou</span><span>2 min read</span></p>
            </div>
          </article>
          <article class="blog-card">
            <a href="#" class="blog-card__media"><img src="assets/blogs/blog-3.jpg" alt="" loading="lazy" decoding="async" /></a>
            <div class="blog-card__body">
              <h3 class="blog-card__title"><a href="#">How Clober Unlocked Bridgeless Liquidity From 12+ Chains to Monad With Avail Nexus</a></h3>
              <p class="blog-card__meta"><span>By Andria Efstathiou</span><span>2 min read</span></p>
            </div>
          </article>
        </div>
      </div>
    </section>

    <section class="testimonials">
      <div class="wrap">
        <h2 class="section-title">Success Stories</h2>
      </div>
      <div class="testimonials__stage">
        <div class="testimonials__track" id="testimonials-track">
          <article class="testimonial-card">
            <img src="assets/testimonials/pixel-tl.png" alt="" class="testimonial-card__pixel testimonial-card__pixel--tl" aria-hidden="true" />
            <img src="assets/testimonials/pixel-br.png" alt="" class="testimonial-card__pixel testimonial-card__pixel--br" aria-hidden="true" />
            <div class="testimonial-card__logo"><img src="assets/testimonials/pingme.svg" alt="PingMe" /></div>
            <blockquote class="testimonial-card__quote">
              <p>"Avail makes cross-chain bridging effortless, perfectly aligning with PingMe's vision of making stablecoin transfers as simple as sending a text or email. With Avail, our users can move seamlessly across multiple blockchains with ease."</p>
              <cite>Kai Cheung, Co-founder &amp; CTO</cite>
            </blockquote>
          </article>
          <article class="testimonial-card">
            <img src="assets/testimonials/pixel-tl.png" alt="" class="testimonial-card__pixel testimonial-card__pixel--tl" aria-hidden="true" />
            <img src="assets/testimonials/pixel-br.png" alt="" class="testimonial-card__pixel testimonial-card__pixel--br" aria-hidden="true" />
            <div class="testimonial-card__logo"><img src="assets/testimonials/kalqix.png" alt="KalqiX" /></div>
            <blockquote class="testimonial-card__quote">
              <p>"With Avail Nexus and Avail DA, KalqiX takes a big leap toward unified liquidity and frictionless cross-chain trading while keeping decentralisation at the core."</p>
              <cite>Prateek Singhania, Co-Founder at KalqiX</cite>
            </blockquote>
          </article>
          <article class="testimonial-card">
            <img src="assets/testimonials/pixel-tl.png" alt="" class="testimonial-card__pixel testimonial-card__pixel--tl" aria-hidden="true" />
            <img src="assets/testimonials/pixel-br.png" alt="" class="testimonial-card__pixel testimonial-card__pixel--br" aria-hidden="true" />
            <div class="testimonial-card__logo"><img src="assets/testimonials/atlantis.png" alt="Atlantis DEX" /></div>
            <blockquote class="testimonial-card__quote">
              <p>"Avail Nexus allows users to trade on Atlantis with whatever assets they have, wherever they hold them. This removes many of the usual drop-off points."</p>
              <cite>Thoth, Leading Atlantis DEX</cite>
            </blockquote>
          </article>
          <article class="testimonial-card">
            <img src="assets/testimonials/pixel-tl.png" alt="" class="testimonial-card__pixel testimonial-card__pixel--tl" aria-hidden="true" />
            <img src="assets/testimonials/pixel-br.png" alt="" class="testimonial-card__pixel testimonial-card__pixel--br" aria-hidden="true" />
            <div class="testimonial-card__logo"><img src="assets/testimonials/bean.png" alt="Bean Exchange" /></div>
            <blockquote class="testimonial-card__quote">
              <p>"By integrating Nexus we're simplifying things for our users. They can easily trade on Bean using their full balances across chains."</p>
              <cite>Aaronx, Founder Bean Exchange</cite>
            </blockquote>
          </article>
          <article class="testimonial-card">
            <img src="assets/testimonials/pixel-tl.png" alt="" class="testimonial-card__pixel testimonial-card__pixel--tl" aria-hidden="true" />
            <img src="assets/testimonials/pixel-br.png" alt="" class="testimonial-card__pixel testimonial-card__pixel--br" aria-hidden="true" />
            <div class="testimonial-card__logo"><img src="assets/testimonials/clober.png" alt="Clober" /></div>
            <blockquote class="testimonial-card__quote">
              <p>"The bridgeless flow feels like magic. Our users can go from zero to trading on Monad in seconds, and that's a huge unlock for activation."</p>
              <cite>Kevin, Founder at Clober</cite>
            </blockquote>
          </article>
          <article class="testimonial-card">
            <img src="assets/testimonials/pixel-tl.png" alt="" class="testimonial-card__pixel testimonial-card__pixel--tl" aria-hidden="true" />
            <img src="assets/testimonials/pixel-br.png" alt="" class="testimonial-card__pixel testimonial-card__pixel--br" aria-hidden="true" />
            <div class="testimonial-card__logo"><img src="assets/testimonials/quickswap.webp" alt="QuickSwap" /></div>
            <blockquote class="testimonial-card__quote">
              <p>"Avail Nexus removes the biggest source of friction in our funnel. Users don't need to bounce around chains and bridges anymore. With Unified Balances, users can route liquidity to QuickSwap instantly and it just works."</p>
              <cite>Alexios Atlas, Head of BD, Quickswap Dex</cite>
            </blockquote>
          </article>
        </div>
        <button type="button" class="testimonials__nav testimonials__nav--prev" id="testimonials-prev" aria-label="Previous testimonial">
          <img src="assets/testimonials/arrow-prev.svg" alt="" width="40" height="40" />
        </button>
        <button type="button" class="testimonials__nav testimonials__nav--next" id="testimonials-next" aria-label="Next testimonial">
          <img src="assets/testimonials/arrow-next.svg" alt="" width="40" height="40" />
        </button>
      </div>
    </section>

    <section class="listings">
      <div class="wrap">
        <h2 class="section-title">Our Partners</h2>
        <div class="listings-grid">
{grid}
        </div>
      </div>
    </section>
  </main>

  <footer class="site-footer" aria-label="Footer">
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
                <li><a href="#" class="site-footer__nav-link">About us</a></li>
                <li><a href="#" class="site-footer__nav-link">Nexus</a></li>
                <li><a href="#" class="site-footer__nav-link">DA</a></li>
                <li><a href="#" class="site-footer__nav-link">Careers</a></li>
              </ul>
              </div>
              <ul class="site-footer__nav-list site-footer__nav-list--pages-right">
                <li><a href="#" class="site-footer__nav-link">Blog</a></li>
                <li><a href="#" class="site-footer__nav-link">Ecosystem</a></li>
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
  </footer>
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

      var track = document.getElementById('testimonials-track');
      var prev = document.getElementById('testimonials-prev');
      var next = document.getElementById('testimonials-next');
      if (track && prev && next) {{
        var index = 0;
        var cards = track.children;
        var total = cards.length;
        function update() {{
          track.style.transform = 'translateX(' + (-index * 100) + '%)';
        }}
        prev.addEventListener('click', function () {{
          index = (index - 1 + total) % total;
          update();
        }});
        next.addEventListener('click', function () {{
          index = (index + 1) % total;
          update();
        }});
      }}
    }})();
  </script>
</body>
</html>
"""
    (ROOT / "index.html").write_text(html)
    print(f"Wrote index.html with {len(partners)} partner cards")


if __name__ == "__main__":
    main()
