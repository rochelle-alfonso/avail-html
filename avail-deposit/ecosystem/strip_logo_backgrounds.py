#!/usr/bin/env python3
"""Make near-white pixels transparent in partner logo PNGs."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

PARTNERS = Path(__file__).resolve().parent / "assets" / "partners"
THRESHOLD = 220
SATURATION_SPREAD = 28  # max(r,g,b) - min(r,g,b) for neutral backgrounds
FEATHER = 10


def is_background_pixel(r: int, g: int, b: int) -> bool:
    if max(r, g, b) < THRESHOLD:
        return False
    return max(r, g, b) - min(r, g, b) <= SATURATION_SPREAD


def strip_white_background(path: Path) -> bool:
    try:
        img = Image.open(path).convert("RGBA")
    except Exception as exc:
        print(f"Skip {path.name}: {exc}")
        return False

    pixels = img.load()
    width, height = img.size
    changed = False

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            if is_background_pixel(r, g, b):
                pixels[x, y] = (r, g, b, 0)
                changed = True
            elif max(r, g, b) >= THRESHOLD - FEATHER and is_background_pixel(r, g, b):
                lightness = max(r, g, b)
                alpha = int((THRESHOLD - lightness + FEATHER) / FEATHER * 255)
                alpha = max(0, min(255, alpha))
                if alpha < a:
                    pixels[x, y] = (r, g, b, alpha)
                    changed = True

    if changed:
        img.save(path, optimize=True)
    return changed


def main() -> None:
    updated = 0
    skipped = 0
    for path in sorted(PARTNERS.glob("*.png")):
        if strip_white_background(path):
            updated += 1
            print(f"Updated {path.name}")
        else:
            skipped += 1
    print(f"Done: {updated} updated, {skipped} unchanged or skipped")


if __name__ == "__main__":
    main()
