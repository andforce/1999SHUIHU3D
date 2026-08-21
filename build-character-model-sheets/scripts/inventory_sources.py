#!/usr/bin/env python3
"""Create or refresh a model-sheet production manifest from source images."""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import re
import struct
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SUPPORTED_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
ENTITY_DEFAULT = {"weapon": "unknown", "mount": "unknown", "pet": "unknown"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan character source images and initialize a model-sheet project."
    )
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("project_dir", type=Path)
    parser.add_argument("--expected-count", type=int)
    parser.add_argument("--names-csv", type=Path, help="UTF-8 CSV with id,name columns")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace manifest entries and blank spec files; never deletes generated images.",
    )
    return parser.parse_args()


def natural_key(path: Path) -> list[Any]:
    return [
        int(part) if part.isdigit() else part.casefold()
        for part in re.split(r"(\d+)", path.name)
    ]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def image_size(path: Path) -> tuple[int | None, int | None]:
    try:
        from PIL import Image  # type: ignore

        with Image.open(path) as image:
            return image.size
    except ImportError:
        pass
    except Exception as exc:
        raise ValueError(f"无法读取图像 {path}: {exc}") from exc

    if path.suffix.casefold() == ".png":
        with path.open("rb") as handle:
            header = handle.read(24)
        if header[:8] != b"\x89PNG\r\n\x1a\n" or len(header) < 24:
            raise ValueError(f"无效 PNG: {path}")
        return struct.unpack(">II", header[16:24])
    return None, None


def load_names(path: Path | None) -> dict[str, str]:
    if path is None:
        return {}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not {"id", "name"}.issubset(reader.fieldnames):
            raise ValueError("姓名 CSV 必须包含 id,name 两列")
        return {
            row["id"].strip(): row["name"].strip()
            for row in reader
            if row.get("id", "").strip()
        }


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json_atomic(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    temporary.replace(path)


def outputs_for(identifier: str) -> dict[str, str]:
    base = Path("characters") / identifier
    return {
        "character_spec": str(base / "character-spec.json"),
        "character_turnaround": str(base / "character-turnaround.png"),
        "weapon_sheet": str(base / "weapon-sheet.png"),
        "mount_sheet": str(base / "mount-sheet.png"),
        "pet_sheet": str(base / "pet-sheet.png"),
        "review_notes": str(base / "review-notes.md"),
    }


def main() -> int:
    args = parse_args()
    source_dir = args.source_dir.expanduser().resolve()
    project_dir = args.project_dir.expanduser().resolve()
    if not source_dir.is_dir():
        print(f"错误：原画目录不存在：{source_dir}", file=sys.stderr)
        return 2

    images = sorted(
        (
            path
            for path in source_dir.iterdir()
            if path.is_file() and path.suffix.casefold() in SUPPORTED_SUFFIXES
        ),
        key=natural_key,
    )
    if not images:
        print("错误：没有找到 PNG、JPEG 或 WebP 图像", file=sys.stderr)
        return 2
    if args.expected_count is not None and len(images) != args.expected_count:
        print(
            f"错误：预期 {args.expected_count} 张，实际找到 {len(images)} 张；未写入项目",
            file=sys.stderr,
        )
        return 2

    identifiers = [path.stem for path in images]
    duplicates = sorted(
        {identifier for identifier in identifiers if identifiers.count(identifier) > 1}
    )
    if duplicates:
        print(f"错误：存在重复编号：{', '.join(duplicates)}", file=sys.stderr)
        return 2

    names = load_names(args.names_csv.expanduser().resolve() if args.names_csv else None)
    manifest_path = project_dir / "manifest.json"
    old_manifest = load_json(manifest_path, {"characters": []})
    old_entries = {
        entry.get("id"): entry for entry in old_manifest.get("characters", [])
    }

    skill_dir = Path(__file__).resolve().parent.parent
    spec_template = load_json(skill_dir / "assets" / "character-spec.template.json", {})
    review_template = (skill_dir / "assets" / "review-notes.template.md").read_text(
        encoding="utf-8"
    )
    entries = []

    for image in images:
        identifier = image.stem
        width, height = image_size(image)
        old_entry = old_entries.get(identifier, {}) if not args.force else {}
        entity_flags = dict(ENTITY_DEFAULT)
        entity_flags.update(old_entry.get("entities", {}))
        entry = {
            "id": identifier,
            "name": names.get(identifier, old_entry.get("name", "")),
            "source": str(image.resolve()),
            "width": width,
            "height": height,
            "sha256": sha256(image),
            "status": old_entry.get("status", "pending"),
            "entities": entity_flags,
            "outputs": outputs_for(identifier),
        }
        entries.append(entry)

        character_dir = project_dir / "characters" / identifier
        character_dir.mkdir(parents=True, exist_ok=True)
        spec_path = character_dir / "character-spec.json"
        if args.force or not spec_path.exists():
            spec = copy.deepcopy(spec_template)
            spec["id"] = identifier
            spec["name"] = entry["name"]
            spec["source"] = entry["source"]
            write_json_atomic(spec_path, spec)
        review_path = character_dir / "review-notes.md"
        if args.force or not review_path.exists():
            review_path.write_text(review_template, encoding="utf-8")

    manifest = {
        "schema_version": 1,
        "source_dir": str(source_dir),
        "project_dir": str(project_dir),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "character_count": len(entries),
        "characters": entries,
    }
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
        for entry in entries:
            writer.writerow(
                {
                    "id": entry["id"],
                    "name": entry["name"],
                    "source": entry["source"],
                    "width": entry["width"],
                    "height": entry["height"],
                    "status": entry["status"],
                    **entry["entities"],
                }
            )

    print(f"已建立项目：{project_dir}")
    print(f"图像数量：{len(entries)}")
    print(f"清单：{manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
