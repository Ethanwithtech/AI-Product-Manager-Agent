#!/usr/bin/env python3
"""
读取企微文档内容（v2）。

新增支持：
  - 幻灯片（slide/p3_）：通过拦截 dop-api/slide/pages/get API，解析 protobuf 提取文字
  - 思维导图（mind/m4_）：通过全选复制获取缩进树形文本

原有支持：
  - 普通在线文档（doc/w3_、doc/e2_）：全选复制
  - 在线表格（sheet/e3_）：全选复制 + 多 Tab + 图片提取

用法:
    python3 read_doc_v2.py <doc_url> [选项]

选项:
    --with-images         提取表格中的图片（仅 sheet 类型有效）
    --list-tabs           列出表格所有 Sheet Tab（仅 sheet 类型有效）
    --tab <名称>          切换到指定 Tab（仅 sheet 类型有效）
    --slide-text-only     幻灯片模式：只输出纯文字，不含幻灯片编号（默认带编号）
    --timeout <秒>        超时时间，默认 60 秒
    --output <路径>       输出到文件（默认输出到 stdout）
    --cookie-file <路径>  Cookie 文件路径（默认 ~/.wecom-doc-cookies.json）

退出码:
    0  成功
    1  参数错误 / 依赖缺失
    2  Cookie 过期或无效
    3  内容提取失败
    4  无权限
"""

import argparse
import base64
import json
import os
import re
import sys
import time

# 将 scripts 目录加入路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common import (
    DEFAULT_COOKIE_FILE,
    activate_editor,
    check_login_required,
    check_no_permission,
    create_browser_context,
    get_modifier,
    load_cookies,
    normalize_cookies,
    request_permission,
    require_playwright,
    safe_goto,
    validate_url,
    wait_for_doc_render,
)

# 企微文档图片 CDN 域名模式
IMAGE_CDN_PATTERN = re.compile(r"wdoc.*\.picgzc\.qpic\.cn")

# ---------------------------------------------------------------------------
# 参数解析
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(description="读取企微文档内容（v2，支持 slide/mind）")
    parser.add_argument("doc_url", help="企微文档 URL")
    parser.add_argument("--with-images", action="store_true", default=False,
                        help="提取并下载表格中的图片（仅 sheet 类型）")
    parser.add_argument("--list-tabs", action="store_true", default=False,
                        help="列出在线表格所有 Sheet Tab 名称")
    parser.add_argument("--tab", default=None,
                        help="切换到指定名称的 Sheet Tab")
    parser.add_argument("--slide-text-only", action="store_true", default=False,
                        help="幻灯片模式：只输出纯文字，不含幻灯片编号")
    parser.add_argument("--timeout", type=int, default=60,
                        help="超时时间（秒），默认 60")
    parser.add_argument("--output", default=None,
                        help="输出文件路径（默认 stdout）")
    parser.add_argument("--cookie-file", default=DEFAULT_COOKIE_FILE,
                        help=f"Cookie 文件路径（默认: {DEFAULT_COOKIE_FILE}）")
    parser.add_argument("--request-access", action="store_true", default=False,
                        help="检测到无权限时自动申请访问权限")
    return parser.parse_args()


# ---------------------------------------------------------------------------
# 文档类型判断
# ---------------------------------------------------------------------------

def get_doc_type(url):
    """判断文档类型，返回 'doc' / 'sheet' / 'slide' / 'mind' / 'other'"""
    if "/slide/" in url or "/slide/" in url.lower():
        return "slide"
    if "/mind/" in url:
        return "mind"
    if "/sheet/" in url:
        return "sheet"
    if "/doc/" in url:
        return "doc"
    return "other"


# ---------------------------------------------------------------------------
# 提取文档标题
# ---------------------------------------------------------------------------

def extract_title(page):
    """从多个来源尝试提取文档标题。"""
    # 从 title input 获取（普通文档）
    title_el = page.query_selector("#melo-doc-title")
    if title_el:
        value = title_el.get_attribute("value") or ""
        if value.strip():
            return value.strip()

    # 从 window.basicClientVars 获取
    title = page.evaluate("""() => {
        try { return window.basicClientVars?.docInfo?.title || ''; }
        catch(e) { return ''; }
    }""")
    if title and title.strip():
        return title.strip()

    # 从页面 title 获取
    page_title = page.title()
    if page_title and "企业微信文档" not in page_title:
        return page_title.strip()

    return "未知标题"


# ---------------------------------------------------------------------------
# 通用：通过全选+复制提取文本
# ---------------------------------------------------------------------------

def extract_content_via_clipboard(page):
    """通过模拟全选+复制操作从剪贴板获取文档文本。"""
    modifier = get_modifier()
    activate_editor(page)
    page.keyboard.press(f"{modifier}+a")
    page.wait_for_timeout(2000)
    page.keyboard.press(f"{modifier}+c")
    page.wait_for_timeout(2000)
    text = page.evaluate("""async () => {
        try { return await navigator.clipboard.readText(); }
        catch (e) { return ''; }
    }""")
    return text or ""


# ---------------------------------------------------------------------------
# 表格：Sheet Tab 支持
# ---------------------------------------------------------------------------

def list_sheet_tabs(page):
    """获取在线表格底部所有 Sheet Tab 名称列表。"""
    tabs = page.evaluate('''() => {
        const all = document.querySelectorAll('*');
        const result = [];
        const seen = new Set();
        const excludes = new Set(['+', '▸', '▾', '◂', '▴', '...', '⋯']);
        for (const el of all) {
            const rect = el.getBoundingClientRect();
            if (rect.top > window.innerHeight - 80 && el.children.length === 0) {
                const text = (el.textContent || '').trim();
                if (text.length > 0 && text.length < 50
                    && !seen.has(text) && !excludes.has(text)) {
                    seen.add(text);
                    result.push(text);
                }
            }
        }
        return result;
    }''')
    return [t for t in tabs if not re.match(r'^[\d\s\+\-\*\/\.\,\:]+$', t)]


def switch_to_tab(page, tab_name):
    """点击指定名称的 Sheet Tab。"""
    try:
        tab_el = page.locator(f'text="{tab_name}"').last
        if tab_el.is_visible(timeout=3000):
            tab_el.click()
            page.wait_for_timeout(2000)
            return True
    except Exception:
        pass
    return False


# ---------------------------------------------------------------------------
# 表格：图片提取
# ---------------------------------------------------------------------------

def scroll_to_capture_images(page, image_urls_captured):
    """滚动页面以触发所有图片加载。"""
    # 纵向滚动
    viewport = page.viewport_size or {"width": 1280, "height": 900}
    page_height = page.evaluate("document.body.scrollHeight") or 10000
    scroll_step = viewport["height"] - 100
    y = 0
    while y < page_height:
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(300)
        y += scroll_step
    # 横向滚动
    page_width = page.evaluate("document.body.scrollWidth") or 5000
    scroll_step_x = viewport["width"] - 100
    x = 0
    while x < page_width:
        page.evaluate(f"window.scrollTo({x}, 0)")
        page.wait_for_timeout(200)
        x += scroll_step_x
    # 回到顶部
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(1000)


def get_original_image_url(thumbnail_url):
    """从缩略图 URL 获取原图 URL（去掉缩略图参数）。"""
    return re.sub(r'\?.*$', '', thumbnail_url)


# ---------------------------------------------------------------------------
# 幻灯片：从 protobuf 数据提取文本
# ---------------------------------------------------------------------------

def extract_texts_from_slide_proto(b64_data):
    """
    从 Base64 编码的 protobuf 幻灯片数据中提取中文和英文文本。
    
    企微幻灯片 API 返回的 data 字段是 Base64 编码的 protobuf，
    其中文本以 UTF-8 字符串形式存储在 protobuf 字段中。
    通过解码后按控制字符分割，可以提取出可读文本。
    """
    padded = b64_data + '=' * (4 - len(b64_data) % 4)
    try:
        raw = base64.b64decode(padded)
    except Exception:
        return []

    text = raw.decode('utf-8', errors='replace')
    
    # 按二进制控制字符分割
    segments = re.split(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f\ufffd\xff]+', text)
    
    results = []
    
    for seg in segments:
        seg = seg.strip()
        if len(seg) < 2:
            continue
        
        # 先清理首部的 protobuf 长度前缀（通常是 1-3 个非字母数字字符）
        seg = re.sub(r'^[:*\+\-\=\>\<\(\)\[\]\{\}@#\$%\^&\s]{1,4}', '', seg).strip()
        # 清理句首单个大写字母前缀（后接中文时是 protobuf 字段长度标记，如 D、L、N 后接中文）
        seg = re.sub(r'^[A-Z0-9]{1}(?=[\u4e00-\u9fff])', '', seg)
        # 清理末尾的单字母后缀（如 B, Ba, B%, B" 等 protobuf 字段标记残留）
        seg = re.sub(r'\s*B[a-z%"\'*\s]{0,2}$', '', seg).strip()
        # 清理末尾的 rel: 引用和 * 字符
        seg = re.sub(r'\s*rel:[a-f0-9\*]+$', '', seg).strip()
        if len(seg) < 2:
            continue
        
        # === 噪音过滤 ===
        
        # 1. 字体名（TencentSans、Arial、微软雅黑 等字体相关，也包含被截断版本）
        if re.match(r'^(TencentSans|encentSans|tSans|entSans|Arial|Helvetica|Calibri|SimSun|SimHei|微软雅黑|宋体|黑体|仿宋|楷体)', seg):
            continue
        
        # 2. 纯语言代码
        if re.match(r'^(zh-CN|en-US|zh-TW|en-GB|ja-JP)$', seg):
            continue
        
        # 3. 纯 hex hash（8位以上全小写十六进制）
        if re.match(r'^[a-f0-9]{6,}[*(\[\{]?$', seg):
            continue
        
        # 4. 尺寸/坐标格式 如 9*5, 222*S, 223*R
        if re.match(r'^\d+[\*x×]\d*[A-Z]?$', seg):
            continue
        
        # 5. 颜色码（如 FF0000, 5C5C5C, A2C0FB, 1772FB）
        if re.match(r'^[0-9A-Fa-f]{6}(P|[A-Z])?$', seg):
            continue
        
        # 6. 单个字母或短无意义符号串
        if re.match(r'^[A-Z]{1,2}$', seg) or re.match(r'^[a-z]{1,2}$', seg):
            continue
        
        # 7. URL 和 base64 图片数据
        if re.match(r'^https?://', seg) or re.match(r'^data:image/', seg):
            continue
        
        # 8. 包含 hash 格式 ID 的节点引用（如 ccd3bac5(、d4c1e8bf*）
        if re.match(r'^[a-f0-9]{6,}[\*\(\[\{:"J\+]', seg):
            continue
        
        # 8b. hex id + 末尾引号/J/冒号 等（如 5923eaef"、e45591acJ、fda63ea9J、2a8d3d38:）
        if re.match(r'^[a-f0-9]{7,}["\'J\+\:]?$', seg):
            continue
        
        # 8c. 短 hash 引用带后缀（如 3d5edf6*`、74dbfdf*+）
        if re.match(r'^[a-f0-9]{5,}[\*`\+\-\.]+', seg):
            continue
        
        # 8d. 只含字母数字加上 *`H 等（如 H*）
        if re.match(r'^[A-Z]{1}[\*`\+]{1}$', seg):
            continue
        
        # 8e. GUID 格式残留（如 22544A-7EE6-4342-B048-85BDC9FD1C3A}）
        if re.match(r'^[0-9A-Fa-f]{4,}-[0-9A-Fa-f]{4}-', seg):
            continue
        
        # 9. 形状/占位符名称（如 "矩形 9*5", "圆角矩形 223*S", "备注占位符 25", "标题 1"）
        if re.match(r'^(矩形|圆角矩形|椭圆|文本框|备注占位符|SmartArt)\s*[\d\*]', seg):
            continue
        if re.match(r'^标题\s+\d+$', seg):
            continue
        
        # 10. 过滤纯空白和纯标点
        if not re.search(r'[\w\u4e00-\u9fff]', seg):
            continue
        
        # 11. 过滤疑似内存地址或版本号（全为数字点格式，或纯数字）
        if re.match(r'^[\d\.]+$', seg):
            continue
        
        # 12. 过滤类属性名（以小写+数字开头，短且无中文）
        if len(seg) <= 6 and re.match(r'^[a-z][a-zA-Z0-9]+$', seg) and not any('\u4e00' <= c <= '\u9fff' for c in seg):
            continue
        
        # === 内容检查：必须有实质内容 ===
        has_chinese = any('\u4e00' <= c <= '\u9fff' for c in seg)
        # 有意义英文：包含字母单词（至少3字符）且不是纯编码
        has_meaningful_en = bool(re.search(r'[a-zA-Z]{3,}', seg)) and (
            ' ' in seg or 
            any('\u4e00' <= c <= '\u9fff' for c in seg) or
            len(seg) > 8
        )
        # 代码片段（含括号、等号等代码特征）
        is_code = bool(re.search(r'[(){}\[\]=><]', seg)) and bool(re.search(r'[a-zA-Z_]', seg))
        
        if has_chinese or has_meaningful_en or (is_code and len(seg) > 10):
            # 清理末尾的引号残留
            seg = seg.rstrip('"\'').strip()
            if len(seg) >= 2:
                results.append(seg)
    
    # 去重，保持顺序
    seen = set()
    unique = []
    for t in results:
        if t not in seen:
            seen.add(t)
            unique.append(t)
    
    return unique


def read_slide(page, args, timeout_ms):
    """
    读取幻灯片文档内容。
    
    策略：拦截 dop-api/slide/pages/get API 响应，
    解析 protobuf data 字段提取文字。
    同时在页面加载时滚动缩略图列表以触发所有批次数据加载。
    """
    print("检测到幻灯片类型，使用 API 拦截模式...", file=sys.stderr, flush=True)
    
    # 从 URL 提取 padId
    pad_id_match = re.search(r'/slide/(p3_\w+)', args.doc_url)
    if not pad_id_match:
        pad_id_match = re.search(r'padId=(p3_\w+)', args.doc_url)
    pad_id = pad_id_match.group(1) if pad_id_match else None
    
    # 收集所有 slide pages API 响应
    all_pages_data = {}  # start_index -> {total, count, data}
    
    def on_resp(r):
        u = r.url
        if 'dop-api/slide/pages/get' in u:
            try:
                body = r.body()
                resp = json.loads(body)
                data_obj = resp.get('data', {})
                start_idx = data_obj.get('start_index', 0)
                all_pages_data[start_idx] = data_obj
            except Exception as e:
                print(f"解析 slide API 失败: {e}", file=sys.stderr)
    
    page.on('response', on_resp)
    
    print(f"正在加载幻灯片: {args.doc_url}", file=sys.stderr, flush=True)
    safe_goto(page, args.doc_url, timeout_ms)
    page.wait_for_timeout(4000)
    
    # 检查登录
    if check_login_required(page):
        print("错误: Cookie 已过期，请重新运行 export_cookies.py", file=sys.stderr)
        sys.exit(2)
    
    # 检查权限
    perm_result = check_no_permission(page)
    if not perm_result["has_permission"]:
        perm_msg = perm_result.get("message", "无权限访问")
        if args.request_access and perm_result.get("can_request"):
            request_permission(page)
        print(f"错误: {perm_msg}", file=sys.stderr)
        sys.exit(4)
    
    title = extract_title(page)
    
    # 获取总页数
    total_slides = 0
    for data_obj in all_pages_data.values():
        total_slides = max(total_slides, data_obj.get('total', 0))
    
    if total_slides == 0:
        # 尝试从页面获取
        try:
            status_text = page.inner_text('p.status-bar-pageInfos-32WyL', timeout=3000)
            m = re.search(r'共\s*(\d+)\s*页', status_text)
            if m:
                total_slides = int(m.group(1))
        except Exception:
            total_slides = 100  # 默认值
    
    print(f"文档共 {total_slides} 页，开始滚动加载所有页面数据...", file=sys.stderr, flush=True)
    
    # 滚动缩略图列表以触发所有页面批次加载
    # 企微幻灯片每次加载 10 页，需要滚动触发
    print("滚动缩略图列表以触发所有页面加载...", file=sys.stderr, flush=True)
    
    # 先滚到顶部，触发头部页面数据
    page.evaluate("""
        const el = document.querySelector('.pre-slide-list-container');
        if (el) el.scrollTop = 0;
    """)
    page.wait_for_timeout(1000)
    
    # 逐步向下滚动缩略图列表，每次滚一屏，触发懒加载
    # 每页缩略图大约 120px 高，10 页 = 1200px
    step = 1200
    max_scroll = max(total_slides * 130, 15000)
    scroll_pos = 0
    
    while scroll_pos <= max_scroll:
        page.evaluate(f"""
            const el = document.querySelector('.pre-slide-list-container');
            if (el) el.scrollTop = {scroll_pos};
        """)
        page.wait_for_timeout(400)
        scroll_pos += step
    
    # 等待最后一批响应
    page.wait_for_timeout(3000)
    
    print(f"已收集 {len(all_pages_data)} 批次数据", file=sys.stderr, flush=True)
    
    # 按页码顺序整理并提取文本
    output_lines = [f"# {title}", f"（幻灯片 · 共 {total_slides} 页）", ""]
    
    # 如果 API 数据不完整，提示用户
    covered_pages = set()
    for start_idx, data_obj in all_pages_data.items():
        count = data_obj.get('count', 10)
        for i in range(start_idx, start_idx + count):
            covered_pages.add(i)
    
    missing = [i for i in range(total_slides) if i not in covered_pages]
    if missing:
        print(f"警告: 第 {[i+1 for i in missing[:5]]}... 等 {len(missing)} 页数据未加载到", file=sys.stderr)
    
    # 逐批次提取，按起始页码排序
    all_extracted_texts = {}
    for start_idx in sorted(all_pages_data.keys()):
        data_obj = all_pages_data[start_idx]
        b64_data = data_obj.get('data', '')
        if not b64_data:
            continue
        texts = extract_texts_from_slide_proto(b64_data)
        count = data_obj.get('count', 10)
        # 平均分配文本到各页（粗粒度，实际 protobuf 中包含所有页内容）
        all_extracted_texts[start_idx] = {
            'texts': texts,
            'start': start_idx,
            'end': start_idx + count - 1,
        }
    
    if not all_extracted_texts:
        return title, "（未能提取幻灯片文本内容，可能是网络超时或 API 接口变更）"
    
    # 格式化输出
    for start_idx in sorted(all_extracted_texts.keys()):
        batch = all_extracted_texts[start_idx]
        start = batch['start']
        end = min(batch['end'], total_slides - 1)
        texts = batch['texts']
        
        if not args.slide_text_only:
            output_lines.append(f"\n---")
            output_lines.append(f"## 📄 第 {start+1}~{end+1} 页")
        
        for t in texts:
            # 过滤掉以特殊 ASCII 字符开头的残留
            t_clean = re.sub(r'^[:\x20-\x2f\x3a-\x40\x5b-\x60\x7b-\x7e]+', '', t).strip()
            if len(t_clean) >= 2:
                output_lines.append(t_clean)
    
    content = '\n'.join(output_lines)
    return title, content


# ---------------------------------------------------------------------------
# 思维导图：全选复制
# ---------------------------------------------------------------------------

def read_mindmap(page, args, timeout_ms):
    """
    读取思维导图内容。
    
    策略：全选+复制，企微思维导图支持此操作，
    可获取完整的缩进树形文本（制表符缩进层级）。
    """
    print("检测到思维导图类型，使用全选复制模式...", file=sys.stderr, flush=True)
    
    print(f"正在加载思维导图: {args.doc_url}", file=sys.stderr, flush=True)
    safe_goto(page, args.doc_url, timeout_ms)
    page.wait_for_timeout(4000)
    
    # 检查登录
    if check_login_required(page):
        print("错误: Cookie 已过期，请重新运行 export_cookies.py", file=sys.stderr)
        sys.exit(2)
    
    # 检查权限
    perm_result = check_no_permission(page)
    if not perm_result["has_permission"]:
        perm_msg = perm_result.get("message", "无权限访问")
        if args.request_access and perm_result.get("can_request"):
            request_permission(page)
        print(f"错误: {perm_msg}", file=sys.stderr)
        sys.exit(4)
    
    title = extract_title(page)
    
    # 等待思维导图渲染
    try:
        page.wait_for_selector('canvas.Mind_mindCanvas__2FVMI, canvas[class*="mindCanvas"]', 
                               timeout=15000, state="attached")
        page.wait_for_timeout(2000)
    except Exception:
        page.wait_for_timeout(5000)
    
    # 执行全选复制
    print("提取思维导图内容...", file=sys.stderr, flush=True)
    modifier = get_modifier()
    
    # 先点击画布区域获取焦点
    try:
        canvas = page.locator('canvas[class*="mindCanvas"], canvas.Mind_mindCanvas__2FVMI').first
        canvas.click()
    except Exception:
        page.mouse.click(640, 400)
    page.wait_for_timeout(1000)
    
    page.keyboard.press(f"{modifier}+a")
    page.wait_for_timeout(1500)
    page.keyboard.press(f"{modifier}+c")
    page.wait_for_timeout(1500)
    
    content = page.evaluate("""async () => {
        try { return await navigator.clipboard.readText(); }
        catch (e) { return ''; }
    }""")
    
    if not content or not content.strip():
        print("全选复制失败，尝试备用方案...", file=sys.stderr, flush=True)
        # 尝试点击大纲模式
        try:
            outline_btn = page.locator('[class*="outline"]').first
            if outline_btn.is_visible(timeout=2000):
                outline_btn.click()
                page.wait_for_timeout(2000)
                # 重新尝试全选复制
                page.keyboard.press(f"{modifier}+a")
                page.wait_for_timeout(1500)
                page.keyboard.press(f"{modifier}+c")
                page.wait_for_timeout(1500)
                content = page.evaluate("""async () => {
                    try { return await navigator.clipboard.readText(); }
                    catch (e) { return ''; }
                }""")
        except Exception:
            pass
    
    return title, content or ""


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def main():
    args = parse_args()
    
    # 校验 URL
    url_error = validate_url(args.doc_url)
    if url_error:
        print(f"错误: {url_error}", file=sys.stderr)
        sys.exit(1)
    
    doc_type = get_doc_type(args.doc_url)
    print(f"文档类型: {doc_type}", file=sys.stderr, flush=True)
    
    # 加载 Cookie
    cookies = load_cookies(args.cookie_file)
    
    # 确保 Playwright 已安装
    sync_playwright = require_playwright()
    
    timeout_ms = args.timeout * 1000
    
    with sync_playwright() as p:
        browser, context = create_browser_context(p, headless=True)
        context.add_cookies(normalize_cookies(cookies))
        page = context.new_page()
        
        try:
            if doc_type == "slide":
                title, content = read_slide(page, args, timeout_ms)
                
            elif doc_type == "mind":
                title, content = read_mindmap(page, args, timeout_ms)
                if not content.strip():
                    print("错误: 未能提取思维导图内容", file=sys.stderr)
                    browser.close()
                    sys.exit(3)
                # 格式化输出
                content = f"# {title}\n（思维导图 · 缩进格式）\n\n{content.strip()}"
                
            elif doc_type == "sheet":
                # 表格：使用原有逻辑
                image_urls_captured = []
                
                if args.with_images:
                    def on_img_resp(r):
                        url = r.url
                        ct = r.headers.get("content-type", "")
                        if "image/" in ct and IMAGE_CDN_PATTERN.search(url):
                            if url not in image_urls_captured:
                                image_urls_captured.append(url)
                    page.on("response", on_img_resp)
                
                print(f"正在加载表格: {args.doc_url}", file=sys.stderr, flush=True)
                safe_goto(page, args.doc_url, timeout_ms)
                page.wait_for_timeout(3000)
                
                if check_login_required(page):
                    print("错误: Cookie 已过期", file=sys.stderr)
                    sys.exit(2)
                
                perm_result = check_no_permission(page)
                if not perm_result["has_permission"]:
                    perm_msg = perm_result.get("message", "无权限")
                    if args.request_access and perm_result.get("can_request"):
                        request_permission(page)
                    print(f"错误: {perm_msg}", file=sys.stderr)
                    sys.exit(4)
                
                wait_for_doc_render(page, timeout_ms)
                title = extract_title(page)
                
                # Tab 切换
                active_tab = None
                if args.list_tabs:
                    page.wait_for_timeout(2000)
                    tabs = list_sheet_tabs(page)
                    browser.close()
                    output = f"# {title}\n\n## Sheet Tab 列表（共 {len(tabs)} 个）\n\n"
                    for i, t in enumerate(tabs, 1):
                        output += f"{i}. {t}\n"
                    _write_output(output, args.output)
                    sys.exit(0)
                
                if args.tab:
                    page.wait_for_timeout(2000)
                    if not switch_to_tab(page, args.tab):
                        browser.close()
                        print(f"错误: 未找到名为「{args.tab}」的 Tab", file=sys.stderr)
                        sys.exit(1)
                    active_tab = args.tab
                
                if args.with_images:
                    scroll_to_capture_images(page, image_urls_captured)
                
                text_content = extract_content_via_clipboard(page)
                browser.close()
                
                if not text_content.strip():
                    print("错误: 未能提取表格内容", file=sys.stderr)
                    sys.exit(3)
                
                display_title = f"{title} - {active_tab}" if active_tab else title
                content = f"# {display_title}\n\n{text_content.strip()}"
                
                if args.with_images and image_urls_captured:
                    unique_urls = list(dict.fromkeys(
                        get_original_image_url(u) for u in image_urls_captured
                    ))
                    content += f"\n\n---\n## 图片（共 {len(unique_urls)} 张）\n"
                    for u in unique_urls:
                        content += f"- {u}\n"
                
                _write_output(content, args.output)
                sys.exit(0)
                
            else:
                # 普通文档（doc）
                print(f"正在加载文档: {args.doc_url}", file=sys.stderr, flush=True)
                safe_goto(page, args.doc_url, timeout_ms)
                page.wait_for_timeout(3000)
                
                if check_login_required(page):
                    print("错误: Cookie 已过期", file=sys.stderr)
                    sys.exit(2)
                
                perm_result = check_no_permission(page)
                if not perm_result["has_permission"]:
                    perm_msg = perm_result.get("message", "无权限")
                    if args.request_access and perm_result.get("can_request"):
                        request_permission(page)
                    print(f"错误: {perm_msg}", file=sys.stderr)
                    sys.exit(4)
                
                wait_for_doc_render(page, timeout_ms)
                title = extract_title(page)
                text_content = extract_content_via_clipboard(page)
                browser.close()
                
                if not text_content.strip():
                    print("错误: 未能提取文档内容", file=sys.stderr)
                    sys.exit(3)
                
                content = f"# {title}\n\n{text_content.strip()}"
                _write_output(content, args.output)
                sys.exit(0)
        
        except Exception as e:
            print(f"错误: {e}", file=sys.stderr)
            try:
                browser.close()
            except Exception:
                pass
            sys.exit(3)
        
        browser.close()
    
    _write_output(content, args.output)


def _write_output(content, output_path):
    """输出内容到文件或 stdout。"""
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"已保存到: {output_path}", file=sys.stderr)
    else:
        print(content)


if __name__ == "__main__":
    main()
