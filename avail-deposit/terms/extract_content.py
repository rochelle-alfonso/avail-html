#!/usr/bin/env python3
"""Extract terms body HTML from Figma design context export."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DC_FILE = Path(
    "/Users/rochellealfonso/.cursor/projects/Users-rochellealfonso-Documents-Avail/agent-tools/895085a7-ab79-417f-a5d6-7dc7c734fe04.txt"
)


def inline_html(inner: str) -> str:
    inner = re.sub(r"\{`([^`]*)`\}", r"\1", inner)
    inner = re.sub(
        r"<span className=\"[^\"]*font-\['Inter:Bold'[^\"]*\">([^<]*)</span>",
        r"<strong>\1</strong>",
        inner,
    )
    inner = re.sub(
        r"<span className=\"[^\"]*text-\[#09f\][^\"]*\">([^<]*)</span>",
        lambda m: f'<a href="{m.group(1)}" class="terms-link">{m.group(1)}</a>',
        inner,
    )
    inner = re.sub(
        r"<span className=\"[^\"]*underline[^\"]*\">([^<]*)</span>",
        lambda m: f'<a href="{m.group(1)}" class="terms-link">{m.group(1)}</a>',
        inner,
    )
    inner = re.sub(r"<span className=\"[^\"]*\">([^<]*)</span>", r"\1", inner)
    inner = re.sub(r"<[^>]+>", "", inner)
    return inner.replace("****", "").strip()


def block_html(body: str) -> str:
    parts = []
    for p in re.findall(r"<p(?: className=\"[^\"]*\")?>(.*?)</p>", body, re.S):
        text = re.sub(r"\s+", " ", inline_html(p)).strip()
        if text and text != "•":
            parts.append(text)
    if not parts:
        return ""
    joined = " ".join(parts)
    joined = re.sub(r"\(\s+", "(", joined)
    joined = re.sub(r"\s+\)", ")", joined)
    joined = re.sub(r"“\s+", "“", joined)
    joined = re.sub(r"\s+”", "”", joined)
    joined = joined.replace("theMainnet", "the Mainnet")
    joined = joined.replace("NOWARRANTY", "NO WARRANTY")
    joined = joined.replace("proof- of-stake", "proof-of-stake")
    return joined


def extract_blocks(chunk: str) -> list[str]:
    pattern = re.compile(
        r'<div className="[^"]*" data-node-id="(663:25\d\d|663:26\d\d)"[^>]*>(.*?)</div>\s*'
        r'(?=<div className="[^"]*" data-node-id="663:|</div>\s*</div>\s*<div className="-translate-x-1/2 absolute bg-\[#ededed\])',
        re.S,
    )
    html_parts: list[str] = []
    pending_hw_prefix = ""

    for node, body in pattern.findall(chunk):
        if node == "663:2583":
            continue

        if node == "663:2584":
            url = "https://docs.availproject.org/operate/system-requirements/"
            pending_hw_prefix = (
                f'j. “<strong>Node Hardware Requirements</strong>” means the minimum Node hardware '
                f'and operating requirements posted at <a href="{url}" class="terms-link">{url}</a>'
            )
            continue

        if node == "663:2587" and pending_hw_prefix:
            text = block_html(body)
            html_parts.append(f"            <p>{pending_hw_prefix}{text}</p>")
            pending_hw_prefix = ""
            continue

        text = block_html(body)
        if not text:
            continue

        if text.startswith("https://docs.availproject.org/operate/system-"):
            continue
        if text in ("requirements/", ", as such requirements may be changed by us from time to time, all of which are incorporated and made a part of these Terms by this reference."):
            continue

        if text.endswith("as posted at") and node == "663:2597":
            url = "https://docs.availproject.org/category/operate-a-node/"
            text += f' <a href="{url}" class="terms-link">{url}</a>.'

        if text.startswith("“Node Hardware Requirements") and "j." not in text:
            continue

        if text.startswith("“Developer Grants"):
            text = "e. " + text

        for url in (
            "https://www.availproject.org/",
            "https://docs.availproject.org/category/operate-a-node/",
        ):
            if url in text and "terms-link" not in text:
                text = text.replace(
                    url, f'<a href="{url}" class="terms-link">{url}</a>', 1
                )

        html_parts.append(f"            <p>{text}</p>")

    # Bullet list from annex
    bullets = [
        "to violate, or encourage the violation of, the legal rights of others;",
        "to engage in, promote or encourage illegal activity;",
        "for any unlawful, invasive, infringing, defamatory, or fraudulent purpose;",
        "to intentionally distribute viruses, worms, Trojan horses, corrupted files, hoaxes, or other items of a destructive or deceptive nature;",
        "to interfere with the use of the Mainnet, Node Software, or the Avail Project;",
        "to disable, interfere with or circumvent any aspect of the Mainnet, Node Software, or the Avail Project;",
        "to use the Mainnet or the Node Software in violation of the Terms; and",
        "to build similar or competitive products to or features of the Avail Project.",
    ]
    html_parts.append("            <ul class=\"terms-list\">")
    for item in bullets:
        html_parts.append(f"              <li>{item}</li>")
    html_parts.append("            </ul>")

    return html_parts


def main() -> None:
    text = DC_FILE.read_text()
    start = text.find('data-node-id="663:2566"')
    end = text.find('data-node-id="663:2649"')
    chunk = text[start:end]
    parts = extract_blocks(chunk)

    # Remove duplicate annex bullet paragraph if present
    cleaned: list[str] = []
    seen_ul = False
    for part in parts:
        if part.strip().startswith("<ul class=\"terms-list\">"):
            if seen_ul:
                continue
            seen_ul = True
        if "to violate, or encourage the violation" in part and "<ul" not in part:
            continue
        if "Business Restricted Jurisdiction" in part and part in cleaned:
            continue
        cleaned.append(part)

    (ROOT / "content.html").write_text("\n".join(cleaned) + "\n")
    print(f"Wrote content.html ({len(cleaned)} blocks)")


if __name__ == "__main__":
    main()
