#!/usr/bin/env bash
# skill 内脚本的回归测试：count_chars.py 与 merge_pages.py。
set -euo pipefail
export LC_ALL=C.UTF-8

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
scripts="$repo_root/skills/nsfc-writing/scripts"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
fail() { printf '失败：%s\n' "$*" >&2; exit 1; }

# count_chars：空白不计，汉字与其他字符分开。
out="$(python3 "$scripts/count_chars.py" -t "粉砂 海床
ab，c")"
printf '%s\n' "$out" | grep -qx '合计（不含空白）：8' || fail "合计字数错误：$out"
printf '%s\n' "$out" | grep -qx '汉字：4' || fail "汉字数错误：$out"
printf '%s' "一二三" > "$tmp/t.md"
python3 "$scripts/count_chars.py" "$tmp/t.md" | grep -qx '合计（不含空白）：3' || fail '文件统计错误'

# merge_pages：需要 Pillow；缺少时跳过。
if ! python3 -c 'import PIL' 2>/dev/null; then
  printf '%s\n' 'skill 脚本回归测试通过（merge_pages 因缺少 Pillow 跳过）'
  exit 0
fi
mkdir -p "$tmp/pages"
python3 - "$tmp/pages" <<'PY'
import sys
from PIL import Image
for i in (1, 2, 10):
    Image.new("RGB", (40, 60), (i * 20, 0, 0)).save(f"{sys.argv[1]}/{i}.png")
PY
python3 "$scripts/merge_pages.py" "$tmp/pages" --name '测试/项目:名称' >/dev/null
pdf="$tmp/测试项目名称.pdf"
[ -f "$pdf" ] || fail '未按清洗后的项目名称生成 PDF'
python3 - "$pdf" <<'PY'
import sys
data = open(sys.argv[1], "rb").read()
assert data.count(b"/Type /Page") - data.count(b"/Type /Pages") == 3, "页数不是 3"
PY
# 输出已存在时默认拒绝覆盖。
if python3 "$scripts/merge_pages.py" "$tmp/pages" --name '测试/项目:名称' 2>/dev/null; then
  fail '未拒绝覆盖已有输出'
fi
python3 "$scripts/merge_pages.py" "$tmp/pages" --name '测试/项目:名称' --overwrite >/dev/null || fail '--overwrite 无效'
[ ! -e "$pdf.part" ] || fail '遗留临时文件'
# 元数据：默认写本机实际用户名；--author 可覆盖；不留库的默认值。
expected="$(git config user.name 2>/dev/null || true)"
[ -n "$expected" ] || expected="${USER:-$(id -un)}"
python3 - "$pdf" "$expected" <<'PY'
import sys
from PIL import Image  # noqa: F401  确认 Pillow 可用
data = open(sys.argv[1], "rb").read()
name = sys.argv[2]
utf16 = b"\xfe\xff" + name.encode("utf-16-be")
assert b"/Author" in data and b"/Creator" in data, "缺少 Author 或 Creator"
assert utf16 in data or b"(" + name.encode() + b")" in data, f"作者不是本机用户名 {name}"
assert b"(PIL)" not in data, "仍保留 PIL 默认值"
PY
python3 "$scripts/merge_pages.py" "$tmp/pages" --name '测试/项目:名称' --overwrite --author 'TestUser' >/dev/null
python3 - "$pdf" <<'PY' || fail '--author 未写入 PDF'
import sys
data = open(sys.argv[1], "rb").read()
assert b"\xfe\xff" + "TestUser".encode("utf-16-be") in data or b"(TestUser)" in data
PY

printf '%s\n' 'skill 脚本回归测试通过'
