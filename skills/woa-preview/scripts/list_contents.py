#!/usr/bin/env python3
"""
list_contents.py - 列出 vuepress-preview 项目中所有文档和 Slides
用法：python3 scripts/list_contents.py [--preview-dir <path>]
      preview_dir 和 base_url 优先从 ~/.woa-preview-config.json 读取
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import config as cfg_mod


def extract_title(md_path: Path) -> str:
    """从 markdown 文件中提取标题（frontmatter title 优先，否则取第一个 # 标题）"""
    try:
        content = md_path.read_text(encoding="utf-8")
        if content.startswith("---"):
            end = content.find("---", 3)
            if end > 0:
                fm = content[3:end]
                m = re.search(r"^title:\s*(.+)$", fm, re.MULTILINE)
                if m:
                    return m.group(1).strip().strip('"\'')
        for line in content.splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    except Exception:
        pass
    return md_path.stem


def list_docs(preview_dir: Path, base_url: str) -> list:
    docs_dir = preview_dir / "docs"
    if not docs_dir.exists():
        return []

    results = []
    for md in sorted(docs_dir.rglob("*.md")):
        rel = md.relative_to(docs_dir)
        if ".vuepress" in rel.parts or md.name == "README.md":
            continue
        title = extract_title(md)
        url_path = "/" + str(rel).replace("\\", "/").removesuffix(".md") + ".html"
        results.append({"title": title, "file": str(rel), "url": base_url + url_path})

    return results


def list_slides(preview_dir: Path, base_url: str) -> list:
    slides_dir = preview_dir / "slides"
    if not slides_dir.exists():
        return []

    results = []
    for talk_dir in sorted(slides_dir.iterdir()):
        if not talk_dir.is_dir():
            continue
        slides_md = talk_dir / "slides.md"
        if not slides_md.exists():
            continue
        name = talk_dir.name
        title = extract_title(slides_md)
        results.append({"name": name, "title": title, "url": f"{base_url}/slides/{name}/"})

    return results


def main():
    parser = argparse.ArgumentParser(description="列出预览站所有内容")
    parser.add_argument("--preview-dir", help="本地项目目录（覆盖 config）")
    # 兼容旧式位置参数（SKILL.md 早期版本用法）
    parser.add_argument("positional", nargs="?", help=argparse.SUPPRESS)
    args = parser.parse_args()

    # ── 配置读取优先级：命令行 > config 文件 > 默认值 ──────────────────────────
    if not cfg_mod.is_initialized():
        print("⚠️  尚未初始化 woa-preview 配置。")
        print("   请先运行：python3 scripts/init_config.py --username <你的工蜂用户名> --cname <xxx.pages.woa.com>")
        print()
        print("   或者传入 --preview-dir 临时指定本地目录（base_url 将显示为 '未知'）")
        # 不直接退出，允许仅靠 --preview-dir 运行（方便调试）
        if not (args.preview_dir or args.positional):
            sys.exit(1)

    preview_dir_str = args.preview_dir or args.positional or cfg_mod.get("preview_dir")
    preview_dir = Path(preview_dir_str).expanduser().resolve()
    base_url = cfg_mod.get("base_url") or "https://<未配置域名>"

    if not preview_dir.exists():
        print(f"❌ 本地目录不存在：{preview_dir}")
        print("   请检查配置（python3 scripts/init_config.py --show）或传入正确的 --preview-dir")
        sys.exit(1)

    print(f"📁 预览站目录  ({base_url})")
    print(f"   本地路径：{preview_dir}")
    print()

    docs = list_docs(preview_dir, base_url)
    print(f"📚 文档 ({len(docs)} 篇)")
    if docs:
        for d in docs:
            print(f"   {d['title']}")
            print(f"     文件：{d['file']}")
            print(f"     链接：{d['url']}")
    else:
        print("   （暂无文档）")
    print()

    slides = list_slides(preview_dir, base_url)
    print(f"🎯 Slides ({len(slides)} 个)")
    if slides:
        for s in slides:
            print(f"   {s['title']}")
            print(f"     目录：slides/{s['name']}/")
            print(f"     链接：{s['url']}")
    else:
        print("   （暂无 Slides）")
    print()

    print(f"合计：{len(docs) + len(slides)} 个内容项")


if __name__ == "__main__":
    main()
