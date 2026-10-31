#!/usr/bin/env python3
"""从 Skill 内置模板初始化中文创作工作空间。"""
from __future__ import annotations
import argparse
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent.parent
TEMPLATE = HERE / "assets" / "工作室模板"

def main() -> int:
    p = argparse.ArgumentParser(description="初始化中文创作工作室")
    p.add_argument("path", type=Path)
    p.add_argument("--name", default="", help="写入工作室名称")
    args = p.parse_args()
    target = args.path.expanduser().resolve()
    if target.exists() and any(target.iterdir()):
        print(f"目标目录非空，为避免覆盖文件而停止：{target}")
        return 2
    target.mkdir(parents=True, exist_ok=True)
    shutil.copytree(TEMPLATE, target, dirs_exist_ok=True)
    config = target / "00_创作中枢" / "工作室配置.md"
    if args.name:
        text = config.read_text(encoding="utf-8").replace("- 工作室名称：", f"- 工作室名称：{args.name}", 1)
        config.write_text(text, encoding="utf-8")
    print(f"已创建中文创作工作空间：{target}")
    print("下一步：填写 00_创作中枢/工作室配置.md，并运行 validate_workspace.py")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
