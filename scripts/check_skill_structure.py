#!/usr/bin/env python3
"""检查 skill 结构：frontmatter、SKILL.md 与 manifest.yaml 的文件集合、版本号一致。

不依赖 PyYAML：frontmatter 与 manifest 只做本仓库用到的简单解析。
退出码：0 通过；1 有问题。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "nsfc-writing"
PATH_RE = re.compile(r"(?:core|sections|references)/[A-Za-z0-9_-]+\.md")


def frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    data: dict[str, str] = {}
    key = None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            key, value = m.group(1), m.group(2).strip()
            data[key] = "" if value in {">", "|", ">-", "|-"} else value
        elif key and line.startswith((" ", "\t")):
            data[key] = (data[key] + " " + line.strip()).strip()
    return data


def main() -> int:
    errors: list[str] = []
    skill_text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    manifest_text = (SKILL_DIR / "manifest.yaml").read_text(encoding="utf-8")

    fm = frontmatter(skill_text)
    if fm.get("name") != "nsfc-writing":
        errors.append("SKILL.md frontmatter 缺 name: nsfc-writing")
    desc = fm.get("description", "")
    if not desc:
        errors.append("SKILL.md frontmatter 缺 description")
    elif len(desc) > 1024:
        errors.append(f"description 过长：{len(desc)} 字符")

    on_disk = {
        str(p.relative_to(SKILL_DIR))
        for sub in ("core", "sections", "references")
        for p in (SKILL_DIR / sub).glob("*.md")
    }
    in_skill = set(PATH_RE.findall(skill_text))
    in_manifest = set(PATH_RE.findall(manifest_text))
    for label, refs in (("SKILL.md", in_skill), ("manifest.yaml", in_manifest)):
        for missing in sorted(on_disk - refs):
            errors.append(f"{label} 未引用 {missing}")
        for ghost in sorted(refs - on_disk):
            errors.append(f"{label} 引用了不存在的 {ghost}")

    for script in sorted((SKILL_DIR / "scripts").glob("*.py")):
        rel = f"scripts/{script.name}"
        for label, text in (("SKILL.md", skill_text), ("manifest.yaml", manifest_text)):
            if rel not in text:
                errors.append(f"{label} 未引用 {rel}")

    m = re.search(r"^version:\s*(\S+)", manifest_text, re.M)
    manifest_version = m.group(1) if m else None
    plugin_version = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")).get("version")
    if manifest_version != plugin_version:
        errors.append(f"版本号不一致：manifest {manifest_version}，plugin.json {plugin_version}")

    for e in errors:
        print(f"  FAIL {e}")
    if errors:
        return 1
    print(f"  PASS frontmatter（description {len(desc)} 字符）、{len(on_disk)} 个片段双向引用、版本 {manifest_version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
