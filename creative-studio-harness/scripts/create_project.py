#!/usr/bin/env python3
"""从项目模板创建一个新的中文项目目录。"""
from __future__ import annotations
import argparse
from pathlib import Path
import shutil


def next_number(parent: Path) -> int:
    nums = []
    for item in parent.glob("项目*_*"):
        prefix = item.name.split("_", 1)[0].replace("项目", "")
        if prefix.isdigit():
            nums.append(int(prefix))
    return max(nums, default=0) + 1

def main() -> int:
    p = argparse.ArgumentParser(description="创建中文内容项目")
    p.add_argument("workspace", type=Path)
    p.add_argument("title")
    p.add_argument("--number", type=int)
    args = p.parse_args()
    root = args.workspace.expanduser().resolve()
    template = root / "99_模板" / "单项目生产模板"
    parent = root / "03_内容生产"
    if not template.is_dir():
        print(f"找不到项目模板：{template}")
        return 2
    parent.mkdir(parents=True, exist_ok=True)
    number = args.number or next_number(parent)
    name = f"项目{number:03d}_{args.title}"
    target = parent / name
    if target.exists():
        print(f"项目已存在：{target}")
        return 2
    shutil.copytree(template, target)
    for path in target.rglob("*.md"):
        path.write_text(path.read_text(encoding="utf-8").replace("项目XXX", f"项目{number:03d}"), encoding="utf-8")
    print(f"已创建项目：{target}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
