#!/usr/bin/env python3
"""Format a WeChat article with bold hierarchical section headings."""

import argparse
import html
import re
import sys
from pathlib import Path


P_STYLE = (
    "margin: 0 0 24px; padding: 0; font-size: 17px; line-height: 1.75; "
    "letter-spacing: 0.544px; color: rgba(0,0,0,0.9); text-align: justify;"
)
H2_STYLE = (
    "margin: 34px 0 14px; padding: 0; font-size: 20px; line-height: 1.55; "
    "letter-spacing: 0.544px; color: rgba(0,0,0,0.95); font-weight: 700;"
)
H3_STYLE = (
    "margin: 22px 0 10px; padding: 0; font-size: 17px; line-height: 1.65; "
    "letter-spacing: 0.544px; color: rgba(0,0,0,0.92); font-weight: 700;"
)
HR_STYLE = "margin: 6px 0 26px; border: 0; border-top: 1px solid rgba(0,0,0,0.12);"


def read_input(path):
    if path:
        return Path(path).expanduser().read_text(encoding="utf-8")
    return sys.stdin.read()


def extract_body(raw):
    text = raw.replace("\r\n", "\n").replace("\r", "\n").strip()
    if "## 改写正文" in text:
        text = text.split("## 改写正文", 1)[1]
    for marker in ["## 改写说明", "## 标题备选", "## 摘要"]:
        if marker in text:
            text = text.split(marker, 1)[0]
    return text.strip()


def split_blocks(markdown):
    return [block.strip() for block in re.split(r"\n\s*\n", markdown.strip()) if block.strip()]


def inline_markup(text):
    escaped = html.escape(text, quote=False)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)


def block_to_html(block):
    if block == "---":
        return f'<hr style="{HR_STYLE}">'
    if block.startswith("## "):
        return f'<p style="{H2_STYLE}"><strong>{html.escape(block[3:].strip(), quote=False)}</strong></p>'
    if block.startswith("### "):
        return f'<p style="{H3_STYLE}"><strong>{html.escape(block[4:].strip(), quote=False)}</strong></p>'
    return f'<p style="{P_STYLE}">{inline_markup(block)}</p>'


def render_text(markdown):
    cleaned = re.sub(r"[*#]", "", markdown)
    return cleaned.replace("---", "----------").strip() + "\n"


def main():
    parser = argparse.ArgumentParser(description="Format a WeChat article with bold hierarchical headings.")
    parser.add_argument("--input", help="Input Markdown article file. Reads stdin when omitted.")
    parser.add_argument("--output-dir", default=".", help="Output directory.")
    parser.add_argument("--basename", default="article", help="Output basename without extension.")
    args = parser.parse_args()

    body = extract_body(read_input(args.input))
    blocks = split_blocks(body)

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    html_path = output_dir / f"{args.basename}.html"
    text_path = output_dir / f"{args.basename}.txt"

    html_path.write_text("\n".join(block_to_html(block) for block in blocks) + "\n", encoding="utf-8")
    text_path.write_text(render_text(body), encoding="utf-8")

    print(f"HTML: {html_path}")
    print(f"TXT: {text_path}")
    print(f"Paragraphs: {sum(1 for block in blocks if block and not block.startswith('#') and block != '---')}")
    print(f"H2: {sum(1 for block in blocks if block.startswith('## '))}")
    print(f"H3: {sum(1 for block in blocks if block.startswith('### '))}")


if __name__ == "__main__":
    main()
