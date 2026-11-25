#!/usr/bin/env bash
# 仓库验证入口。任一检查失败即非零退出。兼容 macOS 自带 bash 3.2。
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
  ok "(非 git 仓库，跳过)"
fi

echo "[2] skill 结构：frontmatter、SKILL.md 与 manifest.yaml 引用、版本号"
if python3 scripts/check_skill_structure.py; then :; else fail=1; fi

echo "[3] README 本地链接"
if python3 scripts/check_readme_links.py README.md README.en.md; then
  ok "README 本地链接"
else
  bad "README 本地链接"
fi

echo "[4] 与参考资料文本重合检查"
if overlap_output=$(python3 scripts/check_overlap.py skills tests docs README.md README.en.md .claude-plugin); then
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

echo "[5] 公开隐私扫描"
public_paths=""
for path in README.md README.en.md AGENTS.md CHANGELOG.md TODO.md LICENSE docs skills tests/fixtures tests/regression .claude-plugin; do
  [ -e "$path" ] && public_paths="$public_paths $path"
done
blacklist=""
[ -f .private/privacy-blacklist.txt ] && blacklist=".private/privacy-blacklist.txt"
# shellcheck disable=SC2086
if python3 scripts/check_public_privacy.py ${blacklist:+--blacklist "$blacklist"} $public_paths; then
  ok "公开文本无隐私风险"
else
  bad "发现公开隐私风险"
fi
if [ -n "$blacklist" ]; then
  if python3 scripts/check_public_privacy.py --only-blacklist --blacklist "$blacklist" scripts tests/scripts .github; then
    ok "脚本与配置无私有黑名单词"
  else
    bad "脚本与配置命中私有黑名单"
  fi
fi

echo
if [ "$fail" = 0 ]; then
  [ "$overlap_skipped" = 1 ] && echo "verify: PASS (overlap skipped)" || echo "verify: PASS"
else
  echo "verify: FAIL"
  exit 1
fi
