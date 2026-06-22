# Avail — Static HTML Sites

Marketing homepage and product pages built from Figma, served as static HTML/CSS/JS.

## Live site (GitHub Pages)

**https://rochelle-alfonso.github.io/avail-html/**

| Page | URL |
|------|-----|
| Landing | https://rochelle-alfonso.github.io/avail-html/ |
| Marketing homepage | https://rochelle-alfonso.github.io/avail-html/avail-website/ |
| Deposits | https://rochelle-alfonso.github.io/avail-html/avail-deposit/ |
| Nexus | https://rochelle-alfonso.github.io/avail-html/avail-deposit/nexus/ |
| DA | https://rochelle-alfonso.github.io/avail-html/avail-deposit/da/ |
| Ecosystem | https://rochelle-alfonso.github.io/avail-html/avail-deposit/ecosystem/ |

## Projects

| Folder | URL (local) | Description |
|--------|-------------|-------------|
| `avail-website/` | http://localhost:9345/ | Marketing homepage |
| `avail-deposit/` | http://localhost:8848/ | Product pages (Deposits, Nexus, DA, Ecosystem, Events, About, Terms, Whitepaper) |

## Run locally

Serve the repo root so cross-site links work:

```bash
git clone https://github.com/rochelle-alfonso/avail-html.git
cd avail-html
python3 -m http.server 8080 --bind 127.0.0.1
# Open http://localhost:8080/
```

Or run each site separately (use separate ports):

```bash
cd avail-website && python3 -m http.server 9345 --bind 127.0.0.1
cd avail-deposit && python3 -m http.server 8848 --bind 127.0.0.1
```

After editing HTML in `avail-deposit/`, re-apply cross-page nav links:

```bash
cd avail-deposit && python3 apply_site_links.py
```

## Pages (`avail-deposit/`)

- `/` — Deposits landing
- `/nexus/` — Nexus
- `/da/` — Data Availability
- `/ecosystem/` — Ecosystem partners
- `/events/` — Events
- `/about-us/` — About
- `/terms/` — Terms & Conditions
- `/whitepaper/` — Whitepaper
