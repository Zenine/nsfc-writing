#!/usr/bin/env bash
# 一行安装：把 skills/nsfc-writing 装到本机 agent 的 skills 目录。
set -euo pipefail

USAGE='用法：
  curl -fsSL https://raw.githubusercontent.com/Zenine/nsfc-writing/main/scripts/install.sh | bash
  curl -fsSL .../install.sh | bash -s -- --link          # 克隆后软链接，便于 git pull 更新
  curl -fsSL .../install.sh | REF=v0.1.2 bash            # 安装指定版本
环境变量：
  TARGET=claude|codex|all   默认 all：装到已存在的 ~/.claude 与 ${CODEX_HOME:-~/.codex}
  DEST=<skills 目录>        自定义 skills 目录，实际安装到 <skills 目录>/nsfc-writing（此时忽略 TARGET）
  REF=<分支或 tag>          默认 main
参数：
  --link   不复制，改为 git clone 到 ${XDG_DATA_HOME:-~/.local/share}/nsfc-writing 并软链接
  --help   显示本说明'

REPO="Zenine/nsfc-writing"
NAME="nsfc-writing"
REF="${REF:-main}"
TARGET="${TARGET:-all}"
DEST="${DEST:-}"
MODE="copy"
for a in "$@"; do
  case "$a" in
    --link) MODE="link" ;;
    --help|-h) printf '%s\n' "$USAGE"; exit 0 ;;
    *) printf '未知参数：%s\n\n%s\n' "$a" "$USAGE" >&2; exit 1 ;;
  esac
done

if [[ ! "$REF" =~ ^[A-Za-z0-9][A-Za-z0-9._/-]*$ ]] || [[ "$REF" == *..* ]] || [[ "$REF" == */ ]] || [[ "$REF" == /* ]]; then
  echo "REF 只能是安全的分支或 tag 名称" >&2
  exit 1
fi
if [ -z "$DEST" ] && [[ ! "$TARGET" =~ ^(all|claude|codex)$ ]]; then
  echo "TARGET 只能是 all、claude 或 codex，收到：$TARGET" >&2
  exit 1
fi

codex_home="${CODEX_HOME:-$HOME/.codex}"
dests=()
if [ -n "$DEST" ]; then
  dests+=("${DEST%/}/$NAME")
else
  [[ "$TARGET" =~ ^(all|claude)$ ]] && [ -d "$HOME/.claude" ] && dests+=("$HOME/.claude/skills/$NAME")
  [[ "$TARGET" =~ ^(all|codex)$ ]] && [ -d "$codex_home" ] && dests+=("$codex_home/skills/$NAME")
fi
[ ${#dests[@]} -gt 0 ] || { echo "未找到 ~/.claude 或 $codex_home，请用 DEST=<skills 目录> 指定安装位置" >&2; exit 1; }

# 目标已存在时，只允许替换本 skill 的旧版本，避免误删其他目录。
for d in "${dests[@]}"; do
  if [ -L "$d" ]; then continue; fi
  if [ -e "$d" ]; then
    if [ ! -f "$d/SKILL.md" ] || ! grep -q "^name: $NAME\$" "$d/SKILL.md"; then
      echo "目标已存在且不是 $NAME：$d，已停止，未做任何改动" >&2
      exit 1
    fi
  fi
done

src_root=""
prev_head=""
fresh_clone=0
if [ "$MODE" = "link" ]; then
  src_root="${XDG_DATA_HOME:-$HOME/.local/share}/$NAME"
  if [ -d "$src_root/.git" ]; then
    prev_head="$(git -C "$src_root" rev-parse HEAD 2>/dev/null || true)"
    git -C "$src_root" fetch -q --depth 1 origin "$REF"
    git -C "$src_root" checkout -q --detach FETCH_HEAD
  else
    git clone -q --depth 1 -b "$REF" "https://github.com/$REPO.git" "$src_root"
    fresh_clone=1
  fi
  src="$src_root/skills/$NAME"
else
  tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
  src=""
  if curl -fsSL "https://codeload.github.com/$REPO/tar.gz/$REF" | tar -xz -C "$tmp" 2>/dev/null; then
    candidate="$(find "$tmp" -maxdepth 1 -mindepth 1 -type d | head -1)/skills/$NAME"
    [ -f "$candidate/SKILL.md" ] && src="$candidate"
  fi
  [ -n "$src" ] || { echo "下载或解包失败：$REPO@$REF" >&2; exit 1; }
fi
[ -f "$src/SKILL.md" ] || { echo "源里没有 SKILL.md：$src" >&2; exit 1; }

backups=()
restore_all() {
  local i d backup
  for ((i = 0; i < ${#backups[@]}; i++)); do
    d="${dests[$i]}"
    backup="${backups[$i]}"
    if [ -e "$d" ] || [ -L "$d" ]; then rm -rf "$d"; fi
    [ -z "$backup" ] || mv "$backup" "$d"
  done
  if [ "$MODE" = "link" ]; then
    if [ -n "$prev_head" ]; then
      git -C "$src_root" checkout -q --detach "$prev_head" || true
    elif [ "$fresh_clone" = 1 ]; then
      rm -rf "$src_root"
    fi
  fi
}
prepare_failed() {
  local d="$1" partial_backup="${2:-}"
  [ -z "$partial_backup" ] || rm -rf "$partial_backup" || true
  restore_all
  echo "安装失败，已保留原有 skill：$d" >&2
  exit 1
}

for d in "${dests[@]}"; do
  parent="$(dirname "$d")"
  if ! mkdir -p "$parent"; then prepare_failed "$d"; fi
  backup=""
  if [ -e "$d" ] || [ -L "$d" ]; then
    if ! backup="$(mktemp -d "$parent/.$NAME-backup.XXXXXX")"; then prepare_failed "$d"; fi
    if ! rmdir "$backup"; then prepare_failed "$d" "$backup"; fi
    if ! mv "$d" "$backup"; then prepare_failed "$d" "$backup"; fi
  fi
  backups+=("$backup")
done

for i in "${!dests[@]}"; do
  d="${dests[$i]}"
  if [ "$MODE" = "link" ]; then
    if ln -s "$src" "$d"; then continue; fi
  else
    if cp -r "$src" "$d"; then continue; fi
  fi
  restore_all
  echo "安装失败，已保留原有 skill：$d" >&2
  exit 1
done

for backup in "${backups[@]}"; do
  [ -z "$backup" ] || rm -rf "$backup"
done
for d in "${dests[@]}"; do
  if [ "$MODE" = "link" ]; then echo "已软链接 → $d"; else echo "已安装 → $d"; fi
done
echo "完成。新开会话后说“帮我诊断一下这段立项依据”即可触发 $NAME。"
