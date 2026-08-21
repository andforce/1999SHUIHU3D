#!/usr/bin/env python3
"""Migrate character specs to the fixed body- and head-view schema."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

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
    parser = argparse.ArgumentParser(
        description="Migrate model-sheet specs to the fixed body- and head-view schema."
    )
    parser.add_argument("project_dir", type=Path)
    return parser.parse_args()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json_atomic(path: Path, data: Any) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    temporary.replace(path)


def main() -> int:
    args = parse_args()
    project_dir = args.project_dir.expanduser().resolve()
    characters_dir = project_dir / "characters"
    if not characters_dir.is_dir():
        print(f"错误：缺少角色目录 {characters_dir}", file=sys.stderr)
        return 2

    spec_paths = sorted(characters_dir.glob("*/character-spec.json"))
    if not spec_paths:
        print("错误：没有找到 character-spec.json", file=sys.stderr)
        return 2

    changed = 0
    errors: list[str] = []
    for spec_path in spec_paths:
        try:
            spec = load_json(spec_path)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{spec_path}：{exc}")
            continue
        generation = spec.setdefault("generation", {})
        spec_changed = False
        if generation.get("views") != SIX_VIEWS:
            generation["views"] = list(SIX_VIEWS)
            spec_changed = True
        if generation.get("head_views") != HEAD_VIEWS:
            generation["head_views"] = list(HEAD_VIEWS)
            spec_changed = True
        for obsolete_field in ("head_back_view_required", "head_back_view_reason"):
            if obsolete_field in generation:
                generation.pop(obsolete_field)
                spec_changed = True
        if spec_changed:
            write_json_atomic(spec_path, spec)
            changed += 1

    if errors:
        for error in errors:
            print(f"错误：{error}", file=sys.stderr)
        print(f"已更新 {changed} 份规格，另有 {len(errors)} 份失败", file=sys.stderr)
        return 1

    print(
        f"已检查 {len(spec_paths)} 份规格；更新 {changed} 份为"
        "基于左面逆时针转45度、左面、正面、背面、右面、"
        "基于右面顺时针转45度六视图与正面、背面、左侧面、"
        "右侧面固定头部四视图"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
