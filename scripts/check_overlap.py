#!/usr/bin/env python3
"""检查 skills/ 等公开文本与本机参考资料（sources/text/）是否存在长段连续重合。

中文按字符计：只保留汉字与数字，去掉空白、标点和拉丁字母后，任意连续 N 个字符（默认 20）与参考资料相同即报告；
与 sources/official/ 中官方公开文件相同的片段不计。
用法：python3 scripts/check_overlap.py <目录或文件>...
退出码：0 无重合（或缺少参考资料时 SKIPPED）；1 有重合。
"""
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources" / "text"
# 官方通告、申请书提纲等公开文件：与之相同的片段属于有意引用，不计为重合。
OFFICIAL = ROOT / "sources" / "official"
N = 20
KEEP = re.compile(r"[\u4e00-\u9fff0-9]")


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    return "".join(KEEP.findall(text))


def main(argv: list[str]) -> int:
    files = sorted(list(SRC.glob("*.md")) + list(SRC.glob("*.txt"))) if SRC.is_dir() else []
    if not files:
        print("SKIPPED: sources/text/ 不存在，跳过重合检查")
        return 0
    corpus = set()
    for f in files:
        s = norm(f.read_text(errors="ignore"))
        corpus.update(s[i : i + N] for i in range(len(s) - N + 1))
    if OFFICIAL.is_dir():
        for f in sorted(list(OFFICIAL.glob("*.md")) + list(OFFICIAL.glob("*.txt"))):
            s = norm(f.read_text(errors="ignore"))
            corpus.difference_update(s[i : i + N] for i in range(len(s) - N + 1))
    targets = []
    for a in argv or ["skills"]:
        p = Path(a) if Path(a).is_absolute() else ROOT / a
        if p.is_dir():
            targets += sorted(x for x in p.rglob("*") if x.suffix in {".md", ".yaml"})
        elif p.is_file():
            targets.append(p)
    hits = 0
    for f in targets:
        for lineno, line in enumerate(f.read_text(errors="ignore").splitlines(), 1):
            s = norm(line)
            for i in range(len(s) - N + 1):
                if s[i : i + N] in corpus:
                    hits += 1
                    print(f"{f.relative_to(ROOT)}:{lineno}: 与参考资料连续重合 ≥{N} 字")
                    break
    if hits:
        print(f"FAIL: {hits} 行与参考资料连续重合 ≥{N} 字")
        return 1
    print(f"OK: {len(targets)} 个文件无 ≥{N} 字连续重合")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
