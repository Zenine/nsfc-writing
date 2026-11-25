#!/usr/bin/env python3
"""把本地保存的报告页面图片按页码顺序合并为一个 PDF。

用于往年结题报告：在国家自然科学基金基础研究知识库网页上完成验证、
逐页保存图片后，用本脚本合并。脚本只处理本地文件，不访问网络。

用法：
  python3 merge_pages.py 图片目录 [-o 输出.pdf] [--name 项目名称] [--author 作者]

PDF 的作者、创建者默认写运行脚本那台机器的实际用户名（git config user.name，
取不到时用系统登录名），不写库的默认值。

依赖：Pillow（pip install Pillow）。
"""
from __future__ import annotations

import argparse
import getpass
import os
import re
import subprocess
import sys
from pathlib import Path

SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}
ILLEGAL = set('\\/:*?"<>|')
MAX_NAME_BYTES = 200


def natural_key(path: Path) -> list:
    """按文件名中的数字自然排序：2.png 排在 10.png 前面。"""
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", path.name)]


def safe_name(name: str, fallback: str) -> str:
    cleaned = "".join(c for c in name if c not in ILLEGAL and c.isprintable()).strip()
    cleaned = cleaned.encode("utf-8")[:MAX_NAME_BYTES].decode("utf-8", "ignore").strip()
    return cleaned or fallback


def machine_user() -> str:
    """运行脚本的机器上的实际用户名：优先 git config user.name，其次系统登录名。"""
    try:
        name = subprocess.run(
            ["git", "config", "user.name"], capture_output=True, text=True, timeout=5
        ).stdout.strip()
        if name:
            return name
    except (OSError, subprocess.SubprocessError):
        pass
    for key in ("USER", "USERNAME", "LOGNAME"):
        if os.environ.get(key):
            return os.environ[key]
    try:
        return getpass.getuser()
    except Exception:
        return ""


def collect(folder: Path) -> list[Path]:
    return sorted((p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in SUFFIXES), key=natural_key)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="把报告页面图片合并为 PDF")
    parser.add_argument("folder", type=Path, help="存放页面图片的目录")
    parser.add_argument("-o", "--output", type=Path, help="输出 PDF 路径（默认为 目录名.pdf 或 项目名称.pdf）")
    parser.add_argument("--name", default="", help="项目名称，用于默认输出文件名")
    parser.add_argument("--overwrite", action="store_true", help="输出文件已存在时覆盖")
    parser.add_argument("--author", default=None, help="PDF 作者与创建者；默认取本机 git user.name 或系统用户名")
    args = parser.parse_args(argv)

    try:
        from PIL import Image
    except ImportError:
        print("缺少 Pillow：pip install Pillow", file=sys.stderr)
        return 2

    if not args.folder.is_dir():
        print(f"目录不存在：{args.folder}", file=sys.stderr)
        return 1
    pages = collect(args.folder)
    if not pages:
        print(f"目录中没有图片：{args.folder}", file=sys.stderr)
        return 1

    output = args.output or args.folder.parent / f"{safe_name(args.name, args.folder.name)}.pdf"
    if output.exists() and not args.overwrite:
        print(f"输出文件已存在：{output}（需要覆盖请加 --overwrite）", file=sys.stderr)
        return 1

    images = []
    try:
        for p in pages:
            with Image.open(p) as im:
                images.append(im.convert("RGB"))
        tmp = output.with_suffix(output.suffix + ".part")
        author = args.author if args.author is not None else machine_user()
        title = args.name or args.folder.name
        images[0].save(
            tmp, "PDF", resolution=100.0, save_all=True, append_images=images[1:],
            title=title, author=author, creator=author, producer=author,
        )
        tmp.replace(output)
    finally:
        for im in images:
            im.close()
    print(f"已合并 {len(pages)} 页 → {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
