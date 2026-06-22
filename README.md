# Avail — Static HTML Sites

Marketing homepage and product pages built from Figma, served as static HTML/CSS/JS.

## Projects

| Folder | URL (local) | Description |
|--------|-------------|-------------|
| `avail-website/` | http://localhost:9345/ | Marketing homepage |
| `avail-deposit/` | http://localhost:8848/ | Product pages (Deposits, Nexus, DA, Ecosystem, Events, About, Terms, Whitepaper) |

## Run locally

```bash
# Marketing homepage
cd avail-website && python3 -m http.server 9345 --bind 127.0.0.1

# Product pages
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
