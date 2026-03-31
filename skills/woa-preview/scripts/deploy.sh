#!/usr/bin/env bash
# deploy.sh - 将 dist/ 产物安全部署到 oa-pages 分支
# 用法：bash scripts/deploy.sh
# 需要在 PREVIEW_DIR 根目录执行，或将 PREVIEW_DIR 作为第一个参数传入

set -euo pipefail

PREVIEW_DIR="${1:-$(python3 "$(dirname "$0")/config.py" 2>/dev/null || echo "")}"

# 如果没有通过参数传入，尝试从 config.json 读取
if [ -z "$PREVIEW_DIR" ]; then
  PREVIEW_DIR="$(python3 -c "
import sys; sys.path.insert(0,'$(dirname "$0")'); import config; print(config.get('preview_dir'))
" 2>/dev/null || echo "")"
fi

if [ -z "$PREVIEW_DIR" ] || [ ! -d "$PREVIEW_DIR" ]; then
  echo "❌ 找不到项目目录。请先初始化配置："
  echo "   python3 scripts/init_config.py --username <gf_username> --cname <xxx.pages.woa.com>"
  exit 1
fi

DIST_DIR="$PREVIEW_DIR/dist"
DEPLOY_TMP="/tmp/woa-preview-deploy-$$"

# ── 检查前置条件 ─────────────────────────────────────────────────────────────
if [ ! -d "$DIST_DIR" ]; then
  echo "❌ 产物目录不存在：$DIST_DIR"
  echo "   请先运行：cd $PREVIEW_DIR && npm run build"
  exit 1
fi

if [ ! -f "$DIST_DIR/index.html" ]; then
  echo "❌ 产物不完整（缺少 index.html），请重新构建"
  exit 1
fi

echo "🚀 开始部署..."
echo "   产物目录：$DIST_DIR"

# ── 把产物复制到临时目录（避免 git checkout 时被清掉）─────────────────────────
cp -r "$DIST_DIR" "$DEPLOY_TMP"
echo "   已备份产物到：$DEPLOY_TMP"

cd "$PREVIEW_DIR"

# ── 确保工作区干净后再切换分支 ────────────────────────────────────────────────
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "⚠️  工作区有未提交改动，先 stash..."
  git stash push -m "deploy: auto-stash before oa-pages deploy"
  STASHED=1
else
  STASHED=0
fi

# ── 切到 oa-pages 分支 ────────────────────────────────────────────────────────
git checkout oa-pages
git pull origin oa-pages --rebase 2>/dev/null || true

# ── 清理旧产物（只清 PREVIEW_DIR 根目录下的非 .git 文件）────────────────────────
echo "   清理旧产物..."
cd "$PREVIEW_DIR"
for item in "$PREVIEW_DIR"/.[!.]* "$PREVIEW_DIR"/*; do
  name="$(basename "$item")"
  [ "$name" = ".git" ] && continue
  [ -e "$item" ] || continue
  rm -rf "$item"
done

# ── 复制新产物 ────────────────────────────────────────────────────────────────
cp -r "$DEPLOY_TMP"/. "$PREVIEW_DIR/"
rm -rf "$DEPLOY_TMP"

# ── 提交并推送 ────────────────────────────────────────────────────────────────
git add -A
CHANGED=$(git diff --cached --stat | tail -1)
if git diff --cached --quiet; then
  echo "ℹ️  产物无变化，跳过提交"
else
  TIMESTAMP="$(date '+%Y-%m-%d %H:%M')"
  git commit -m "deploy: update $TIMESTAMP"
  git push origin oa-pages
  echo "✅ 部署完成！$CHANGED"
fi

# ── 切回 main ─────────────────────────────────────────────────────────────────
git checkout main

# ── 恢复 stash ────────────────────────────────────────────────────────────────
if [ "$STASHED" = "1" ]; then
  git stash pop && echo "   已恢复 stash"
fi

# ── 报告 ─────────────────────────────────────────────────────────────────────
BASE_URL="$(python3 -c "
import sys; sys.path.insert(0,'$(dirname "$0")'); import config; print(config.get('base_url',''))
" 2>/dev/null || echo "")"

echo ""
echo "🎉 部署结果："
echo "   🔗 ${BASE_URL:-（域名未配置）}"
if [ -d "$PREVIEW_DIR/dist/slides" ]; then
  for D in "$PREVIEW_DIR"/dist/slides/*/; do
    NAME="$(basename "$D")"
    echo "   🎯 ${BASE_URL}/slides/${NAME}/"
  done
fi
