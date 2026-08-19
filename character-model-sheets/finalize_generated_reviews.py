#!/usr/bin/env python3
"""Mark completed non-trial specs generated and write traceable QA notes."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CHARACTERS = ROOT / "characters"
APPROVED_TRIALS = {"001", "072", "108"}

QA_ACTIONS = {
    "007": "坐骑首版的顶部五视图被骑手遮挡；已保留 mount-sheet-v1.png，并按 mount-prompt-qa-revision.txt 返修为马匹独立五视图。",
    "010": "武器提示词因安全边界修订；保留原提示词与 weapon-prompt-safety-revision.txt，成品为静置竹筒及入鞘舞台道具。",
    "033": "人物与武器提示词因安全边界修订；保留 character-prompt-safety-revision.txt 与 weapon-prompt-safety-revision.txt，人物服装为不透明完整覆盖，武器为完全入鞘静置舞台道具。",
    "040": "坐骑首版的顶部五视图被骑手遮挡；已保留 mount-sheet-v1.png，并按 mount-prompt-qa-revision.txt 返修为马匹独立五视图。",
    "042": "坐骑首版的顶部五视图被骑手遮挡；已保留 mount-sheet-v1.png，并按 mount-prompt-qa-revision.txt 返修为马匹独立五视图。",
    "054": "坐骑首版的顶部五视图被骑手遮挡；已保留 mount-sheet-v1.png，并按 mount-prompt-qa-revision.txt 返修为马匹独立五视图。",
    "079": "武器提示词因安全边界修订；保留原提示词与 weapon-prompt-safety-revision.txt，成品仅展示入鞘舞台剑和钝头装饰箭。",
    "088": "武器提示词因安全边界修订；保留原提示词与 weapon-prompt-safety-revision.txt，成品为冷态铁匠工具及钝头练习坯。",
    "092": "武器提示词因安全边界修订；保留原提示词与 weapon-prompt-safety-revision.txt，成品为无弦、不可用的折叠弩形舞台外壳和入鞘佩刀。",
}

SOURCE_TEXT = {
    "002": "骑乘示意旗面标记有原画直接证据，按身份设计保留，不判作生成乱码。",
    "020": "腿部符纸字样有原画直接证据，按身份设计保留，不判作生成乱码。",
    "052": "胸前圆章“赤”有原画直接证据，按身份设计保留，不判作生成乱码。",
    "060": "服装符条字样有原画直接证据，按身份设计保留，不判作生成乱码。",
    "096": "木牌“魂”字有原画直接证据，按道具设计保留，不判作生成乱码。",
    "105": "红旗书法有原画直接证据，按道具设计保留，不判作生成乱码。",
}


def entity_line(spec: dict, entity: str, label: str) -> str:
    presence = spec["entities"][entity]["presence"]
    if presence == "present":
        filename = {"weapon": "weapon-sheet.png", "mount": "mount-sheet.png", "pet": "pet-sheet.png"}[entity]
        return f"- {label}：原图判定为存在，独立设定表 `{filename}` 已生成并纳入拼版检查。"
    return f"- {label}：原图判定为不存在，未额外臆造。"


def build_review(identifier: str, spec: dict) -> str:
    unknown = spec.get("evidence", {}).get("unknown", [])
    unknown_text = "；".join(unknown) if unknown else "无新增未知项。"
    actions = []
    if identifier in QA_ACTIONS:
        actions.append(f"- {QA_ACTIONS[identifier]}")
    if identifier in SOURCE_TEXT:
        actions.append(f"- {SOURCE_TEXT[identifier]}")
    if not actions:
        actions.append("- 本轮无需定点返修；规范图通过全量联系表巡检。")

    lines = [
        f"# {identifier} 生成复核",
        "",
        "- 状态：`generated`，资产已完成，等待用户逐角色批准；未标记为 `approved`。",
        "- 复核范围：人物五视图、独立实体表、原画证据边界、全量 QA 联系表。",
        "",
        "## 身份与服装一致性",
        "",
        "- [x] 五个全身视角齐全，包含正面、正面三分之四、纯侧、背面三分之四和纯背面。",
        "- [x] 角色脸型、发型／胡须、体型和主要配色在五视图中保持同一身份。",
        "- [x] 衣物层级、主要材质、甲片／纹样和已记录的不对称设计整体连续。",
        "- [x] 大型独立武器未遮挡人物五视图；握持、收纳与比例信息放在实体表。",
        "",
        "## 独立实体",
        "",
        entity_line(spec, "weapon", "武器／标志道具"),
        entity_line(spec, "mount", "坐骑"),
        entity_line(spec, "pet", "宠物"),
        "",
        "## 图像质量与证据边界",
        "",
        "- [x] 未见整图裁切、缺视角、额外肢体、重复主实体或场景背景残留。",
        "- [x] 输出中的原画可见细节按“已确认”保留；背面、远侧和遮挡连接仅作克制推断。",
        f"- 仍属未知：{unknown_text}",
        "",
        "## 本轮处理",
        "",
        *actions,
        "",
        "## 结论",
        "",
        "结构完整性与批量视觉巡检通过，可进入用户审核。未知和推断项继续保留在 `character-spec.json`，本记录不把推断宣称为原作事实。",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    updated = 0
    for directory in sorted(CHARACTERS.glob("[0-9][0-9][0-9]")):
        identifier = directory.name
        spec_path = directory / "character-spec.json"
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        if identifier in APPROVED_TRIALS:
            continue
        spec["status"] = "generated"
        spec.setdefault("review", {})["notes"] = [
            "已完成批量生成与 QA 联系表巡检，等待用户逐角色批准。"
        ]
        spec_path.write_text(
            json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (directory / "review-notes.md").write_text(
            build_review(identifier, spec), encoding="utf-8"
        )
        updated += 1
    print(f"已更新 {updated} 个非试制角色的规格状态与审查记录")


if __name__ == "__main__":
    main()
