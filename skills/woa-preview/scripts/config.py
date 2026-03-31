#!/usr/bin/env python3
"""
config.py - woa-preview skill 配置管理
读取/写入 ~/.woa-preview-config.json
"""

import json
import os
import subprocess
from pathlib import Path

CONFIG_PATH = Path.home() / ".woa-preview-config.json"

DEFAULTS = {
    "preview_dir": str(Path.home() / "workspace/static-preview"),
    "gf_username": "",
    "gf_email": "",
    "base_url": "",          # e.g. https://xxx.pages.woa.com
    "repo_name": "vuepress-preview",
    "cname": "",             # e.g. xxx.pages.woa.com
}


def load() -> dict:
    """加载配置，不存在则返回空 dict"""
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text())
        except Exception:
            pass
    return {}


def save(cfg: dict):
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2, ensure_ascii=False))


def get(key: str, fallback=None):
    cfg = load()
    return cfg.get(key, DEFAULTS.get(key, fallback))


def is_initialized() -> bool:
    cfg = load()
    return bool(cfg.get("gf_username") and cfg.get("base_url") and cfg.get("preview_dir"))


def show():
    """打印当前配置"""
    cfg = load()
    if not cfg:
        print("⚠️  尚未初始化，请先运行：python3 scripts/init_config.py")
        return
    print(f"📋 当前配置（{CONFIG_PATH}）")
    for k, v in cfg.items():
        print(f"   {k}: {v or '(未设置)'}")
