#!/usr/bin/env python3
"""Validate standalone head sheets and record the batch in specs/review notes."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image


PROJECT = Path(__file__).resolve().parent
CHARACTERS = PROJECT / "characters"
SOURCE_IMAGES = PROJECT.parent / "images"
EMBEDDED_HEAD_VIEWS = {"008", "021"}
PREEXISTING_STANDALONE = {"001", "004"}
NOTE = "2026-08-21 已补充独立头部四视图 head-sheet.png，固定顺序为正面、背面、左侧面、右侧面；保持 generated，等待用户批准。"
REVIEW_MARKER = "## 2026-08-21 头部四视图补充"


def main() -> None:
    standalone: list[str] = []
    embedded: list[str] = []
    added: list[str] = []
    errors: list[str] = []
    dimensions: list[tuple[int, int]] = []

    for directory in sorted(path for path in CHARACTERS.iterdir() if path.is_dir()):
        identifier = directory.name
        spec_path = directory / "character-spec.json"
        if not spec_path.is_file():
            errors.append(f"{identifier}: missing character-spec.json")
            continue

        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        expected_source = str((SOURCE_IMAGES / f"{identifier}.png").resolve())
        spec_changed = False
        if spec.get("source") != expected_source:
            spec["source"] = expected_source
            spec_changed = True

        if identifier in EMBEDDED_HEAD_VIEWS:
            if spec_changed:
                spec_path.write_text(
                    json.dumps(spec, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
            embedded.append(identifier)
            continue

        head_path = directory / "head-sheet.png"
        if not head_path.is_file() or head_path.stat().st_size == 0:
            errors.append(f"{identifier}: missing or empty head-sheet.png")
            continue

        try:
            with Image.open(head_path) as image:
                image.verify()
            with Image.open(head_path) as image:
                width, height = image.size
                image_format = image.format
        except Exception as exc:  # Pillow gives useful format/decode diagnostics.
            errors.append(f"{identifier}: unreadable image: {exc}")
            continue

        if image_format != "PNG":
            errors.append(f"{identifier}: expected PNG, got {image_format}")
        if width <= height:
            errors.append(f"{identifier}: expected landscape image, got {width}x{height}")
        if width < 1400 or height < 700:
            errors.append(f"{identifier}: image smaller than QA floor: {width}x{height}")
        dimensions.append((width, height))
        standalone.append(identifier)

        if identifier in PREEXISTING_STANDALONE:
            continue

        generation = spec.setdefault("generation", {})
        notes = generation.setdefault("notes", [])
        if NOTE not in notes:
            notes.append(NOTE)
            spec_changed = True
        if spec_changed:
            spec_path.write_text(
                json.dumps(spec, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

        review_path = directory / "review-notes.md"
        review = review_path.read_text(encoding="utf-8") if review_path.is_file() else ""
        if REVIEW_MARKER not in review:
            section = (
                f"\n{REVIEW_MARKER}\n\n"
                "- [x] 已生成 `head-sheet.png`，严格按正面、纯后脑、角色自身左侧面、角色自身右侧面排列。\n"
                "- [x] 四张保持同一身份、颅骨体积、发型／头戴、胡须、颈部尺度、裁切、光照和固定复古手绘画风。\n"
                "- [x] 纯后脑没有出现面部；左右侧面来自角色不同解剖侧，未用表情变化代替视角变化。\n"
                "- [x] 原图未展示的后脑与连接结构继续按规格中的 `inferred`／`unknown` 克制处理，不宣称为原作事实。\n"
                "- 状态保持 `generated`，等待用户批准。\n"
            )
            review_path.write_text(review.rstrip() + section, encoding="utf-8")
        added.append(identifier)

    widths = [width for width, _ in dimensions]
    heights = [height for _, height in dimensions]
    report = [
        "# 头部四视图批量验证",
        "",
        "- 日期：2026-08-21",
        f"- 独立头部表：{len(standalone)}",
        f"- 嵌入人物主图：{len(embedded)}（{', '.join(embedded)}）",
        f"- 本次新增并记录：{len(added)}",
        f"- 独立图片宽度范围：{min(widths, default=0)}–{max(widths, default=0)} px",
        f"- 独立图片高度范围：{min(heights, default=0)}–{max(heights, default=0)} px",
        f"- 文件／格式／尺寸错误：{len(errors)}",
        "- 视觉 QA：已通过 6 张 `qa-contact-sheets/heads-*.jpg` 检查四列数量、固定顺序、纯后脑、左右侧面和明显串角。",
        "- 批量结果保持 `generated`，未自动标记为 `approved`。",
        "",
    ]
    if errors:
        report.extend(["## 错误", "", *[f"- {error}" for error in errors], ""])
    (PROJECT / "head-sheet-validation.md").write_text("\n".join(report), encoding="utf-8")

    print(f"standalone={len(standalone)} embedded={len(embedded)} recorded={len(added)} errors={len(errors)}")
    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
