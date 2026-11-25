#!/usr/bin/env python3
"""检查公开文本与本机参考资料（sources/text/）是否存在长段连续重合。

只保留汉字，去掉空白、标点、数字和拉丁字母后，按整份文件滑窗比对：任意连续
N 个字符（默认 20）与参考资料相同即报告，跨行、跨列表项的重合也能检出。
与 sources/official/ 中官方公开文件相同的片段属于有意引用，不计。
用法：python3 scripts/check_overlap.py <目录或文件>...
退出码：0 无重合（或缺少参考资料时 SKIPPED）；1 有重合。
"""
from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

import os

ROOT = Path(__file__).resolve().parent.parent
SOURCES = Path(os.environ.get("NSFC_SOURCES_DIR", ROOT / "sources"))
SRC = SOURCES / "text"
OFFICIAL = SOURCES / "official"
N = 20
KEEP = re.compile(r"[\u4e00-\u9fff]")
SUFFIXES = {".md", ".yaml", ".yml", ".json", ".txt"}
SENTENCE_END = ("。", "!", "?", ";", "！", "？", "；")


def norm_with_lines(text: str) -> tuple[str, list[int]]:
    """返回规范化文本及每个字符对应的原文行号。"""
    chars: list[str] = []
    lines: list[int] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        line = unicodedata.normalize("NFKC", line)
        for ch in line:
            if KEEP.match(ch):
                chars.append(ch)
                lines.append(lineno)
        # 句末标点结尾的行视为句子边界，避免把相邻两句拼成伪重合；硬换行的半句仍会连起来比对。
        if line.rstrip().endswith(SENTENCE_END):
            chars.append("|")
            lines.append(lineno)
    return "".join(chars), lines


def windows(s: str) -> set[str]:
    return {s[i : i + N] for i in range(len(s) - N + 1)}


def ref_files(folder: Path) -> list[Path]:
    if not folder.is_dir():
        return []
    return sorted(p for p in folder.rglob("*") if p.is_file() and p.suffix in {".md", ".txt"})


def display(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def main(argv: list[str]) -> int:
    sources = ref_files(SRC)
    if not sources:
        print("SKIPPED: sources/text/ 不存在或为空，跳过重合检查")
        return 0
    corpus: set[str] = set()
    for f in sources:
        corpus |= windows(norm_with_lines(f.read_text(errors="ignore"))[0])
    official = ref_files(OFFICIAL)
    for f in official:
        corpus -= windows(norm_with_lines(f.read_text(errors="ignore"))[0])

    targets: list[Path] = []
    for a in argv or ["skills"]:
        p = Path(a) if Path(a).is_absolute() else ROOT / a
        if p.is_dir():
            targets += sorted(x for x in p.rglob("*") if x.is_file() and x.suffix in SUFFIXES)
        elif p.is_file():
            targets.append(p)

    hits = 0
    for f in targets:
        s, lines = norm_with_lines(f.read_text(errors="ignore"))
        reported: set[int] = set()
        for i in range(len(s) - N + 1):
            if s[i : i + N] in corpus:
                lineno = lines[i]
                if lineno not in reported:
                    reported.add(lineno)
                    hits += 1
                    print(f"{display(f)}:{lineno}: 与参考资料连续重合 ≥{N} 字")
    print(f"参考资料 {len(sources)} 份，官方文件 {len(official)} 份，检查 {len(targets)} 个文件")
    if hits:
        print(f"FAIL: {hits} 处与参考资料连续重合 ≥{N} 字")
        return 1
    print(f"OK: 无 ≥{N} 字连续重合")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
