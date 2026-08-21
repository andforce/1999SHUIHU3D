#!/usr/bin/env python3
"""Validate the structure and completion state of a model-sheet project."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

VALID_STATUSES = {"pending", "spec-ready", "generated", "approved", "blocked"}
VALID_VARIANT_STATUSES = {"planned", "generated", "approved"}
VALID_PRESENCE = {"unknown", "absent", "present"}
ENTITY_OUTPUTS = {
    "weapon": "weapon_sheet",
    "mount": "mount_sheet",
    "pet": "pet_sheet",
}
SIX_VIEWS = [
    "left-profile-counterclockwise-45-degree",
    "left-profile",
    "front",
    "back",
    "right-profile",
    "right-profile-clockwise-45-degree",
]
HEAD_VIEWS = [
    "front",
    "back",
    "left-profile",
    "right-profile",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a model-sheet production project.")
    parser.add_argument("project_dir", type=Path)
    parser.add_argument(
        "--final",
        action="store_true",
        help="Require every character to be approved and complete",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print every warning and error instead of a compact summary",
    )
    return parser.parse_args()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def nonempty_file(path: Path) -> bool:
    return path.is_file() and path.stat().st_size > 0


def main() -> int:
    args = parse_args()
    project_dir = args.project_dir.expanduser().resolve()
    manifest_path = project_dir / "manifest.json"
    if not manifest_path.is_file():
        print(f"错误：缺少 {manifest_path}", file=sys.stderr)
        return 2

    manifest = load_json(manifest_path)
    characters = manifest.get("characters")
    if not isinstance(characters, list) or not characters:
        print("错误：manifest.json 没有角色记录", file=sys.stderr)
        return 2

    errors: list[str] = []
    warnings: list[str] = []
    seen: set[str] = set()
    status_counts: dict[str, int] = {}

    for entry in characters:
        identifier = str(entry.get("id", "")).strip()
        label = f"角色 {identifier or '<空编号>'}"
        if not identifier:
            errors.append(f"{label}：缺少 id")
            continue
        if identifier in seen:
            errors.append(f"{label}：编号重复")
        seen.add(identifier)

        source = Path(entry.get("source", ""))
        if not nonempty_file(source):
            errors.append(f"{label}：原图不存在或为空：{source}")

        status = entry.get("status", "")
        status_counts[status] = status_counts.get(status, 0) + 1
        if status not in VALID_STATUSES:
            errors.append(f"{label}：无效状态 {status!r}")
        if args.final and status != "approved":
            errors.append(
                f"{label}：最终交付状态必须为 approved，当前为 {status!r}"
            )

        outputs = entry.get("outputs", {})
        spec_relative = outputs.get("character_spec", "")
        spec_path = project_dir / spec_relative
        spec = None
        if not nonempty_file(spec_path):
            errors.append(f"{label}：缺少角色规格 {spec_path}")
        else:
            try:
                spec = load_json(spec_path)
            except (OSError, json.JSONDecodeError) as exc:
                errors.append(f"{label}：角色规格无法读取：{exc}")

        if spec is not None and spec.get("status", "pending") != status:
            message = (
                f"{label}：规格状态 {spec.get('status')!r} 与清单状态 {status!r} 不一致；"
                "运行 sync_manifest.py"
            )
            (errors if args.final else warnings).append(message)
        if spec is not None:
            generation = spec.get("generation", {})
            spec_views = generation.get("views")
            if spec_views != SIX_VIEWS:
                message = (
                    f"{label}：规格不是基于左面逆时针转45度、左面、正面、"
                    "背面、右面、基于右面顺时针转45度六视图顺序；"
                    "运行 migrate_six_views.py"
                )
                (errors if args.final else warnings).append(message)
            spec_head_views = generation.get("head_views")
            if spec_head_views != HEAD_VIEWS:
                message = (
                    f"{label}：规格不是正面、背面、左侧面、右侧面"
                    "头部四视图顺序；运行 migrate_six_views.py"
                )
                (errors if args.final else warnings).append(message)

            variants = generation.get("variants", [])
            if not isinstance(variants, list):
                errors.append(f"{label}：generation.variants 必须是数组")
            else:
                seen_variant_ids: set[str] = set()
                for variant_index, variant in enumerate(variants, start=1):
                    variant_label = f"{label} 变体 {variant_index}"
                    if not isinstance(variant, dict):
                        errors.append(f"{variant_label}：记录必须是对象")
                        continue

                    variant_id = str(variant.get("id", "")).strip()
                    if not variant_id:
                        errors.append(f"{variant_label}：缺少 id")
                    elif variant_id in seen_variant_ids:
                        errors.append(f"{label}：变体 id 重复：{variant_id!r}")
                    else:
                        seen_variant_ids.add(variant_id)
                        variant_label = f"{label} 变体 {variant_id}"

                    variant_status = variant.get("status", "planned")
                    if variant_status not in VALID_VARIANT_STATUSES:
                        errors.append(
                            f"{variant_label}：无效状态 {variant_status!r}"
                        )

                    variant_kind = str(variant.get("kind", variant_id)).strip()
                    if (
                        variant_kind == "original-pose-turnaround"
                        or "views" in variant
                    ) and variant.get("views") != SIX_VIEWS:
                        errors.append(
                            f"{variant_label}：原画姿态版必须使用固定六视图顺序"
                        )

                    output_relative = str(variant.get("output", "")).strip()
                    if not output_relative:
                        errors.append(f"{variant_label}：缺少 output")
                        continue
                    output_fragment = Path(output_relative)
                    if output_fragment.is_absolute() or ".." in output_fragment.parts:
                        errors.append(
                            f"{variant_label}：output 必须是角色目录内的相对路径"
                        )
                        continue
                    if variant_status in {"generated", "approved"}:
                        variant_output = spec_path.parent / output_fragment
                        if not nonempty_file(variant_output):
                            errors.append(
                                f"{variant_label}：状态为 {variant_status}，"
                                f"但缺少 {variant_output}"
                            )

        entities = entry.get("entities", {})
        for entity, output_key in ENTITY_OUTPUTS.items():
            presence = entities.get(entity, "unknown")
            if presence not in VALID_PRESENCE:
                errors.append(f"{label}：{entity} presence 无效：{presence!r}")
            elif presence == "unknown":
                message = f"{label}：{entity} 尚未判定"
                (errors if args.final else warnings).append(message)
            elif presence == "present" and (
                args.final or status in {"generated", "approved"}
            ):
                output_path = project_dir / outputs.get(output_key, "")
                if not nonempty_file(output_path):
                    errors.append(f"{label}：标记有 {entity}，但缺少 {output_path}")
            if spec is not None:
                spec_presence = (
                    spec.get("entities", {})
                    .get(entity, {})
                    .get("presence", "unknown")
                )
                if spec_presence != presence:
                    message = (
                        f"{label}：规格中的 {entity}={spec_presence!r} 与清单中的"
                        f" {entity}={presence!r} 不一致；运行 sync_manifest.py"
                    )
                    (errors if args.final else warnings).append(message)

        if args.final or status in {"generated", "approved"}:
            turnaround = project_dir / outputs.get("character_turnaround", "")
            if not nonempty_file(turnaround):
                errors.append(f"{label}：缺少人物六视图与头部放大图 {turnaround}")

    print(f"角色总数：{len(characters)}")
    print(
        "状态："
        + ", ".join(
            f"{key or '<空>'}={value}" for key, value in sorted(status_counts.items())
        )
    )
    warning_limit = len(warnings) if args.verbose else 20
    error_limit = len(errors) if args.verbose else 50
    for warning in warnings[:warning_limit]:
        print(f"警告：{warning}")
    if len(warnings) > warning_limit:
        print(
            f"另有 {len(warnings) - warning_limit} 项警告未显示；使用 --verbose 查看全部"
        )
    for error in errors[:error_limit]:
        print(f"错误：{error}", file=sys.stderr)
    if len(errors) > error_limit:
        print(
            f"另有 {len(errors) - error_limit} 项错误未显示；使用 --verbose 查看全部",
            file=sys.stderr,
        )
    print(f"警告 {len(warnings)} 项，错误 {len(errors)} 项")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
