---
name: woa-preview
description: 将文档、报告、分析等内容发布到 pages.woa.com 静态预览服务。当用户表达出"希望预览/查看/分享某个文档或内容"的意图时触发，例如"帮我预览一下"、"发布出来看看"、"生成一个可访问的链接"、"我想在线查看这份报告"等。自动管理 vuepress-preview 工蜂仓库，检测已有内容避免重复创建，将内容构建为 VuePress 站点（文档）或 Slidev SPA（PPT）并通过 oa-pages 分支部署到 pages.woa.com。
---

# WOA Preview Skill

将任意文档或 PPT 发布到 `pages.woa.com` 静态预览服务。

## 触发时机

- "帮我预览一下" / "把这个发布出来" / "生成一个可以访问的链接"
- "我想在线看这份报告" / "做个 PPT 发出来" / "部署一下"
- "列一下目录" / "预览站里有什么"

---

## 脚本目录

所有脚本位于 skill 同目录的 `scripts/`：

| 脚本 | 用途 |
|------|------|
| `init_config.py` | 首次初始化：生成 `~/.woa-preview-config.json` |
| `config.py` | 配置读写公共模块（被其他脚本 import） |
| `list_contents.py` | 列出所有文档和 Slides |
| `deploy.sh` | 安全部署产物到 oa-pages 分支 |

> **配置文件**：`~/.woa-preview-config.json`（用户私有，不入 git）
> 存储：`preview_dir`、`gf_username`、`gf_email`、`base_url`、`cname`、`repo_name`

---

## 第一步：判断是否已初始化

**每次执行任务前先检查：**

```bash
python3 <skill_dir>/scripts/init_config.py --show
```

| 结果 | 处理方式 |
|------|---------|
| 显示完整配置 | 直接进入对应流程 |
| "尚未初始化" | 执行【初始化流程】 |
| 配置不完整（缺 username/cname）| 补充缺失项后重新运行 init_config.py |

> `<skill_dir>` 为本 SKILL.md 所在目录，使用时替换为绝对路径。

---

## 初始化流程（首次使用）

### 1. 收集必要信息

向用户询问（或从上下文推断）：

| 信息 | 说明 |
|------|------|
| 工蜂用户名 | 可通过 `mcporter call gongfeng.get_current_user` 自动获取 |
| 工蜂邮箱 | 提交用邮箱，如 `xxx@tencent.com` |
| pages 子域名 | 如 `yourname.pages.woa.com` |
| 本地目录（可选）| 默认 `~/workspace/static-preview` |

### 2. 写入配置

```bash
python3 <skill_dir>/scripts/init_config.py \
  --username <gf_username> \
  --email <gf_email> \
  --cname <xxx.pages.woa.com> \
  [--preview-dir <本地目录>]
```

### 3. 检查仓库状态

```bash
# 从配置读取变量
PREVIEW_DIR=$(python3 -c "import sys; sys.path.insert(0,'<skill_dir>/scripts'); import config; print(config.get('preview_dir'))")
GF_USERNAME=$(python3 -c "import sys; sys.path.insert(0,'<skill_dir>/scripts'); import config; print(config.get('gf_username'))")
REPO_NAME=$(python3 -c "import sys; sys.path.insert(0,'<skill_dir>/scripts'); import config; print(config.get('repo_name'))")
```

| 本地目录 | 工蜂仓库 | 处理 |
|---------|---------|------|
| ✅ 存在 | ✅ 存在 | `git pull`，进入内容流程 |
| ❌ 不存在 | ✅ 存在 | `git clone` 到本地 |
| ❌ 不存在 | ❌ 不存在 | 完整初始化（见下） |

### 4. 完整初始化（本地 + 远程均不存在时）

```bash
mkdir -p $PREVIEW_DIR && cd $PREVIEW_DIR
git init

npm install -D \
  vuepress@next vue \
  @vuepress/bundler-vite@next \
  @vuepress/theme-default@next \
  sass-embedded \
  @slidev/cli \
  @slidev/theme-default
```

创建目录结构：

```
$PREVIEW_DIR/
├── docs/
│   ├── .vuepress/
│   │   ├── config.js
│   │   └── public/
│   │       └── CNAME         ← 写入 <cname>
│   └── README.md             ← 首页
├── slides/                   ← Slidev PPT 目录
├── build.sh                  ← 一键构建脚本
├── .gitignore
└── package.json
```

**`docs/.vuepress/public/CNAME`**：写入 `<cname>`（从配置读取）

**`docs/.vuepress/config.js`**：
```js
import { viteBundler } from '@vuepress/bundler-vite'
import { defaultTheme } from '@vuepress/theme-default'
import { defineUserConfig } from 'vuepress'

export default defineUserConfig({
  bundler: viteBundler(),
  theme: defaultTheme({
    title: 'Preview',
    navbar: [{ text: '首页', link: '/' }],
    sidebar: [],
  }),
})
```

**`docs/README.md`**：
```markdown
# 文档预览站

## 文档列表

## Slides 演示

| 标题 | 日期 | 链接 |
|------|------|------|
```

**`.gitignore`**：
```
node_modules/
docs/.vuepress/.temp
docs/.vuepress/.cache
docs/.vuepress/dist
dist/
.slidev-tmp/
slides/**/node_modules/
slides/**/.slidev/
```

**`package.json` scripts**：
```json
{
  "scripts": {
    "docs:dev": "vuepress dev docs",
    "docs:build": "vuepress build docs",
    "slides:dev": "slidev slides/$npm_config_talk/slides.md",
    "build": "bash build.sh"
  }
}
```

**`build.sh`**：
```bash
#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DIST_DIR="$SCRIPT_DIR/dist"
SLIDES_DIST="$DIST_DIR/slides"

echo "🧹 清理旧产物..." && rm -rf "$DIST_DIR" && mkdir -p "$SLIDES_DIST"

echo "📚 构建 VuePress..." && cd "$SCRIPT_DIR" && npm run docs:build
cp -r docs/.vuepress/dist/. "$DIST_DIR/"

echo "🎯 构建 Slidev PPT..."
for TALK_DIR in "$SCRIPT_DIR/slides"/*/; do
  TALK_NAME="$(basename "$TALK_DIR")"
  SLIDES_MD="$TALK_DIR/slides.md"
  [ -f "$SLIDES_MD" ] || continue
  echo "  构建 $TALK_NAME..."
  SLIDEV_TMP="$SCRIPT_DIR/.slidev-tmp/$TALK_NAME"
  mkdir -p "$SLIDEV_TMP"
  cd "$TALK_DIR"
  [ -f "package.json" ] && npm install --prefer-offline 2>/dev/null || true
  npx slidev build slides.md --base "/slides/$TALK_NAME/" --out "$SLIDEV_TMP" 2>&1 | grep -v "^$" | sed 's/^/  /'
  cp -r "$SLIDEV_TMP/." "$SLIDES_DIST/$TALK_NAME/"
  echo "  ✅ $TALK_NAME"
done

rm -rf "$SCRIPT_DIR/.slidev-tmp"
echo "🎉 构建完成！产物在 dist/"
```

在工蜂创建仓库并初始提交：
```bash
mcporter call gongfeng.create_repository name="$REPO_NAME" description="静态预览站"

cd $PREVIEW_DIR
git config user.name "$GF_USERNAME"
git config user.email "$GF_EMAIL"
git remote add origin git@git.woa.com:$GF_USERNAME/$REPO_NAME.git
git branch -M main
git add -A && git commit -m "init: preview site"
git push -u origin main
```

### 5. 引导用户授权（仅首次）

> 请点击链接，将 `$REPO_NAME` 仓库授权给 pages.woa.com：
> 👉 **https://pages.woa.com/oauth/authorize**
>
> 授权完成后告诉我「好了」。

---

## 内容类型判断

| 内容 | 目标 | 文件路径 |
|------|------|---------|
| 文章 / 报告 / 分析 | VuePress 文档 | `docs/YYYY-MM-DD-topic.md` |
| PPT / 演示 / 幻灯片 | Slidev SPA | `slides/YYYY-MM-DD-topic/slides.md` |

---

## 流程一：新增 VuePress 文档

```bash
cd $PREVIEW_DIR && git checkout main && git pull origin main
```

1. 写入 `docs/<YYYY-MM-DD>-<slug>.md`
2. 更新 `docs/README.md` 文档列表，追加一行
3. 更新 `docs/.vuepress/config.js` sidebar，追加一项
4. 提交：`git add -A && git commit -m "docs: add <slug>" && git push origin main`

---

## 流程二：新增 Slidev PPT

```bash
cd $PREVIEW_DIR && git checkout main && git pull origin main
```

1. 创建 `slides/<YYYY-MM-DD>-<slug>/slides.md`（frontmatter 必须含 `title:` 和 `routerMode: hash`）

   **最小模板**：
   ```markdown
   ---
   theme: default
   title: PPT 标题
   routerMode: hash
   class: text-center
   transition: slide-left
   ---

   # 标题页

   副标题

   ---

   # 第二页

   内容...
   ```

   > ⚠️ `routerMode: hash` 必须加，否则静态服务直接访问 URL 时会 404（history 模式需要服务端重写规则）
2. 更新 `docs/README.md` 的 Slides 表格，追加一行：
   ```
   | PPT 标题 | YYYY-MM-DD | [查看](https://<cname>/slides/YYYY-MM-DD-slug/) |
   ```
3. 提交：`git add -A && git commit -m "slides: add <slug>" && git push origin main`

> Slidev 语法参考：https://cn.sli.dev

---

## 流程三：构建 + 部署

```bash
# 1. 一键构建
cd $PREVIEW_DIR && npm run build

# 2. 安全部署到 oa-pages
bash <skill_dir>/scripts/deploy.sh $PREVIEW_DIR
```

`deploy.sh` 会自动：
- 检查产物完整性
- stash 未提交改动（部署后恢复）
- 切换到 oa-pages，清理旧文件，复制新产物
- commit + push
- 切回 main，恢复 stash

---

## 查看目录

当用户问"有哪些文档/PPT"、"列一下目录"：

```bash
python3 <skill_dir>/scripts/list_contents.py
```

---

## 项目结构（参考）

```
$PREVIEW_DIR/
├── docs/                      ← VuePress 文档区
│   ├── .vuepress/config.js
│   ├── README.md              ← 首页
│   └── YYYY-MM-DD-topic.md
├── slides/                    ← Slidev PPT 区
│   └── YYYY-MM-DD-topic/
│       └── slides.md
├── build.sh
├── package.json
└── .gitignore

oa-pages 分支（产物）：
/              ← VuePress SPA
/slides/<name>/ ← 各 Slidev SPA
```

---

## 注意事项

- `~/.woa-preview-config.json` 不入 git，每台机器独立配置
- `oa-pages` 是孤立部署分支，绝不含 `node_modules/` 或源码
- Slidev 跨站链接用完整 URL（不同 SPA，不能用相对路径）
- git committer 需与工蜂账号匹配
