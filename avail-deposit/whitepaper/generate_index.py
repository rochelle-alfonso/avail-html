#!/usr/bin/env python3
"""Generate whitepaper/index.html."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent

PDF_EMBED_URL = (
    "https://drive.google.com/file/d/1mD4OYR02jINrMU8ffnXTOr8T8M8QibEc/preview"
)

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
                <li><a href="../about-us/" class="site-footer__nav-link">About us</a></li>
                <li><a href="../nexus/" class="site-footer__nav-link">Nexus</a></li>
                <li><a href="../da/" class="site-footer__nav-link">DA</a></li>
                <li><a href="#" class="site-footer__nav-link">Careers</a></li>
              </ul>
              </div>
              <ul class="site-footer__nav-list site-footer__nav-list--pages-right">
                <li><a href="#" class="site-footer__nav-link">Blog</a></li>
                <li><a href="../ecosystem/" class="site-footer__nav-link">Ecosystem</a></li>
                <li><a href="../terms/" class="site-footer__nav-link">T&amp;C</a></li>
                <li><a href="../whitepaper/" class="site-footer__nav-link" aria-current="page">Whitepaper</a></li>
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


def main() -> None:
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Whitepaper — Avail</title>
  <meta name="description" content="Read the Avail whitepaper." />
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
      <section class="hero hero--whitepaper">
        <div class="wrap hero--whitepaper__inner">
          <p class="hero--whitepaper__eyebrow">Read Our</p>
          <h1 class="hero--whitepaper__title">Whitepaper</h1>
        </div>
      </section>

      <section class="whitepaper-viewer" aria-label="Avail whitepaper">
        <div class="wrap whitepaper-viewer__inner">
          <iframe
            class="whitepaper-viewer__frame"
            src="{PDF_EMBED_URL}"
            title="Avail Whitepaper PDF"
            allow="autoplay"
            loading="lazy"
          ></iframe>
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
