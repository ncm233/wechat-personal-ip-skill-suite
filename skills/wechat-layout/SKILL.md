---
name: wechat-layout
description: Use when the user says "@公众号排版", "公众号排版", "把这篇排版成公众号", "转成公众号后台可粘贴格式", or wants to format a rewritten Chinese article into minimalist WeChat public-account HTML based on a large-text, high-whitespace reference layout.
---

# WeChat Layout

Format rewritten Chinese articles into a clean WeChat public-account layout that can be pasted into the WeChat editor. The default layout follows the reference article at `https://mp.weixin.qq.com/s/qrKl1oWRLcxtMYdpE-jr4g`: large readable body text, generous paragraph spacing, sparse separators, and no decorative template components.

## Layout Style Options

Choose a layout style before formatting:

1. `minimalist` (default): large readable body text, generous paragraph spacing, sparse separators, no decorative template components. Uses `scripts/format_wechat_article.py`.
2. `bm-green`: bm.md / green-simple style installed from `wechat-article-formatter`. Uses green accent color, black-background H2 heading chips, styled blockquotes, tables, code blocks, and `styles/custom.css`. Uses `scripts/format_bm_md_article.py` and the installed CSS at:
3. `reference-bold-hierarchy`: reference-account layout for batch WeChat drafts inspired by `https://mp.weixin.qq.com/s/tS-NFXhyg0EO-fUDEmH5gw`: medium-length article, clean body text, bold hierarchical section titles, and no source/context explanation inside the body. Uses `scripts/format_reference_bold_article.py`.

```text
C:\Users\ZhuanZ（无密码）\.codex\skills\wechat-article-formatter\styles\custom.css
```

Use `bm-green` when the user asks for the imported `wechat-article-formatter`, `bm.md`, `green-simple`, green accent layout, or a more styled/template-like WeChat layout. Keep `minimalist` as the default when no layout style is specified.

Use `reference-bold-hierarchy` when the user asks to follow the reference account layout, asks for each section title to be bold and hierarchical, or asks for batch WeChat drafts to look closer to the referenced account. Target 900-1600 Chinese characters unless the source requires more; prefer a tight opening plus 3-5 numbered sections. Do not include source-processing explanations such as `from YouMind`, `source says`, or `this was rewritten from...` in the article body.

## Reference Layout DNA

Observed with browser/devtools on mobile and desktop:

- Title: 22px, line-height about 30.8px, medium weight, dark text.
- Metadata: default WeChat gray/link style; do not recreate manually unless producing a full preview page.
- Body container: WeChat default width, about 350px on mobile and 677px on desktop.
- Body text: 17px, line-height 27.2px, `text-align: justify`, color `rgba(0,0,0,.9)`.
- Paragraph spacing: `margin-bottom: 24px`, no first-line indent.
- Section breaks: thin horizontal line, `1px solid rgba(0,0,0,.1)`, followed by one blank paragraph rhythm.
- Structure: mostly plain paragraphs; no decorative cards, no colored callout boxes, no heavy headings.
- Images: rare; full content width when used.
- Ending: keep the final short sentence as its own paragraph.
- Publishing title: keep it separate for the WeChat backend title field; do not render the title again inside the article body.

## Inputs

Expected inputs:

- Recommended title and rewritten article text from `wechat-rewrite`.
- Optional cover image path from `wechat-cover-image`.
- Optional output directory or basename.

If the article contains the `wechat-rewrite` output sections, extract only `推荐主标题` and `改写正文` for layout.

## Workflow

### Step 1: Clean The Draft

Remove generation scaffolding:

- Remove `## 标题备选`.
- Remove `## 改写说明`.
- Keep `## 推荐主标题` as the publishing title only.
- Keep only the final article body for layout.
- Do not put the publishing title into the generated HTML/TXT body. WeChat already has a title field.

Do not rewrite the article unless the user explicitly asks for wording changes.

### Step 2: Segment The Article

Identify major thought turns and insert separators only where the essay changes phase.

Good separator positions:

- After the opening thesis block.
- Before a numbered route/path section.
- Before a new conceptual section.
- Before the final emotional closing section.

Avoid putting separators after every few paragraphs. The reference article used 4 separators in a long article.

### Step 3: Apply Minimalist WeChat Styling

Use this paragraph style:

```html
<p style="margin: 0 0 24px; padding: 0; font-size: 17px; line-height: 1.6; letter-spacing: 0.544px; color: rgba(0,0,0,0.9); text-align: justify;">
  ...
</p>
```

Use this separator style:

```html
<hr style="margin: 0 0 24px; border: 0; border-top: 1px solid rgba(0,0,0,0.1);">
```

Use this image style when a cover or inline image is included:

```html
<p style="margin: 0 0 24px; text-align: center;">
  <img src="..." style="max-width: 100%; height: auto; display: block; margin: 0 auto;" alt="">
</p>
```

When the user asks to place the cover illustration inside the article, append it at the end of the body after the final text paragraph:

```bash
python C:\Users\ZhuanZ（无密码）\.codex\skills\wechat-layout\scripts\format_wechat_article.py \
  --input "<article.md>" \
  --output-dir "<target-folder>" \
  --basename "<slug>" \
  --append-image "cover-900x383.jpg"
```

### Step 4: Generate Files

For default `minimalist` layout, use the bundled script:

Use the bundled script:

```bash
python C:\Users\ZhuanZ（无密码）\.codex\skills\wechat-layout\scripts\format_wechat_article.py \
  --input "<article.md>" \
  --output-dir "<target-folder>" \
  --basename "<slug>"
```

For stdin:

```bash
Get-Clipboard | python C:\Users\ZhuanZ（无密码）\.codex\skills\wechat-layout\scripts\format_wechat_article.py \
  --output-dir "<target-folder>" \
  --basename "<slug>"
```

The script outputs:

- `<basename>.html`: WeChat-ready inline-style HTML.
- `<basename>.txt`: clean plain-text copy for inspection.

For `bm-green` layout, use:

```bash
python C:\Users\ZhuanZ（无密码）\.codex\skills\wechat-layout\scripts\format_bm_md_article.py \
  --input "<article.md>" \
  --output-dir "<target-folder>" \
  --basename "<slug>"
```

This script also writes `<basename>.bm.md` for inspection. It calls:

```text
POST https://bm.md/api/markdown/render
```

with `markdownStyle=green-simple`, `codeTheme=kimbie-light`, `platform=wechat`, and the imported custom CSS. If bm.md is unavailable and the user explicitly asks for offline output, rerun with `--offline-fallback`.

For `reference-bold-hierarchy` layout, use:

```bash
python C:\Users\ZhuanZ锛堟棤瀵嗙爜锛塡.codex\skills\wechat-layout\scripts\format_reference_bold_article.py \
  --input "<article.md>" \
  --output-dir "<target-folder>" \
  --basename "<slug>"
```

Expected Markdown structure:

```markdown
Opening paragraph.

---

## 01 Section title

Section body.

### Secondary title

Secondary body.
```

The generated HTML must preserve `font-size`, `line-height`, inline `style=`, paragraphs, `<strong>`, `font-weight: 700`, and heading hierarchy (`20px` H2, `17px` H3/body).

### Step 5: Validate

Check:

- The title is present separately from the HTML body and is not rendered as the first body element.
- The body has no AI scaffolding sections.
- Paragraphs are readable and not over-segmented.
- Separators mark major phase changes only.
- HTML uses inline styles suitable for WeChat editor pasting.
- For `reference-bold-hierarchy`, H2/H3 section titles are bold and visually distinct, while body text remains clean and medium-length.
- No external CSS, scripts, nested cards, or decorative template blocks.
- If `--append-image` is used, the image is the final body element and uses a local path that the publisher can upload.
- For `bm-green`, confirm `article.bm.md` exists and the HTML was rendered by bm.md or explicitly marked as offline fallback.

## Output Shape

Return:

```text
## 标题
<publishing title>

## 排版文件
- HTML：<path>
- 纯文本：<path>

## 排版说明
- 排版风格：<minimalist or bm-green>
- 正文字号：17px
- 段落间距：24px
- 分隔线数量：<n>
- 是否移除脚手架：
```
