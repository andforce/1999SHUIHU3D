#!/usr/bin/env python3
"""Build labeled contact sheets for original-pose six-view turnarounds."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
CHARACTERS = ROOT / "characters"
OUTPUT = ROOT / "qa" / "original-pose"
ROWS = 3
COLS = 6
CELL_W = 400
CELL_H = 280
LABEL_H = 30
BG = (238, 235, 226)


def font(size: int) -> ImageFont.ImageFont:
    for candidate in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ):
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    files = [
        CHARACTERS / f"{number:03d}" / "character-turnaround-original-pose.png"
        for number in range(1, 109)
    ]
    missing = [str(path) for path in files if not path.exists()]
    if missing:
        raise SystemExit("Missing original-pose images:\n" + "\n".join(missing))

    label_font = font(20)
    page_size = ROWS * COLS
    for page_index, start in enumerate(range(0, len(files), page_size), start=1):
        canvas = Image.new("RGB", (COLS * CELL_W, ROWS * CELL_H), BG)
        draw = ImageDraw.Draw(canvas)
        for offset, path in enumerate(files[start : start + page_size]):
            row, col = divmod(offset, COLS)
            x, y = col * CELL_W, row * CELL_H
            with Image.open(path) as opened:
                image = opened.convert("RGB")
            image = ImageOps.contain(image, (CELL_W - 10, CELL_H - LABEL_H - 10))
            px = x + (CELL_W - image.width) // 2
            py = y + LABEL_H + (CELL_H - LABEL_H - image.height) // 2
            canvas.paste(image, (px, py))
            draw.rectangle((x, y, x + CELL_W - 1, y + CELL_H - 1), outline=(150, 145, 132), width=1)
            draw.text((x + 10, y + 4), path.parent.name, fill=(40, 38, 34), font=label_font)
        target = OUTPUT / f"contact-sheet-{page_index:02d}.jpg"
        canvas.save(target, quality=92, subsampling=0)
        print(target)


if __name__ == "__main__":
    main()
