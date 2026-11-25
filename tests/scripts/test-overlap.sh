#!/usr/bin/env bash
# check_overlap.py 的回归测试：用合成参考资料，不依赖本机 sources/。
set -euo pipefail
export LC_ALL=C.UTF-8

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
checker="$repo_root/scripts/check_overlap.py"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/src/text" "$tmp/src/official" "$tmp/target"

ref='春风拂过山岗溪水潺潺流向远方的村落炊烟袅袅升起映照着夕阳余晖'
printf '%s\n' "$ref" > "$tmp/src/text/ref.md"
printf '%s\n' '请勿删除或改动提纲标题及括号中的文字以免影响形式审查结果' > "$tmp/src/official/outline.txt"
printf '%s\n' '请勿删除或改动提纲标题及括号中的文字以免影响形式审查结果' >> "$tmp/src/text/ref.md"

# 硬换行拆成三行仍应命中。
printf '%s\n%s\n%s\n' "${ref:0:10}" "${ref:10:10}" "${ref:20}" > "$tmp/target/wrapped.md"
# 拆成两个各 19 字的列表项仍应命中。
printf -- '- %s\n- %s\n' "${ref:0:19}" "${ref:19:19}" > "$tmp/target/list.md"
# 与官方文件相同的片段不计。
printf '%s\n' '请勿删除或改动提纲标题及括号中的文字以免影响形式审查结果' > "$tmp/target/official.md"
# 句末标点处断开：两句各自不足 20 字，不应拼成命中。
printf '%s\n%s\n' "${ref:0:12}。" "${ref:12:12}。" > "$tmp/target/sentences.md"

out="$tmp/out"
if NSFC_SOURCES_DIR="$tmp/src" python3 "$checker" "$tmp/target" > "$out" 2>&1; then
  printf '失败：应检出重合\n' >&2; cat "$out" >&2; exit 1
fi
grep -q 'wrapped.md:1:' "$out" || { printf '失败：硬换行未检出\n' >&2; exit 1; }
grep -q 'list.md:1:' "$out" || { printf '失败：拆分列表项未检出\n' >&2; exit 1; }
if grep -q 'official.md' "$out"; then printf '失败：官方文件片段被误报\n' >&2; exit 1; fi
if grep -q 'sentences.md' "$out"; then printf '失败：跨句拼接误报\n' >&2; exit 1; fi

# 仓库外的绝对路径命中时不崩溃。
grep -q 'Traceback' "$out" && { printf '失败：出现异常堆栈\n' >&2; exit 1; }

# 缺少参考资料时跳过。
NSFC_SOURCES_DIR="$tmp/none" python3 "$checker" "$tmp/target" | grep -q '^SKIPPED:' || { printf '失败：缺资料时未跳过\n' >&2; exit 1; }

printf '%s\n' '重合检查回归测试通过'
