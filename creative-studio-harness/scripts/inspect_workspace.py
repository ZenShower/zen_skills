#!/usr/bin/env python3
"""检查一个中文创作空间的结构，输出可读的接入报告。"""
from __future__ import annotations

import argparse
from pathlib import Path


EXPECTED = [
    "00_创作中枢",
    "01_设定与生产资产库",
    "02_灵感与选题池",
    "03_内容生产",
    "04_数据反馈与复盘",
    "05_成品归档",
    "06_参考资料与输入",
    "99_模板",
]
MARKERS = ["工作室配置.md", "唯一事实源索引.md", "工作台.md", "工具登记表.md"]


def main() -> int:
    parser = argparse.ArgumentParser(description="检查中文创作工作室")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    root = args.path.expanduser().resolve()
    if not root.exists():
        print(f"路径不存在：{root}")
        return 2

    print(f"工作空间：{root}")
    print()
    print("顶层目录：")
    for name in EXPECTED:
        state = "存在" if (root / name).is_dir() else "缺失"
        print(f"- [{state}] {name}")

    print()
    print("中枢文件：")
    for name in MARKERS:
        state = "存在" if (root / "00_创作中枢" / name).is_file() else "缺失"
        print(f"- [{state}] 00_创作中枢/{name}")

    projects = sorted(
        (root / "03_内容生产").glob("项目*_*")
        if (root / "03_内容生产").exists()
        else []
    )
    print()
    print(f"可识别项目目录：{len(projects)}")
    for project in projects[:20]:
        print(f"- {project.name}")
    if len(projects) > 20:
        print(f"- …另有 {len(projects) - 20} 个")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
