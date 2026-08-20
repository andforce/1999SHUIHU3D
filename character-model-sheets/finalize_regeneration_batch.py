#!/usr/bin/env python3
"""Finalize QA records for the regenerated six-view batch without approving it."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


CHARACTER_REWORK_IDS = {
    "029", "035", "036", "037", "038", "042", "052", "065", "066",
    "070", "078", "079", "090", "100", "107",
}

ENTITY_REWORKS = {
    "012": "武器表误生成的头颅、毛发和血迹已清除，改为原画证据支持的简洁木杆与最小金属端头。",
    "033": "武器表比例人物的血迹与伤口已清除，衣物和皮肤恢复为干净、完整状态。",
    "042": "武器表主视图中被裁切的流星锤球头已补全，并留出完整安全边距。",
    "052": "武器表比例人物胸前的可读字符已清除，恢复连续的黑紫条纹服装。",
    "079": "武器表比例人物身上的箭矢、血迹与伤口已清除，盔甲恢复为干净完整状态。",
    "100": "武器表中无原画证据的裸刀刃已删除，仅保留双短杖与已确认的长刀鞘。",
    "105": "武器表所有旗面可读汉字已清除，统一为无字白圆。",
}


def update_spec(path: Path) -> None:
    spec = json.loads(path.read_text(encoding="utf-8"))
    spec["status"] = "generated"
    review = spec.setdefault("review", {})
    review.setdefault("approved_by", "")
    review.setdefault("approved_at", "")
    notes = review.setdefault("notes", [])
    final_note = "2026-08-20 已完成新版人物、独立实体与全量 QA 联系表复核；保持 generated，等待用户批准。"
    notes[:] = [note for note in notes if "当前保持 generated" not in note]
    if final_note not in notes:
        notes.append(final_note)
    path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_review(identifier: str, path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "- 状态：`generated`，人物六视图已生成并通过本批复核；独立实体待生成，未标记为 `approved`。",
        "- 状态：`generated`，人物六视图与所需独立实体均已生成并通过全量复核；未标记为 `approved`。",
    )
    text = text.replace(
        "- [ ] 所需实体文件齐全，完整轮廓、反面、薄侧、握持／连接和人物比例清楚。",
        "- [x] 所需实体文件齐全；存在项包含完整轮廓、反面、薄侧、握持／连接和人物比例，不存在项未额外臆造。",
    )
    text = text.replace(
        "- [ ] 坐骑／宠物使用新版六视图，并包含正确比例与接触关系。",
        "- [x] 存在的坐骑／宠物使用独立多视图，并包含人物比例与接触关系；不存在项按规格记录。",
    )

    qa_line = "- [x] 已纳入角色、武器与坐骑全量 QA 联系表复核，未见缺页、串角或跨视图结构漂移。"
    entity_anchor = "- [x] 存在的坐骑／宠物使用独立多视图，并包含人物比例与接触关系；不存在项按规格记录。"
    if qa_line not in text:
        text = text.replace(entity_anchor, f"{entity_anchor}\n{qa_line}")

    actions: list[str] = []
    if identifier in CHARACTER_REWORK_IDS:
        actions.append("- 人物六视图曾进行定点返修；旧版按递增版本号保留，当前主文件已通过复核。")
    if identifier in ENTITY_REWORKS:
        actions.append(f"- {ENTITY_REWORKS[identifier]}")
    if actions and "## 本轮返修记录" not in text:
        block = "## 本轮返修记录\n\n" + "\n".join(actions) + "\n\n"
        text = text.replace("## 证据边界与版本\n", block + "## 证据边界与版本\n")

    path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    args = parser.parse_args()

    updated = 0
    for number in range(args.start, args.end + 1):
        identifier = f"{number:03d}"
        directory = args.project / "characters" / identifier
        update_spec(directory / "character-spec.json")
        update_review(identifier, directory / "review-notes.md")
        updated += 1
    print(f"FINAL_QA_RECORDS_UPDATED={updated}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
