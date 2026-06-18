---
name: wechat-publish-draft
description: Use when the user says "@公众号草稿箱", "上传公众号草稿", "推送到公众号后台", "发到微信公众号草稿箱", or wants to upload WeChat-ready HTML plus a cover image into a WeChat Official Account draft box. This skill creates drafts only and must not publish or mass-send articles.
---

# WeChat Publish Draft

Upload a formatted WeChat article HTML file and cover image to the WeChat Official Account draft box. This skill creates a backend draft only; it never clicks publish, free-publishes, or mass-sends without a separate explicit request and a separate safety review.

## Inputs

Expected inputs:

- WeChat-ready HTML from `wechat-layout`.
- Article title from `wechat-rewrite`.
- Cover image from `wechat-cover-image`, or an existing WeChat cover `media_id`.
- Optional digest, author, source URL, account suffix, and comment settings.

If HTML, title, or cover/media_id is missing, ask for the missing item.

## Existing Configuration

Reuse existing config from:

```text
C:\Users\ZhuanZ（无密码）\.codex\skills\wechat-publish-draft\scripts\.env
D:\Users\ZhuanZ（无密码）\Documents\New project\.env
```

The script also supports a local skill `.env` file and environment variables.

Required variables:

```env
WECHAT_APPID=...
WECHAT_APPSECRET=...
```

For multiple accounts:

```env
WECHAT_APPID_A=...
WECHAT_APPSECRET_A=...
WECHAT_APPID_B=...
WECHAT_APPSECRET_B=...
```

Do not print AppSecret, access_token, or full media IDs unless the user explicitly needs them. It is okay to report that credentials exist.

## Workflow

### Step 1: Validate Local Files

Check:

- HTML file exists.
- Cover image exists, unless `--cover-media-id` is provided.
- HTML is inline-style and suitable for WeChat editor import.
- Any local `<img src="...">` paths are reachable from the HTML file directory or absolute paths.

### Step 2: Get Access Token

Use the configured AppID/AppSecret to call:

```text
GET https://api.weixin.qq.com/cgi-bin/token
```

If the request returns IP whitelist errors such as `40164`, tell the user to add the current machine/server outbound IP to WeChat Official Account backend `设置与开发 -> 基本配置 -> IP白名单`.

If the request returns `40125 invalid appsecret` or `40001 invalid credential`, stop before uploading media or creating a draft. Explain that the local AppSecret is invalid or no longer matches the AppID. Common causes:

- AppSecret was reset in the WeChat backend, so the old value is invalid.
- AppSecret was copied incorrectly, with missing/extra characters or whitespace.
- AppSecret is frozen/disabled.
- AppID and AppSecret belong to different Official Accounts.

Ask the user to confirm the current AppSecret in the WeChat backend, update the local `.env` only, then retry. Do not print or expose the AppSecret.

### Step 3: Upload Inline Images

For local body images, call:

```text
POST https://api.weixin.qq.com/cgi-bin/media/uploadimg
```

Replace local `img src` values with returned WeChat image URLs. Do not upload remote HTTP images; warn if remote non-WeChat image URLs remain.

### Step 4: Upload Cover

If `--cover-media-id` is absent, upload the cover with:

```text
POST https://api.weixin.qq.com/cgi-bin/material/add_material?type=image
```

Use the returned `media_id` as `thumb_media_id`.

### Step 5: Create Draft

Call:

```text
POST https://api.weixin.qq.com/cgi-bin/draft/add
```

Payload shape:

```json
{
  "articles": [
    {
      "title": "...",
      "author": "...",
      "digest": "...",
      "content": "...",
      "content_source_url": "...",
      "thumb_media_id": "...",
      "need_open_comment": 1,
      "only_fans_can_comment": 0
    }
  ]
}
```

Use `json.dumps(..., ensure_ascii=False).encode("utf-8")` to avoid Chinese garbling.

## Command

```bash
python C:\Users\ZhuanZ（无密码）\.codex\skills\wechat-publish-draft\scripts\upload_draft.py \
  --html "<wechat-layout.html>" \
  --title "<article title>" \
  --cover "<cover-900x383.jpg>"
```

Optional:

```bash
  --account A \
  --author "AI比我快" \
  --digest "文章摘要" \
  --source-url "https://..." \
  --cover-media-id "<existing media_id>" \
  --no-open-comment \
  --dry-run
```

## Safety Rules

- Create drafts only.
- Do not call `freepublish/submit`, mass send APIs, or UI publish buttons.
- Do not expose secrets in final output.
- Do not overwrite or delete existing drafts.
- If the user asks to publish publicly, stop and create a separate plan/checklist first.
- If WeChat returns an error, report the `errcode`, a short explanation, and the next action.
- For `40125` / `40001` credential failures, explicitly say no draft was created and no media was uploaded because the failure happened at `get_access_token`.

## Output Shape

Return:

```text
## 草稿箱结果
- 状态：成功/失败
- 草稿 media_id：<redacted or full if needed>
- 账号：默认/A/B

## 上传内容
- HTML：
- 封面：
- 正文图片数量：

## 后台检查
- 去微信公众号后台草稿箱检查标题、封面、正文排版。
- 只确认草稿，不自动发布。
```
