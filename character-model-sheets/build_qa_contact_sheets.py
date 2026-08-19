#!/usr/bin/env python3
"""Build compact QA contact sheets from canonical project outputs."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
CHARACTERS = ROOT / "characters"
OUTPUT = ROOT / "qa-contact-sheets"


def load_font(size: int) -> ImageFont.ImageFont:
    candidates = (
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    )
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def build_group(asset_name: str, prefix: str, *, per_sheet: int = 18) -> list[Path]:
    paths = sorted(CHARACTERS.glob(f"[0-9][0-9][0-9]/{asset_name}"))
    if not paths:
        return []

    OUTPUT.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []
    columns = 6
    rows = math.ceil(per_sheet / columns)
    cell_w, cell_h = 320, 235
    label_h = 28
    font = load_font(20)
    header_font = load_font(24)

    for page_index, start in enumerate(range(0, len(paths), per_sheet), start=1):
        page_paths = paths[start : start + per_sheet]
        canvas = Image.new("RGB", (columns * cell_w, 44 + rows * cell_h), "#d8d4cc")
        draw = ImageDraw.Draw(canvas)
        title = f"{prefix} QA {page_index:02d}  |  {len(paths)} assets"
        draw.text((14, 8), title, fill="#202020", font=header_font)

        for index, path in enumerate(page_paths):
            row, column = divmod(index, columns)
            x = column * cell_w
            y = 44 + row * cell_h
            frame = (x + 7, y + label_h + 3, x + cell_w - 7, y + cell_h - 7)
            with Image.open(path) as source:
                image = ImageOps.exif_transpose(source).convert("RGB")
                thumb = ImageOps.contain(image, (frame[2] - frame[0], frame[3] - frame[1]))
            paste_x = frame[0] + (frame[2] - frame[0] - thumb.width) // 2
            paste_y = frame[1] + (frame[3] - frame[1] - thumb.height) // 2
            canvas.paste(thumb, (paste_x, paste_y))
            draw.rectangle(frame, outline="#77736c", width=1)
            draw.text((x + 10, y + 2), path.parent.name, fill="#111111", font=font)

        output_path = OUTPUT / f"{prefix.lower()}-{page_index:02d}.jpg"
        canvas.save(output_path, quality=90, subsampling=0)
        created.append(output_path)
    return created


def main() -> None:
    outputs: list[Path] = []
    outputs.extend(build_group("character-turnaround.png", "characters"))
    outputs.extend(build_group("weapon-sheet.png", "weapons"))
    outputs.extend(build_group("mount-sheet.png", "mounts"))
    for path in outputs:
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
