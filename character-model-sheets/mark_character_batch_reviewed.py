#!/usr/bin/env python3
"""Mark the character-review section complete for a generated ID range."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    args = parser.parse_args()
    changed = 0
    for number in range(args.start, args.end + 1):
        cid = f"{number:03d}"
        path = args.project / "characters" / cid / "review-notes.md"
        text = path.read_text(encoding="utf-8")
        marker = "## 独立实体"
        if marker not in text:
            raise RuntimeError(f"{path} 缺少独立实体章节")
        head, tail = text.split(marker, 1)
        head = head.replace("- [ ]", "- [x]")
        head = head.replace(
            "等待新版图像生成与逐项验收；未标记为 `approved`。",
            "人物六视图已生成并通过本批复核；独立实体待生成，未标记为 `approved`。",
        )
        path.write_text(head + marker + tail, encoding="utf-8")
        changed += 1
    print(f"CHARACTER_REVIEWS_UPDATED={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
