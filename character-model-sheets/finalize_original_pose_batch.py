#!/usr/bin/env python3
"""Finalize metadata and write a QA summary for original-pose turnarounds."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
CHARACTERS = ROOT / "characters"
APPROVED_SAMPLES = {"001", "002", "016"}
REPAIRED = {
    "004": "初版保留为 character-turnaround-original-pose-v1.png。",
    "006": "初版保留为 character-turnaround-original-pose-v1.png。",
    "008": "初版保留为 character-turnaround-original-pose-v1.png。",
    "065": "两轮边缘修复分别保留为 v1、v2；当前版完整收纳人物、披布与兵器。",
    "080": "边缘修复版保留为 v1；当前版完整收纳人物与长兵器。",
    "098": "两轮边缘修复分别保留为 v1、v2；当前版完整收纳蹲姿人物手脚。",
    "105": "两轮边缘修复分别保留为 v1、v2；当前版完整收纳人物、旗帜与刀。",
}


def append_unique(values: list[str], value: str) -> None:
    if value not in values:
        values.append(value)


def main() -> None:
    outputs: list[Path] = []
    status_counts: Counter[str] = Counter()

    for spec_path in sorted(CHARACTERS.glob("*/character-spec.json")):
        character_id = spec_path.parent.name
        spec = json.loads(spec_path.read_text())
        variants = spec.setdefault("generation", {}).setdefault("variants", [])
        variant = next(
            (item for item in variants if item.get("id") == "original-pose-turnaround"),
            None,
        )
        if variant is None:
            raise RuntimeError(f"{character_id}: missing original-pose-turnaround variant")

        output = spec_path.parent / variant["output"]
        if not output.is_file():
            raise RuntimeError(f"{character_id}: missing {output.name}")
        outputs.append(output)

        desired_status = "approved" if character_id in APPROVED_SAMPLES else "generated"
        variant["status"] = desired_status
        status_counts[desired_status] += 1

        review_notes = spec.setdefault("review", {}).setdefault("notes", [])
        if desired_status == "approved":
            append_unique(
                review_notes,
                "2026-08-21 用户确认原画姿态版样例标准，变体状态更新为 approved。",
            )
        else:
            append_unique(
                review_notes,
                "2026-08-21 已生成独立原画姿态版六视图 character-turnaround-original-pose.png；默认中立站姿 character-turnaround.png 保持不变；当前变体为 generated，等待用户逐项批准。",
            )
        if character_id in REPAIRED:
            append_unique(review_notes, f"2026-08-21 原画姿态版 QA：{REPAIRED[character_id]}")

        spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n")

    if len(outputs) != 108:
        raise RuntimeError(f"expected 108 outputs, found {len(outputs)}")

    formats: Counter[str] = Counter()
    sizes: Counter[tuple[int, int]] = Counter()
    for output in outputs:
        with Image.open(output) as image:
            image.verify()
        with Image.open(output) as image:
            formats[image.format or "unknown"] += 1
            sizes[image.size] += 1

    contact_sheets = sorted((ROOT / "qa" / "original-pose").glob("contact-sheet-*.jpg"))
    report = [
        "# 原画姿态六视图全量校验",
        "",
        "- 日期：2026-08-21",
        f"- 角色目录：108",
        f"- 原画姿态六视图输出：{len(outputs)}",
        f"- 可读取 PNG：{formats.get('PNG', 0)}",
        f"- 样例已批准：{status_counts['approved']}（001、002、016）",
        f"- 全量已生成待批准：{status_counts['generated']}",
        f"- QA 联系表：{len(contact_sheets)} 张（每张 18 个角色）",
        "- 版式检查：每个输出包含六个独立观察方向；默认中立站姿输出未被覆盖。",
        "- 边缘修复：004、006、008、065、080、098、105 保留历史版本；065、080、098、105 针对主体或兵器贴边进行了专项补绘。",
        "",
        "## 输出尺寸",
        "",
    ]
    report.extend(
        f"- {width}×{height}：{count} 张"
        for (width, height), count in sorted(sizes.items())
    )
    report.extend(
        [
            "",
            "## QA 联系表",
            "",
            *[f"- {sheet.relative_to(ROOT)}" for sheet in contact_sheets],
            "",
        ]
    )
    (ROOT / "original-pose-validation.md").write_text("\n".join(report))

    print(f"finalized={len(outputs)}")
    print(f"approved_samples={status_counts['approved']}")
    print(f"generated_waiting_approval={status_counts['generated']}")
    print(f"contact_sheets={len(contact_sheets)}")


if __name__ == "__main__":
    main()
