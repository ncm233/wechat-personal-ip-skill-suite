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

Example pipeline style parameters:

```text
article_style=article-thedankoe
cover_style=cover-02-dark-editorial
layout_style=bm-green
```

Layout style options:

- `minimalist`: default large-text, high-whitespace WeChat layout.
- `bm-green`: imported bm.md `green-simple` style with green accents, black H2 heading chips, styled blockquotes, tables, and code blocks.

## Safety

Secrets are intentionally excluded. Configure local `.env` files for WeChat and image-generation credentials after installation.
