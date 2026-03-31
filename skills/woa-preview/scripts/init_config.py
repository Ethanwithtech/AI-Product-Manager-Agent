#!/usr/bin/env python3
"""
init_config.py - woa-preview skill 初始化配置
由 AI 在首次使用时调用，收集用户环境信息并写入 ~/.woa-preview-config.json

用法：
    python3 scripts/init_config.py \
        --username <gf_username> \
        --email <gf_email> \
        --cname <xxx.pages.woa.com> \
        [--preview-dir <path>] \
        [--repo-name <name>]

所有参数均可选，未提供的项保留已有值（或用默认值）。
运行后打印最终配置供 AI 确认。
"""

import argparse
import sys
from pathlib import Path

# 脚本自身目录，无论从哪里调用都能找到 config.py
sys.path.insert(0, str(Path(__file__).parent))
import config as cfg_mod


def main():
    parser = argparse.ArgumentParser(description="初始化 woa-preview 配置")
    parser.add_argument("--username",    help="工蜂用户名 (GF_USERNAME)")
    parser.add_argument("--email",       help="工蜂提交邮箱 (GF_EMAIL)")
    parser.add_argument("--cname",       help="pages.woa.com 子域名，如 myname.pages.woa.com")
    parser.add_argument("--preview-dir", help="本地项目目录，默认 ~/workspace/static-preview")
    parser.add_argument("--repo-name",   default="vuepress-preview", help="工蜂仓库名，默认 vuepress-preview")
    parser.add_argument("--show",        action="store_true", help="只显示当前配置，不修改")
    args = parser.parse_args()

    if args.show:
        cfg_mod.show()
        return

    # 加载已有配置（增量更新，不覆盖已有值）
    existing = cfg_mod.load()
    cfg = dict(cfg_mod.DEFAULTS)
    cfg.update(existing)

    if args.username:
        cfg["gf_username"] = args.username
    if args.email:
        cfg["gf_email"] = args.email
    if args.cname:
        cname = args.cname.strip()
        cfg["cname"] = cname
        cfg["base_url"] = f"https://{cname}"
    if args.preview_dir:
        cfg["preview_dir"] = str(Path(args.preview_dir).expanduser().resolve())
    if args.repo_name:
        cfg["repo_name"] = args.repo_name

    # 校验必填项（合并现有配置后再检查，增量更新时已有值算合法）
    missing = []
    if not cfg["gf_username"]:
        missing.append("--username")
    if not cfg["cname"]:
        missing.append("--cname")

    if missing:
        print(f"❌ 缺少必填参数：{', '.join(missing)}")
        print("   首次使用示例：")
        print("   python3 scripts/init_config.py --username zhangsan --email zhangsan@tencent.com --cname zhangsan.pages.woa.com")
        sys.exit(1)

    # 首次初始化时提示仍缺少的可选字段
    warnings = []
    if not cfg["gf_email"]:
        warnings.append("gf_email（--email）：git commit 需要，建议补充")
    if warnings:
        print("⚠️  以下字段未设置：")
        for w in warnings:
            print(f"   - {w}")
        print()

    cfg_mod.save(cfg)

    print(f"✅ 配置已保存到 {cfg_mod.CONFIG_PATH}")
    print()
    for k, v in cfg.items():
        print(f"   {k}: {v or '(未设置)'}")
    print()
    print("下一步：")
    if not Path(cfg["preview_dir"]).exists():
        print(f"  1. 初始化本地项目：mkdir -p {cfg['preview_dir']}")
        print(f"  2. 克隆或初始化仓库，参考 SKILL.md '首次使用' 章节")
    else:
        print(f"  项目目录已存在：{cfg['preview_dir']} ✅")
        print("  可直接使用 '新增文档' 或 '新增 Slides' 流程")


if __name__ == "__main__":
    main()
