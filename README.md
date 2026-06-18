# WeChat Personal IP Skill Suite

A Codex skill suite for building a personal-IP and lead-generation WeChat content pipeline.

## Included Skills

- `wechat-article-pipeline`: orchestrates rewrite, cover generation, layout, and optional draft-box upload.
- `wechat-rewrite`: rewrites source material with selectable article styles.
- `wechat-cover-image`: generates WeChat cover prompts/images with selectable editorial visual styles.
- `wechat-layout`: formats rewritten articles into WeChat-ready HTML and plain text, with selectable layout styles.
- `wechat-article-formatter`: imported bm.md / green-simple formatter style provider for `layout_style=bm-green`.
- `wechat-publish-draft`: uploads formatted content to the WeChat Official Account draft box.
- `wechat-style-factory`: distills article and cover style libraries from local article archives.

## Generated Style Library

`youmind-style-library` contains generated article-style and cover-style Markdown files from the local YouMind viral article archive.

`youmind-style-library/red-style-skills` contains user-marked high-priority style skills. Batch generation should prefer these red styles and avoid repeating article/cover styles within the same batch.

Example pipeline style parameters:

```text
article_style=article-thedankoe
cover_style=cover-02-dark-editorial
layout_style=bm-green
layout_style=reference-bold-hierarchy
```

Layout style options:

- `minimalist`: default large-text, high-whitespace WeChat layout.
- `bm-green`: imported bm.md `green-simple` style with green accents, black H2 heading chips, styled blockquotes, tables, and code blocks.
- `reference-bold-hierarchy`: reference-account style with medium-length copy, clean paragraphs, and bold H2/H3 section hierarchy.

Batch generation rules:

- Prefer red marked style skills when requested.
- Use a different article style and a different cover style for every article in the same batch before reusing any style.
- Save `batch-style-plan.json` plus per-article `style-assignment.json`.

## Safety

Secrets are intentionally excluded. Configure local `.env` files for WeChat and image-generation credentials after installation.
