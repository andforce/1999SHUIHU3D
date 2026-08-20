#!/usr/bin/env python3
"""Prepare six-view prompts/spec metadata for characters 004-108."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


SIX_VIEWS = [
    "left-profile-counterclockwise-45-degree",
    "left-profile",
    "front",
    "back",
    "right-profile",
    "right-profile-clockwise-45-degree",
]


def joined(value: object) -> str:
    if isinstance(value, list):
        return "；".join(str(item) for item in value) if value else "无"
    return str(value or "无")


def anchor_prompt(anchors: list[dict[str, object]]) -> str:
    if not anchors:
        return (
            "No permanent one-sided costume anchor is confirmed in the current evidence record. "
            "Held weapons, mounts and action-driven cloth motion are not permanent body asymmetry; "
            "do not invent a new one-sided accessory."
        )
    return json.dumps(anchors, ensure_ascii=False, indent=2)


def inferred_anchors(spec: dict[str, object]) -> list[dict[str, object]]:
    character = spec.get("character", {})
    if not isinstance(character, dict):
        return []
    current = character.get("asymmetric_anchors")
    if isinstance(current, list):
        return current

    anchors: list[dict[str, object]] = []
    rules = character.get("left_right_asymmetry", [])
    if not isinstance(rules, list):
        return anchors
    for rule_value in rules:
        rule = str(rule_value)
        if "右前腰" in rule or "右腰" in rule:
            side = "character-right"
            point = "right-front-waist"
        elif "左前腰" in rule or "左腰" in rule:
            side = "character-left"
            point = "left-front-waist"
        else:
            continue
        anchors.append(
            {
                "feature": rule,
                "anatomical_side": side,
                "attachment_point": point,
                "local_orientation": "保持原图记录的局部悬挂方向、盘卷关系与重力朝向",
                "never_mirror": True,
                "never_reposition_for_visibility": True,
                "visibility_by_view": {
                    "left-profile-counterclockwise-45-degree": "按角色自身侧和真实透视显示，远侧时允许遮挡",
                    "left-profile": "按角色自身侧显示，远侧时允许被躯干遮挡",
                    "front": "角色自身右侧投影在画面左侧，左侧反之",
                    "back": "角色自身右侧投影在画面右侧，左侧反之",
                    "right-profile": "按角色自身侧显示，远侧时允许被躯干遮挡",
                    "right-profile-clockwise-45-degree": "按角色自身侧和真实透视显示，远侧时允许遮挡",
                },
            }
        )
    return anchors


def character_prompt(spec: dict[str, object]) -> str:
    cid = str(spec["id"])
    evidence = spec.get("evidence", {})
    character = spec.get("character", {})
    entities = spec.get("entities", {})
    identity = character.get("identity", {})
    anchors = character.get("asymmetric_anchors", [])
    return f"""Use case: stylized-concept
Asset type: professional game/animation character six-view model sheet
Input images: Image 1 is the sole primary visual evidence for character {cid}. Image 2 is the legacy turnaround only as a secondary identity/costume continuity reference; do not copy its old five-view layout or any mistake. Image 3 is the approved project six-view layout/style baseline only; never borrow its face, body, costume, colors or accessories.
Primary request: Create one complete landscape six-view turnaround of the exact same character from Image 1. Preserve the original identity and design but replace the action, camera angle, effects and scenery with a neutral production pose.

Strict left-to-right order: (1) based on the left profile, rotate the whole character counterclockwise 45 degrees; (2) pure left profile; (3) pure front; (4) pure back; (5) pure right profile; (6) based on the right profile, rotate the whole character clockwise 45 degrees.

Relative 45-degree geometry is mandatory. Column 1 derives only from column 2 by rotating the entire body counterclockwise 45 degrees around the vertical axis. Column 6 derives only from column 5 by rotating the entire body clockwise 45 degrees. Head, ribcage, pelvis, knees and both feet rotate together. Columns 1 and 6 must show opposite near cheeks, ears, shoulders, costume/armor perspective and far-limb occlusion. Never copy, reuse, horizontally flip or collapse either column into a front or pure profile.

Identity: gender presentation {identity.get('gender_presentation', 'unknown')}; apparent age {identity.get('apparent_age', 'unknown')}; face {identity.get('face', 'unknown')}; hair {identity.get('hair', 'unknown')}; facial hair {identity.get('facial_hair', 'unknown')}; body type {identity.get('body_type', 'unknown')}; proportions {identity.get('body_proportions', 'preserve Image 1')}.
Costume layers: {joined(character.get('costume_layers', []))}.
Palette: {joined(character.get('palette', []))}.
Materials: {joined(character.get('materials', []))}.
Patterns and symbols: {joined(character.get('patterns_and_symbols', []))}.
Must preserve: {joined(character.get('must_preserve', []))}.
Confirmed visual evidence: {joined(evidence.get('confirmed', []))}.
Restrained structural inference: {joined(evidence.get('inferred', []))}.
Unknown and editable: {joined(evidence.get('unknown', []))}.
Asymmetric three-dimensional anchors: {anchor_prompt(anchors if isinstance(anchors, list) else [])}

Anchor rule: every recorded asymmetric feature stays permanently fixed to its anatomical side and three-dimensional attachment point. Rotate only the observer/body orientation; never swap sides, mirror, duplicate or move a far-side feature toward the camera. Real occlusion has priority over full visibility.

Composition: exactly six full-body figures and nothing else, fully visible and uncropped, identical height, head-body ratio, head-top line and foot baseline, equal spacing, neutral natural stance, arms slightly away from torso, hands relaxed. Keep permanent worn accessories and scabbards only when visible in Image 1. Every held weapon, signature prop, mount and pet must be completely absent from this character sheet; they will be generated on separate sheets. Do not add a second row or any object study.

Style/medium: faithful to Image 1's bold black ink contours, late-1990s hand-painted cel shading and watercolor coloring; clean warm-light-gray production-sheet presentation matching Image 3, not photorealistic.
Constraints: same identity, face, hair, facial hair, body type, garment layers, palette, patterns, armor and fixed accessories in every view; pure side/front/back views structurally readable; inferred back details minimal and undecorated. No title, labels, letters, watermark, scenery, action effects, extra people, extra animals, duplicate weapons, fused props, extra limbs, accidental mirroring or cropping.
"""


def entity_prompt(spec: dict[str, object], kind: str) -> str:
    cid = str(spec["id"])
    entity = spec["entities"][kind]
    items = joined(entity.get("items", []))
    notes = joined(entity.get("notes", []))
    evidence = spec.get("evidence", {})
    if kind == "weapon":
        return f"""Use case: stylized-concept
Asset type: professional game/animation standalone weapon or signature-prop design sheet
Input images: Image 1 is the sole primary visual evidence for character {cid}'s entity. Image 2 is the newly generated character six-view and determines owner identity, scale and style. Image 3 is the legacy entity sheet only as a secondary continuity reference; correct its mistakes and do not copy labels or old layout.
Primary request: Create one clean landscape design sheet for: {items}. Preserve only the silhouette, colors, materials, patterns, grip and attachment relationships supported by Image 1.
Required views: complete main face, complete reverse, true thinnest side profile, key construction details, natural grip/use state, storage or body-attachment state when applicable, and a small full-body owner comparison for accurate scale. Every repeated view must depict the same entity and dimensions.
Entity notes: {notes}.
Confirmed evidence: {joined(evidence.get('confirmed', []))}.
Unknown/inferred restraint: {joined(evidence.get('unknown', []))}; complete unseen reverse, edge and mechanism minimally with no unsupported ornament.
Style: bold black ink contours, late-1990s hand-painted cel shading and watercolor coloring, warm light-gray neutral production-sheet background, even working light.
Constraints: all complete views fully visible and uncropped; no title, labels, letters, measurements, watermark, scenery, action effects, unrelated props, duplicate entities, fused hands, extra blades, extra parts or invented decoration.
"""

    animal_label = "mount" if kind == "mount" else "pet"
    contact = (
        "Include one accurate owner-and-animal standing scale comparison and one natural riding/contact reference. "
        "Show saddle, bridle, reins, armor or packs only where Image 1 confirms them; explain their attachment visually."
        if kind == "mount"
        else "Include one accurate owner-and-animal standing scale comparison and a natural interaction reference."
    )
    return f"""Use case: stylized-concept
Asset type: professional game/animation {animal_label} six-view model sheet
Input images: Image 1 is the sole primary visual evidence for character {cid}'s {animal_label}. Image 2 is the newly generated owner six-view and determines owner scale and style. Image 3 is the legacy entity sheet only as a secondary continuity reference; correct its mistakes and do not copy its old layout.
Primary request: Create one clean landscape six-view model sheet of the exact same animal/entity: {items}.
Strict left-to-right order: based on left profile counterclockwise 45 degrees, pure left profile, pure front, pure back, pure right profile, based on right profile clockwise 45 degrees. Column 1 derives only from column 2; column 6 derives only from column 5. The two relative 45-degree views must have opposite near eyes, ears, shoulders/forelimbs and far-limb occlusion; never copy or horizontally flip.
Entity notes: {notes}.
Confirmed evidence: {joined(evidence.get('confirmed', []))}.
Unknown/inferred restraint: {joined(evidence.get('unknown', []))}; complete unseen anatomy and equipment minimally without new markings or ornaments.
{contact}
Composition: all six complete bodies fully visible and uncropped, consistent height, proportions and ground baseline; clean warm light-gray background and even working light.
Style: bold black ink contours, late-1990s hand-painted cel shading and watercolor coloring, accurate readable anatomy.
Constraints: one consistent animal identity; no title, labels, letters, watermark, scenery, effects, extra animals, extra riders, duplicated limbs, malformed paws/hooves, unsupported tack or cropping.
"""


def review_notes(cid: str, spec: dict[str, object]) -> str:
    entities = spec["entities"]
    required = [
        label
        for key, label in (("weapon", "武器／标志道具"), ("mount", "坐骑"), ("pet", "宠物"))
        if entities[key]["presence"] == "present"
    ]
    required_text = "、".join(required) if required else "无独立实体"
    return f"""# {cid} 新版六视图生产复核

- 状态：`generated`，等待新版图像生成与逐项验收；未标记为 `approved`。
- 需交付：人物六视图；{required_text}。

## 人物六视图

- [ ] 固定顺序为基于左面逆时针转45度、左面、正面、背面、右面、基于右面顺时针转45度。
- [ ] 第一列与第六列来自相反侧面基准，近侧结构与远侧遮挡相反，未复制或水平翻转。
- [ ] 六个全身视角同高、同基线、无裁切，身份、服装、纹样和配色一致。
- [ ] 非对称结构固定在同一解剖侧与三维连接点，远侧按真实关系遮挡。
- [ ] 未见多余肢体、重复实体、融合道具、透视冲突、文字乱码或场景残留。

## 独立实体

- [ ] 所需实体文件齐全，完整轮廓、反面、薄侧、握持／连接和人物比例清楚。
- [ ] 坐骑／宠物使用新版六视图，并包含正确比例与接触关系。

## 证据边界与版本

- 背面、远侧、内部与遮挡结构继续按 `inferred` 或 `unknown` 处理，不宣称为原作事实。
- 旧版资产已保留为递增版本文件；当前主文件将用于新版交付。
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("--start", type=int, default=4)
    parser.add_argument("--end", type=int, default=108)
    args = parser.parse_args()
    project = args.project.resolve()
    prepared = 0
    for number in range(args.start, args.end + 1):
        cid = f"{number:03d}"
        char_dir = project / "characters" / cid
        spec_path = char_dir / "character-spec.json"
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        spec["status"] = "generated"
        spec.setdefault("character", {})["asymmetric_anchors"] = inferred_anchors(spec)
        generation = spec.setdefault("generation", {})
        generation["views"] = list(SIX_VIEWS)
        generation["notes"] = [
            "沿用 001–003 新版基准的暖浅灰画布、强黑墨线、1990 年代手绘赛璐璐与水彩着色。",
            "人物六视图不持大型独立实体，避免遮挡服装；握持、收纳、骑乘和比例放入实体表。",
            "六个视角必须同高、同脚底基线、同一身份，且左面、正面、背面与右面结构清晰。",
            "第一列只以第二列左面为基准逆时针旋转45度；第六列只以第五列右面为基准顺时针旋转45度，两列不得复制或水平翻转。",
        ]
        review = spec.setdefault("review", {})
        review["approved_by"] = ""
        review["approved_at"] = ""
        review["notes"] = [
            "2026-08-19 已迁移为新版六视图并进入全量重新生成。",
            "旧版人物与实体图片已保留为递增版本备份。",
            "当前保持 generated，待新版图像逐项验收和用户确认。",
        ]
        spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (char_dir / "character-prompt.txt").write_text(character_prompt(spec), encoding="utf-8")
        for kind in ("weapon", "mount", "pet"):
            if spec["entities"][kind]["presence"] == "present":
                (char_dir / f"{kind}-prompt.txt").write_text(entity_prompt(spec, kind), encoding="utf-8")
        (char_dir / "review-notes.md").write_text(review_notes(cid, spec), encoding="utf-8")
        prepared += 1
    print(f"PREPARED={prepared}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
