#!/usr/bin/env python3
"""检查中文创作工作空间的最小运行条件。"""
from __future__ import annotations

import argparse
from pathlib import Path


REQUIRED_DIRS = [
    "00_创作中枢",
    "01_设定与生产资产库",
    "02_灵感与选题池",
    "03_内容生产",
    "04_数据反馈与复盘",
    "05_成品归档",
    "06_参考资料与输入",
    "99_模板",
]
REQUIRED_FILES = [
    "工作室配置.md",
    "唯一事实源索引.md",
    "工作台.md",
    "内容形式与节奏策略.md",
    "工具登记表.md",
]
CONFIG_FIELDS = [
    "工作室名称：",
    "一句话定位：",
    "核心受众：",
    "主要内容形式：",
    "内容承诺：",
    "视觉与叙事方向：",
    "明确禁区：",
    "当前可用工具：",
]


def has_value(text: str, marker: str) -> bool:
    for line in text.splitlines():
        if line.lstrip().startswith(f"- {marker}"):
            value = line.split(marker, 1)[1].strip()
            return bool(value)
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="验证中文创作工作室")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    root = args.path.expanduser().resolve()
    errors = []

    if not root.exists() or not root.is_dir():
        print(f"验证未通过：目录不存在：{root}")
        return 1

    for name in REQUIRED_DIRS:
        if not (root / name).is_dir():
            errors.append(f"缺少目录：{name}")
    for name in REQUIRED_FILES:
        if not (root / "00_创作中枢" / name).is_file():
            errors.append(f"缺少文件：00_创作中枢/{name}")

    template = root / "99_模板" / "单项目生产模板"
    if not template.is_dir():
        errors.append("缺少目录：99_模板/单项目生产模板")

    config = root / "00_创作中枢" / "工作室配置.md"
    if config.is_file():
        text = config.read_text(encoding="utf-8")
        for marker in CONFIG_FIELDS:
            if not has_value(text, marker):
                errors.append(f"工作室配置尚未填写：{marker}")

    if errors:
        print("验证未通过：")
        for error in errors:
            print(f"- {error}")
        return 1
    print("验证通过：工作空间具备最小运行结构，工作室配置已完成 v0.1 字段填写。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
