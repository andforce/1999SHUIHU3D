#!/usr/bin/env python3
"""Build side-by-side contact sheets for cross-asset character consistency QA."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
CHARACTERS = ROOT / "characters"
OUTPUT = ROOT / "qa" / "consistency"


def load_font(size: int) -> ImageFont.ImageFont:
    for candidate in (
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ):
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def load_rgb(path: Path) -> Image.Image:
    with Image.open(path) as source:
        return ImageOps.exif_transpose(source).convert("RGB")


def front_body_crop(image: Image.Image) -> Image.Image:
    """The canonical front view is the third of six horizontal columns."""
    left = round(image.width * 2 / 6)
    right = round(image.width * 3 / 6)
    return image.crop((left, 0, right, image.height))


def front_head_from_character(image: Image.Image, character_id: str) -> Image.Image:
    # 021 uses a four-head row above the six-body row, so the ordinary third-body
    # crop lands on the back-of-head panel instead of the canonical front face.
    if character_id == "021":
        return image.crop((0, 0, round(image.width / 4), round(image.height * 0.48)))
    body = front_body_crop(image)
    return body.crop((0, 0, body.width, round(body.height * 0.48)))


def front_head_from_sheet(image: Image.Image) -> Image.Image:
    """The canonical head front is the first of four horizontal columns."""
    return image.crop((0, 0, round(image.width / 4), image.height))


def paste_contained(
    canvas: Image.Image,
    image: Image.Image,
    frame: tuple[int, int, int, int],
    draw: ImageDraw.ImageDraw,
) -> None:
    left, top, right, bottom = frame
    thumb = ImageOps.contain(image, (right - left, bottom - top))
    x = left + (right - left - thumb.width) // 2
    y = top + (bottom - top - thumb.height) // 2
    canvas.paste(thumb, (x, y))
    draw.rectangle(frame, outline="#77736c", width=1)


def build_head_pairs() -> list[Path]:
    ids = [f"{index:03d}" for index in range(1, 109)]
    columns, rows = 6, 3
    cell_w, cell_h = 400, 300
    header_h, label_h = 44, 30
    font = load_font(20)
    header_font = load_font(24)
    outputs: list[Path] = []

    for page_index, start in enumerate(range(0, len(ids), columns * rows), start=1):
        page_ids = ids[start : start + columns * rows]
        canvas = Image.new("RGB", (columns * cell_w, header_h + rows * cell_h), "#d8d4cc")
        draw = ImageDraw.Draw(canvas)
        draw.text((14, 8), f"Head consistency {page_index:02d} | left: character  right: head sheet", fill="#202020", font=header_font)

        for index, character_id in enumerate(page_ids):
            row, column = divmod(index, columns)
            x, y = column * cell_w, header_h + row * cell_h
            draw.text((x + 10, y + 2), character_id, fill="#111111", font=font)
            baseline_path = CHARACTERS / character_id / "character-turnaround.png"
            head_path = CHARACTERS / character_id / "head-sheet.png"
            baseline = front_head_from_character(load_rgb(baseline_path), character_id)
            paste_contained(canvas, baseline, (x + 7, y + label_h, x + 194, y + cell_h - 7), draw)
            if head_path.is_file():
                head = front_head_from_sheet(load_rgb(head_path))
                paste_contained(canvas, head, (x + 206, y + label_h, x + cell_w - 7, y + cell_h - 7), draw)
            else:
                frame = (x + 206, y + label_h, x + cell_w - 7, y + cell_h - 7)
                draw.rectangle(frame, outline="#a33b32", width=3)
                draw.text((x + 248, y + 135), "MISSING", fill="#a33b32", font=font)

        output = OUTPUT / f"head-pairs-{page_index:02d}.jpg"
        canvas.save(output, quality=92, subsampling=0)
        outputs.append(output)
    return outputs


def build_entity_pairs(asset_name: str, prefix: str) -> list[Path]:
    entity_paths = sorted(CHARACTERS.glob(f"[0-9][0-9][0-9]/{asset_name}"))
    columns, rows = 3, 3
    cell_w, cell_h = 800, 430
    header_h, label_h = 44, 30
    font = load_font(20)
    header_font = load_font(24)
    outputs: list[Path] = []

    for page_index, start in enumerate(range(0, len(entity_paths), columns * rows), start=1):
        page_paths = entity_paths[start : start + columns * rows]
        canvas = Image.new("RGB", (columns * cell_w, header_h + rows * cell_h), "#d8d4cc")
        draw = ImageDraw.Draw(canvas)
        draw.text((14, 8), f"{prefix.title()} consistency {page_index:02d} | left: character  right: entity sheet", fill="#202020", font=header_font)

        for index, entity_path in enumerate(page_paths):
            character_id = entity_path.parent.name
            row, column = divmod(index, columns)
            x, y = column * cell_w, header_h + row * cell_h
            draw.text((x + 10, y + 2), character_id, fill="#111111", font=font)
            baseline = front_body_crop(load_rgb(entity_path.parent / "character-turnaround.png"))
            entity = load_rgb(entity_path)
            paste_contained(canvas, baseline, (x + 7, y + label_h, x + 244, y + cell_h - 7), draw)
            paste_contained(canvas, entity, (x + 256, y + label_h, x + cell_w - 7, y + cell_h - 7), draw)

        output = OUTPUT / f"{prefix}-pairs-{page_index:02d}.jpg"
        canvas.save(output, quality=92, subsampling=0)
        outputs.append(output)
    return outputs


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    outputs = [
        *build_head_pairs(),
        *build_entity_pairs("character-turnaround-original-pose.png", "pose"),
        *build_entity_pairs("weapon-sheet.png", "weapon"),
        *build_entity_pairs("mount-sheet.png", "mount"),
    ]
    for output in outputs:
        print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
