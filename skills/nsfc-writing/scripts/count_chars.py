#!/usr/bin/env python3
"""统计申请书文字的字数：汉字、其他非空白字符分别计数，合计不含空白。

用法：
  python3 count_chars.py 文件.md            # 统计整份文件
  python3 count_chars.py -t "要统计的文字"     # 统计一段文字
  echo "文字" | python3 count_chars.py -      # 从标准输入读取
"""
from __future__ import annotations

import argparse
import re
import sys

HAN = re.compile(r"[一-鿿㐀-䶿]")


def count(text: str) -> dict[str, int]:
    no_space = re.sub(r"\s", "", text)
    han = len(HAN.findall(no_space))
    return {"合计（不含空白）": len(no_space), "汉字": han, "其他字符": len(no_space) - han}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="统计字数（不含空白）")
    parser.add_argument("path", nargs="?", help="文件路径；- 表示标准输入")
    parser.add_argument("-t", "--text", help="直接给出要统计的文字")
    args = parser.parse_args(argv)
    if args.text is not None:
        text = args.text
    elif args.path == "-" or args.path is None:
        text = sys.stdin.read()
    else:
        with open(args.path, encoding="utf-8") as f:
            text = f.read()
    for k, v in count(text).items():
        print(f"{k}：{v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
