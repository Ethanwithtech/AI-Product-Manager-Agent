#!/usr/bin/env python3
"""
浏览器截图工具 — 使用 Playwright 对网页进行截图。

支持三种模式：
1. 全页截图（默认）
2. 可视区域截图
3. 指定 CSS 选择器元素截图

依赖：pip3 install playwright && python3 -m playwright install chromium

用法：
    python screenshot.py <url> [options]

示例：
    # 全页截图
    python screenshot.py https://example.com

    # 可视区域截图
    python screenshot.py https://example.com --viewport-only

    # 指定元素截图
    python screenshot.py https://example.com --selector ".main-content"

    # 自定义视口大小和输出路径
    python screenshot.py https://example.com --width 1440 --height 900 --output ./my-screenshot.png

    # 等待特定元素加载后再截图
    python screenshot.py https://example.com --wait-for ".loaded-indicator"

    # 模拟移动端
    python screenshot.py https://example.com --device "iPhone 13"
"""

import argparse
import os
import sys
import time
from datetime import datetime
from pathlib import Path


def require_playwright():
    """检查 Playwright 是否已安装。"""
    try:
        from playwright.sync_api import sync_playwright
        return sync_playwright
    except ImportError:
        print(
            "错误: 需要安装 Playwright。运行:\n"
            "  pip3 install playwright && python3 -m playwright install chromium",
            file=sys.stderr,
        )
        sys.exit(1)


def generate_output_path(url, output_dir="./screenshots"):
    """根据 URL 和时间戳生成输出文件路径。"""
    from urllib.parse import urlparse
    parsed = urlparse(url)
    domain = parsed.hostname or "unknown"
    domain = domain.replace(".", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(output_dir, exist_ok=True)
    return os.path.join(output_dir, f"{domain}_{timestamp}.png")


def take_screenshot(
    url,
    output=None,
    full_page=True,
    selector=None,
    width=1280,
    height=720,
    wait_for=None,
    wait_timeout=30000,
    device=None,
    delay=0,
    cookie_file=None,
):
    """
    对指定 URL 进行截图。

    参数:
        url: 目标网页 URL
        output: 输出文件路径（None 则自动生成）
        full_page: 是否全页截图
        selector: CSS 选择器（截取特定元素）
        width: 视口宽度
        height: 视口高度
        wait_for: 等待某个 CSS 选择器出现后再截图
        wait_timeout: 等待超时（毫秒）
        device: 模拟设备名称（如 "iPhone 13"）
        delay: 截图前额外等待秒数
        cookie_file: Cookie JSON 文件路径
    
    返回:
        截图文件的绝对路径
    """
    sync_playwright = require_playwright()

    if output is None:
        output = generate_output_path(url)

    # 确保输出目录存在
    os.makedirs(os.path.dirname(os.path.abspath(output)), exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # 设备模拟 or 自定义视口
        if device:
            device_desc = p.devices.get(device)
            if not device_desc:
                print(f"⚠️  未知设备 '{device}'，使用默认视口")
                context = browser.new_context(viewport={"width": width, "height": height})
            else:
                context = browser.new_context(**device_desc)
        else:
            context = browser.new_context(
                viewport={"width": width, "height": height},
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            )

        # 加载 Cookie
        if cookie_file and os.path.exists(cookie_file):
            import json
            with open(cookie_file, "r") as f:
                cookies = json.load(f)
            if isinstance(cookies, list):
                context.add_cookies(cookies)

        page = context.new_page()

        try:
            # 导航到页面
            page.goto(url, wait_until="networkidle", timeout=wait_timeout)

            # 等待特定元素
            if wait_for:
                page.wait_for_selector(wait_for, timeout=wait_timeout)

            # 额外等待
            if delay > 0:
                time.sleep(delay)

            # 截图
            if selector:
                element = page.query_selector(selector)
                if element:
                    element.screenshot(path=output)
                    print(f"✅ 元素截图已保存: {os.path.abspath(output)}")
                else:
                    print(f"⚠️  未找到选择器 '{selector}'，改为全页截图")
                    page.screenshot(path=output, full_page=True)
                    print(f"✅ 全页截图已保存: {os.path.abspath(output)}")
            else:
                page.screenshot(path=output, full_page=full_page)
                mode = "全页" if full_page else "可视区域"
                print(f"✅ {mode}截图已保存: {os.path.abspath(output)}")

        except Exception as e:
            print(f"❌ 截图失败: {e}", file=sys.stderr)
            browser.close()
            sys.exit(1)

        browser.close()

    return os.path.abspath(output)


def main():
    parser = argparse.ArgumentParser(
        description="浏览器截图工具 — 对网页进行截图",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("url", help="目标网页 URL")
    parser.add_argument("-o", "--output", help="输出文件路径 (默认: ./screenshots/<domain>_<timestamp>.png)")
    parser.add_argument("--viewport-only", action="store_true", help="仅截取可视区域（默认全页）")
    parser.add_argument("--selector", "-s", help="截取指定 CSS 选择器元素")
    parser.add_argument("--width", type=int, default=1280, help="视口宽度 (默认: 1280)")
    parser.add_argument("--height", type=int, default=720, help="视口高度 (默认: 720)")
    parser.add_argument("--wait-for", help="等待指定 CSS 选择器出现后再截图")
    parser.add_argument("--wait-timeout", type=int, default=30000, help="等待超时毫秒数 (默认: 30000)")
    parser.add_argument("--device", help="模拟设备 (如 'iPhone 13', 'iPad Pro 11')")
    parser.add_argument("--delay", type=float, default=0, help="截图前额外等待秒数")
    parser.add_argument("--cookies", help="Cookie JSON 文件路径")

    args = parser.parse_args()

    take_screenshot(
        url=args.url,
        output=args.output,
        full_page=not args.viewport_only,
        selector=args.selector,
        width=args.width,
        height=args.height,
        wait_for=args.wait_for,
        wait_timeout=args.wait_timeout,
        device=args.device,
        delay=args.delay,
        cookie_file=args.cookies,
    )


if __name__ == "__main__":
    main()
