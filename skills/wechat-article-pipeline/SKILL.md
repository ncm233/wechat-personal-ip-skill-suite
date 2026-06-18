---
name: wechat-article-pipeline
description: Use when the user says "@公众号流水线", "公众号全流程", "wechat-article-pipeline", "改写生成封面排版推草稿箱", or wants one coordinated workflow that rewrites source material into a Chinese WeChat article with selectable article styles and cover styles, generates a cover image, formats WeChat-ready HTML, and uploads it to the WeChat Official Account draft box.
---

# WeChat Article Pipeline

Coordinate the full WeChat public-account production workflow from raw material to draft-box upload. This skill is an orchestrator: use child skills for the actual work, keep artifacts organized in one article folder, and avoid duplicating child-skill instructions.

## Child Skills

Use these skills in order when the requested scope includes the step. Read each child skill's `SKILL.md` before acting on that step.

- `wechat-style-factory`: optional preparation step for extracting reusable article and cover style files from a local archive.
- `wechat-rewrite`: rewrite source material into a publish-ready article and title set. Supports `article_style`.
- `wechat-cover-image`: generate a WeChat cover image from the rewritten article. Supports `cover_style`.
- `wechat-layout`: convert the rewritten article into clean WeChat-ready HTML and plain text.
- `wechat-publish-draft`: upload the HTML and cover to the WeChat Official Account draft box only.

If the user asks for only one stage, use the matching child skill instead of forcing the full pipeline.

## Default Workspace

Unless the user gives another target directory, create one folder per article under:

```text
D:\Users\ZhuanZ（无密码）\Documents\New project\今日公众号项目
```

Folder naming:

```text
YYYY-MM-DD-<short-slug>
```

Preferred artifact names:

```text
source.md
rewritten.md
cover-prompt.md
cover-900x383.jpg
cover-square.jpg
article.html
article.txt
draft-result.json
```

Keep all generated article artifacts in the article folder.

## Style Library

The pipeline can accept style parameters:

```text
article_style=<style-id>
cover_style=<style-id>
layout_style=<minimalist|bm-green>
style_library=<path-to-style-library>
```

For the current local YouMind style library, the default generated index is:

```text
D:\Users\ZhuanZ（无密码）\Documents\New project\youmind-style-library\pipeline\style-index.md
```

When `article_style` is provided:

- If it is a built-in `wechat-rewrite` option such as `default-personal`, `tech-media-news`, or `ai-tech-review`, pass that option directly to `wechat-rewrite`.
- If it points to a generated style file such as `article-thedankoe`, read the corresponding Markdown file from the style library and use its rules as the rewrite style guide.

When `cover_style` is provided:

- If it is a built-in `wechat-cover-image` option such as `every.to`, `abstract-magazine`, `science-collage`, `classical-dark-poster`, or `dark-woodcut`, pass that option directly to `wechat-cover-image`.
- If it points to a generated cover style file such as `cover-01-clean-light`, read the corresponding Markdown file and contact sheet from the style library, then use its visual rules as the cover prompt style.

If the user asks to build or refresh the style library, run `wechat-style-factory` first.

When `layout_style` is provided:

- `minimalist` is the default existing WeChat layout: large body text, high whitespace, sparse separators, no decorative template components.
- `bm-green` uses the imported `wechat-article-formatter` / bm.md `green-simple` style with custom CSS, green accents, black H2 heading chips, styled blockquotes, tables, and code blocks.
- If the user says `wechat-article-formatter`, `bm.md`, `green-simple`, `绿色排版`, or `导入的公众号排版skill`, map it to `layout_style=bm-green`.
- If the user does not specify a layout style, use `minimalist`.

## Workflow

### Step 1: Clarify Scope

Determine which stages are requested:

1. Style extraction only.
2. Rewrite only.
3. Rewrite + cover.
4. Rewrite + cover + layout.
5. Rewrite + cover + layout + draft-box upload.

For `wechat-article-pipeline`, the default scope is rewrite + cover + layout. Upload to draft box is allowed when explicitly requested or when the user asks for full pipeline including draft-box upload. The upload step creates a backend draft only; it must not publish publicly or mass-send.

If the source material is missing, ask for it. Otherwise proceed.

### Step 2: Create Article Folder

Create the article folder before generating files. Save the user's original material as `source.md` unless it already exists in a user-provided file.

Slug rules:

- Prefer a short lowercase English slug from the topic.
- Use `article` if the topic is unclear.
- If the folder exists, append `-2`, `-3`, etc.

### Step 3: Rewrite

Use `wechat-rewrite` on the source material, applying `article_style` when provided. Save the complete output as `rewritten.md`.

Required rewrite output:

- Selected article style.
- Recommended main title.
- 5-8 title candidates.
- Short summary.
- Full article body.
- Short rewrite notes.

Do not move to cover generation until the recommended title and article body are present.

### Step 4: Generate Cover

Use `wechat-cover-image` with the recommended title and rewritten article, applying `cover_style` when provided. Save the final prompt as `cover-prompt.md`. Save or rename outputs to:

- `cover-900x383.jpg`
- `cover-square.jpg`

Validate that the main cover is exactly `900x383` and the square cover is exactly `500x500`.

### Step 5: Layout

Use `wechat-layout` on `rewritten.md`, applying `layout_style` when provided. Save:

- `article.html`
- `article.txt`

For `minimalist`, run the existing `format_wechat_article.py` flow. For `bm-green`, run `format_bm_md_article.py`, which renders through bm.md with the imported `wechat-article-formatter` CSS and also writes `article.bm.md`.

Validate that the HTML contains only the final article body, not title candidates or rewrite notes. Keep the recommended title separately for draft upload.

### Step 6: Draft-Box Upload

Run this step only when requested as part of the workflow.

Use `wechat-publish-draft` with:

- `article.html`
- recommended title from `rewritten.md`
- `cover-900x383.jpg`

Start with `--dry-run` only if the user asks for a trial, setup check, or validation. Otherwise create a real draft in the Official Account backend draft box.

Never publish publicly, mass-send, call freepublish APIs, or click a UI publish button as part of this pipeline.

Always save `draft-result.json`. If upload was not attempted because of an error in an earlier stage, set `status` to `failed` or `pending` and explain why in `notes`.

## Failure Handling

- If style extraction succeeds but style naming is too generic, keep the generated files and ask the user which contact sheets should be promoted into production style options.
- If rewrite succeeds but cover generation fails, keep `rewritten.md` and `cover-prompt.md`, report the image API error, and stop before layout only if the cover is required for the next step.
- If layout succeeds but draft upload fails, keep `article.html`, `article.txt`, and the cover files, then report the WeChat `errcode` and next action.
- If WeChat returns an IP whitelist error such as `40164`, tell the user to add the current outbound IP to the Official Account backend IP whitelist.
- If WeChat returns `40125 invalid appsecret` or `40001 invalid credential` while getting `access_token`, treat it as a credential problem before any upload occurred. Tell the user the local AppSecret is no longer valid or does not match the AppID. Common causes: AppSecret was reset, copied incorrectly, frozen/disabled, or belongs to another Official Account. Ask the user to provide the current AppSecret from the WeChat backend, then update only the local `.env` secret file and retry. Never reveal the old or new AppSecret in the response.
- Do not expose API keys, AppSecret, access tokens, or full credentials in the final response.

## Output Shape

Return a compact production summary:

```text
## 公众号流水线结果
- 状态：
- 文章风格：
- 封面风格：
- 排版风格：
- 标题：
- 文章目录：

## 产物
- 改写稿：
- 封面：
- 排版 HTML：
- 草稿箱：

## 下一步
- 后台检查项或失败后的处理动作。
```

When upload succeeds, report that the backend draft was created and ask the user to inspect it in the WeChat Official Account backend before any public publishing.
