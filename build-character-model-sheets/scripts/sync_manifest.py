#!/usr/bin/env python3
"""Sync names, statuses, and entity decisions from character specs to manifests."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ENTITIES = ("weapon", "mount", "pet")
VALID_STATUSES = {"pending", "spec-ready", "generated", "approved", "blocked"}
VALID_PRESENCE = {"unknown", "absent", "present"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync character specs into manifest.json and manifest.csv."
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
    manifest_path = project_dir / "manifest.json"
    if not manifest_path.is_file():
        print(f"错误：缺少 {manifest_path}", file=sys.stderr)
        return 2

    manifest = load_json(manifest_path)
    characters = manifest.get("characters", [])
    errors: list[str] = []
    changed = 0

    for entry in characters:
        identifier = str(entry.get("id", "")).strip()
        spec_relative = entry.get("outputs", {}).get(
            "character_spec", f"characters/{identifier}/character-spec.json"
        )
        spec_path = project_dir / spec_relative
        if not spec_path.is_file():
            errors.append(f"角色 {identifier}：缺少 {spec_path}")
            continue
        try:
            spec = load_json(spec_path)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"角色 {identifier}：规格无法读取：{exc}")
            continue

        status = spec.get("status", "pending")
        if status not in VALID_STATUSES:
            errors.append(f"角色 {identifier}：无效状态 {status!r}")
            continue
        entity_values: dict[str, str] = {}
        for entity in ENTITIES:
            presence = (
                spec.get("entities", {}).get(entity, {}).get("presence", "unknown")
            )
            if presence not in VALID_PRESENCE:
                errors.append(
                    f"角色 {identifier}：{entity} presence 无效：{presence!r}"
                )
            entity_values[entity] = presence

        if errors and errors[-1].startswith(f"角色 {identifier}："):
            continue

        before = (entry.get("name"), entry.get("status"), entry.get("entities"))
        spec_name = str(spec.get("name", "")).strip()
        if spec_name:
            entry["name"] = spec_name
        entry["status"] = status
        entry["entities"] = entity_values
        after = (entry.get("name"), entry.get("status"), entry.get("entities"))
        if before != after:
            changed += 1

    if errors:
        for error in errors:
            print(f"错误：{error}", file=sys.stderr)
        print("清单未写入；请先修复全部规格错误", file=sys.stderr)
        return 1

    manifest["updated_at"] = datetime.now(timezone.utc).isoformat()
    write_json_atomic(manifest_path, manifest)

    csv_path = project_dir / "manifest.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        fieldnames = [
            "id",
            "name",
            "source",
            "width",
            "height",
            "status",
            "weapon",
            "mount",
            "pet",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for entry in characters:
            writer.writerow(
                {
                    "id": entry.get("id", ""),
                    "name": entry.get("name", ""),
                    "source": entry.get("source", ""),
                    "width": entry.get("width", ""),
                    "height": entry.get("height", ""),
                    "status": entry.get("status", ""),
                    **entry.get("entities", {}),
                }
            )

    print(f"已同步 {len(characters)} 个角色；{changed} 个汇总项发生变化")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
