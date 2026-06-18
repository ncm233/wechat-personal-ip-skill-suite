#!/usr/bin/env python3
"""Format a rewritten article through bm.md with the installed green WeChat CSS."""

import argparse
import html
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


DEFAULT_RENDER_URL = "https://bm.md/api/markdown/render"
DEFAULT_CSS = Path(r"C:\Users\ZhuanZ（无密码）\.codex\skills\wechat-article-formatter\styles\custom.css")


def slugify(value):
    value = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff_-]+", "-", value.strip())
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value[:60] or f"bm-wechat-layout-{time.strftime('%Y%m%d-%H%M%S')}"


def read_input(path):
    if path:
        return Path(path).expanduser().read_text(encoding="utf-8")
    return sys.stdin.read()


def extract_title_and_body(raw):
    text = raw.replace("\r\n", "\n").replace("\r", "\n").strip()
    title = ""

    title_match = re.search(r"^## 推荐主标题\s*\n+(.+?)(?:\n{2,}|$)", text, flags=re.M | re.S)
    if title_match:
        title = title_match.group(1).strip().splitlines()[0].strip()

    body_match = re.search(r"^## 改写正文\s*\n+(.+?)(?=\n## 改写说明|\n## 标题备选|\Z)", text, flags=re.M | re.S)
    if body_match:
        body = body_match.group(1).strip()
    else:
        body = text

    body = re.sub(r"^## 改写风格\s*\n+.+?(?=\n## |\Z)", "", body, flags=re.M | re.S).strip()
    body = re.sub(r"^## 推荐主标题\s*\n+.+?(?=\n## |\Z)", "", body, flags=re.M | re.S).strip()
    body = re.sub(r"^## 标题备选\s*\n+.+?(?=\n## |\Z)", "", body, flags=re.M | re.S).strip()
    body = re.sub(r"^## 摘要\s*\n+.+?(?=\n## |\Z)", "", body, flags=re.M | re.S).strip()
    body = re.sub(r"^## 改写说明\s*\n+.+$", "", body, flags=re.M | re.S).strip()

    if not title:
        first_line = next((line.strip("# ").strip() for line in body.splitlines() if line.strip()), "")
        if len(first_line) <= 60 and not first_line.endswith(("。", "，", "；")):
            title = first_line
            body = body.replace(first_line, "", 1).strip()

    return title, body


def markdown_to_plain_text(markdown):
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", markdown)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.M)
    text = re.sub(r"[*_`>~-]+", "", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


def extract_rendered_html(response):
    if isinstance(response, str):
        return response
    if not isinstance(response, dict):
        raise ValueError("bm.md response is not a JSON object")

    for key in ("html", "content", "result"):
        value = response.get(key)
        if isinstance(value, str) and value.strip():
            return value

    data = response.get("data")
    if isinstance(data, str) and data.strip():
        return data
    if isinstance(data, dict):
        for key in ("html", "content", "result"):
            value = data.get(key)
            if isinstance(value, str) and value.strip():
                return value

    raise ValueError(f"Unsupported bm.md response shape: {json.dumps(response, ensure_ascii=False)[:1000]}")


def render_with_bm(markdown, css, args):
    payload = {
        "markdown": markdown,
        "markdownStyle": args.markdown_style,
        "codeTheme": args.code_theme,
        "customCss": css,
        "enableFootnoteLinks": True,
        "openLinksInNewWindow": True,
        "platform": "wechat",
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        args.render_url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "wechat-layout-bm-green/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"bm.md render failed: HTTP {exc.code}\n{detail}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"bm.md render failed: {exc}") from exc

    try:
        return extract_rendered_html(json.loads(raw))
    except json.JSONDecodeError:
        if raw.lstrip().startswith("<"):
            return raw
        raise SystemExit(f"bm.md returned non-JSON response:\n{raw[:1000]}")


def fallback_html(markdown):
    parts = []
    for block in re.split(r"\n{2,}", markdown.strip()):
        block = block.strip()
        if not block:
            continue
        if block == "---":
            parts.append('<hr style="margin: 10px 0; border: 0; border-top: 1px solid rgb(53,179,120);">')
        elif block.startswith("## "):
            text = html.escape(block[3:].strip(), quote=False)
            parts.append(f'<h2 style="margin:30px 0 15px;text-align:center;"><span style="font-size:18px;color:#fff;background:#000;padding:2px 10px;font-weight:bold;">{text}</span></h2>')
        else:
            escaped = html.escape(block, quote=False).replace("\n", "<br>")
            parts.append(f'<p style="color:rgb(89,89,89);font-size:15px;line-height:1.8;letter-spacing:.04em;text-align:left;margin:0;padding:8px 0;">{escaped}</p>')
    return "\n".join(parts) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Format an article through bm.md with green WeChat CSS.")
    parser.add_argument("--input", help="Input rewritten article file. Reads stdin when omitted.")
    parser.add_argument("--output-dir", default=".", help="Output directory.")
    parser.add_argument("--basename", help="Output basename without extension.")
    parser.add_argument("--css", default=str(DEFAULT_CSS), help="Custom CSS file.")
    parser.add_argument("--render-url", default=DEFAULT_RENDER_URL)
    parser.add_argument("--markdown-style", default="green-simple")
    parser.add_argument("--code-theme", default="kimbie-light")
    parser.add_argument("--timeout", default=120, type=int)
    parser.add_argument("--offline-fallback", action="store_true", help="Use local fallback HTML instead of bm.md.")
    args = parser.parse_args()

    raw = read_input(args.input)
    title, body = extract_title_and_body(raw)
    css_path = Path(args.css).expanduser()
    css = css_path.read_text(encoding="utf-8") if css_path.exists() else ""

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    base = args.basename or slugify(title)

    markdown_path = output_dir / f"{base}.bm.md"
    html_path = output_dir / f"{base}.html"
    text_path = output_dir / f"{base}.txt"

    markdown_path.write_text(body.strip() + "\n", encoding="utf-8")
    rendered = fallback_html(body) if args.offline_fallback else render_with_bm(body, css, args)
    html_path.write_text(rendered, encoding="utf-8")
    text_path.write_text(markdown_to_plain_text(body), encoding="utf-8")

    print(f"HTML: {html_path}")
    print(f"TXT: {text_path}")
    print(f"Markdown: {markdown_path}")
    print(f"Title: {title}")
    print(f"Layout style: bm-green")


if __name__ == "__main__":
    main()
