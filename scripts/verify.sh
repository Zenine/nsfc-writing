#!/usr/bin/env bash
# 仓库验证入口。任一检查失败即非零退出。
set -uo pipefail
cd "$(dirname "$0")/.."
fail=0
overlap_skipped=0
ok()   { echo "  PASS $*"; }
bad()  { echo "  FAIL $*"; fail=1; }

echo "[1] 参考资料与私有文件未被 git 跟踪"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  pattern='(\.(pdf|pptx|docx|mp4)$|^sources/|^\.private/)'
  tracked=$(git ls-files | grep -Ei "$pattern" || true)
  [ -z "$tracked" ] && ok "已跟踪文件干净" || bad "被跟踪: $tracked"
  staged=$(git diff --cached --name-only | grep -Ei "$pattern" || true)
  [ -z "$staged" ] && ok "暂存区干净" || bad "暂存区含: $staged"
else
  ok "(非 git 仓库,跳过)"
fi

SKILL_DIR=skills/nsfc-writing
SKILL=$SKILL_DIR/SKILL.md
MANIFEST=$SKILL_DIR/manifest.yaml
echo "[2] SKILL.md frontmatter"
if [ -f "$SKILL" ]; then
  head -n 5 "$SKILL" | grep -q '^name: nsfc-writing$' && ok "name" || bad "缺 name: nsfc-writing"
  desc=$(head -n 5 "$SKILL" | sed -n 's/^description: //p')
  [ -n "$desc" ] && ok "description" || bad "缺 description"
  len=$(printf '%s' "$desc" | python3 -c 'import sys; print(len(sys.stdin.read()))')
  [ "$len" -le 1024 ] && ok "description 长度 $len ≤ 1024" || bad "description 过长: $len"
else
  bad "缺 $SKILL"
fi

echo "[3] 片段文件与 SKILL.md、manifest.yaml 互相引用"
for f in "$SKILL_DIR"/core/*.md "$SKILL_DIR"/sections/*.md "$SKILL_DIR"/references/*.md; do
  rel=${f#"$SKILL_DIR"/}
  grep -q "$rel" "$SKILL" && ok "SKILL.md 引用 $rel" || bad "SKILL.md 未引用 $rel"
  grep -q "$rel" "$MANIFEST" && ok "manifest 引用 $rel" || bad "manifest 未引用 $rel"
done
for rel in $(grep -ohE '(core|sections|references)/[A-Za-z0-9_-]+\.md' "$SKILL" "$MANIFEST" | sort -u); do
  [ -f "$SKILL_DIR/$rel" ] && ok "存在 $rel" || bad "引用了不存在的 $rel"
done

echo "[4] README 本地链接"
if python3 scripts/check_readme_links.py README.md README.en.md; then
  ok "README 本地链接"
else
  bad "README 本地链接"
fi

echo "[5] 与参考资料文本重合检查"
if overlap_output=$(python3 scripts/check_overlap.py skills tests/fixtures README.md README.en.md); then
  printf '%s\n' "$overlap_output"
  if printf '%s\n' "$overlap_output" | grep -q '^SKIPPED:'; then
    overlap_skipped=1
  else
    ok "overlap"
  fi
else
  printf '%s\n' "$overlap_output"
  bad "overlap"
fi

echo "[6] 公开隐私扫描"
public_paths=()
for path in README.md README.en.md AGENTS.md CHANGELOG.md TODO.md docs skills tests/fixtures tests/regression .claude-plugin; do
  [ -e "$path" ] && public_paths+=("$path")
done
blacklist_args=()
[ -f .private/privacy-blacklist.txt ] && blacklist_args=(--blacklist .private/privacy-blacklist.txt)
if python3 scripts/check_public_privacy.py "${blacklist_args[@]}" "${public_paths[@]}"; then
  ok "公开文本无隐私风险"
else
  bad "发现公开隐私风险"
fi

echo
if [ "$fail" = 0 ]; then
  [ "$overlap_skipped" = 1 ] && echo "verify: PASS (overlap skipped)" || echo "verify: PASS"
else
  echo "verify: FAIL"
  exit 1
fi
