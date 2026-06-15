# Pipeline Integration Notes

Use this library as the style source for the final personal-IP and lead-generation pipeline.

Recommended pipeline parameters:

```text
article_style=<article-style-id>
cover_style=<cover-style-id>
```

Recommended flow:

1. Choose an article style from `article-styles/`.
2. Use its rules to guide `wechat-rewrite`.
3. Choose a cover style from `cover-styles/` after checking the contact sheet.
4. Add the selected cover style as an option in `wechat-cover-image` when it becomes a production style.
5. Keep experimental style files in this library until they are visually and editorially verified.
