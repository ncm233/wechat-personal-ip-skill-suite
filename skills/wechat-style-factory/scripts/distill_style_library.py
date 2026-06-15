#!/usr/bin/env python
"""Distill article and cover style libraries from a local article archive."""

from __future__ import annotations

import argparse
import csv
import math
import os
import re
import shutil
import statistics
import tempfile
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

try:
    from PIL import Image, ImageFilter, ImageStat
except Exception as exc:  # pragma: no cover
    raise SystemExit("Pillow is required. Install with: python -m pip install pillow") from exc


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
BOILERPLATE_MARKERS = (
    "## 元信息",
    "## 封面",
    "## TL;DR",
    "## 正文",
    "推荐阅读",
    "转载",
    "授权",
)


def slugify(value: str, fallback: str = "style") -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or fallback


def read_text(path: Path) -> str:
    for enc in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="ignore")


def extract_root(input_path: Path, work_dir: Path) -> Path:
    if input_path.is_dir():
        return input_path
    if input_path.suffix.lower() != ".zip":
        raise ValueError(f"Unsupported input: {input_path}")
    target = work_dir / input_path.stem
    if target.exists():
        return find_archive_root(target)
    with zipfile.ZipFile(input_path) as zf:
        zf.extractall(target)
    return find_archive_root(target)


def find_archive_root(root: Path) -> Path:
    candidates = [root, *[p for p in root.rglob("*") if p.is_dir()]]
    for cand in candidates:
        if (cand / "articles.csv").exists() and (cand / "articles").is_dir() and (cand / "covers").is_dir():
            return cand
    raise FileNotFoundError(f"Could not find archive root under {root}")


def load_rows(root: Path) -> list[dict]:
    csv_path = root / "articles.csv"
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def article_path(root: Path, row: dict) -> Path:
    rank = int(row.get("rank") or 0)
    slug = row.get("slug") or row.get("id") or "article"
    return root / "articles" / f"{rank:04d}-{slug}.md"


def cover_path(root: Path, row: dict) -> Path | None:
    rank = int(row.get("rank") or 0)
    slug = row.get("slug") or row.get("id") or "cover"
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        p = root / "covers" / f"{rank:04d}-{slug}{ext}"
        if p.exists():
            return p
    return None


def article_body(md: str) -> str:
    marker = "## 正文"
    idx = md.find(marker)
    if idx >= 0:
        return md[idx + len(marker):].strip()
    return md


def headings(md: str) -> list[str]:
    result = []
    for line in md.splitlines():
        if line.startswith("#"):
            text = re.sub(r"^#+\s*", "", line).strip()
            if text and not any(x in text for x in ("元信息", "封面", "TL;DR", "正文")):
                result.append(text[:80])
    return result


def opening_excerpt(md: str, limit: int = 650) -> str:
    body = article_body(md)
    lines = []
    for raw in body.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("!") or line.startswith("- "):
            continue
        if any(marker in line for marker in ("推荐阅读", "转载声明", "授权")):
            continue
        lines.append(line)
        if sum(len(x) for x in lines) > limit:
            break
    text = "\n".join(lines)
    return text[:limit].strip()


def title_features(titles: list[str]) -> dict:
    total = max(len(titles), 1)
    return {
        "count": len(titles),
        "question": sum("?" in t or "？" in t for t in titles),
        "exclaim": sum("!" in t or "！" in t for t in titles),
        "colon": sum(":" in t or "：" in t or "｜" in t or "|" in t for t in titles),
        "digits": sum(bool(re.search(r"\d", t)) for t in titles),
        "avg_len": round(sum(len(t) for t in titles) / total, 1),
        "top_words": Counter(re.findall(r"[A-Za-z][A-Za-z0-9+.-]*|[\u4e00-\u9fff]{2,}", " ".join(titles))).most_common(20),
    }


def paragraph_stats(samples: list[str]) -> dict:
    paras = []
    for text in samples:
        for p in text.splitlines():
            p = p.strip()
            if p:
                paras.append(len(p))
    if not paras:
        return {"median": 0, "avg": 0, "short_ratio": 0}
    return {
        "median": int(statistics.median(paras)),
        "avg": int(statistics.mean(paras)),
        "short_ratio": round(sum(x <= 28 for x in paras) / len(paras), 2),
    }


def write_article_style(root: Path, out_dir: Path, author: str, rows: list[dict], max_samples: int) -> dict:
    selected = rows[:max_samples]
    titles = [r.get("title", "").strip() for r in selected if r.get("title")]
    summaries = []
    openings = []
    all_headings = []
    files = []
    for row in selected:
        p = article_path(root, row)
        if not p.exists():
            continue
        md = read_text(p)
        files.append(p.name)
        summaries.append(row.get("description") or row.get("summary") or "")
        openings.append(opening_excerpt(md))
        all_headings.extend(headings(md))

    feats = title_features(titles)
    pstats = paragraph_stats(openings)
    style_id = f"article-{slugify(author, 'unknown-author')}"
    path = out_dir / f"{style_id}.md"
    display = selected[0].get("author_name") or author
    common_headings = [h for h, _ in Counter(all_headings).most_common(8)]
    top_words = "、".join(w for w, _ in feats["top_words"][:12])

    content = f"""# {style_id}

Source group: `{display}` / `{author}`
Sample count: {len(selected)}

## 1. 总体风格定位
- 这是一个从 `{display}` 样本中自动蒸馏出的文章风格草案，适合继续人工或 AI 二次精修。
- 样本标题平均长度约 {feats['avg_len']} 字，正文开头段落中位长度约 {pstats['median']} 字，整体偏向 {'短段落高节奏' if pstats['short_ratio'] >= 0.45 else '中长段信息推进'}。
- 该组内容的高频标题信号包括：{top_words or '待进一步人工提炼'}。
- 写作目标应优先复刻其标题钩子、开头承诺、段落节奏和可收藏结构，而不是复述样本主题。

## 2. 标题风格
- 常见标题结构：主体/结果前置、问题承诺、方法清单、强判断或教程型标题。
- 标题里的高频词：{top_words or '无明显高频词'}。
- 标题制造点击欲的方式：数字标题 {feats['digits']} 篇，问句标题 {feats['question']} 篇，感叹标题 {feats['exclaim']} 篇，冒号/栏目式标题 {feats['colon']} 篇；优先把读者收益、结果、身份或场景放到标题前半段。

## 3. 开头方式
- 常见开头类型：先给判断或痛点，再解释为什么值得继续读。
- 是否喜欢直接下判断：从样本开头看，建议默认直接进入结论，不做长背景铺垫。
- 是否使用故事、问题、冲突或反常识：优先使用问题、反差、收益承诺和具体场景。

## 4. 正文结构
- 段落长度：开头样本段落均值约 {pstats['avg']} 字，中位数约 {pstats['median']} 字。
- 小标题习惯：常见小标题示例包括：{'; '.join(common_headings[:6]) or '待进一步抽样确认'}。
- 观点和案例的比例：建议用“观点 -> 解释 -> 例子/步骤 -> 小结判断”的循环推进。
- 是否喜欢列表、编号、表格：从样本标题和文章结构看，适合使用编号、小标题和步骤化清单增强收藏价值。

## 5. 语言特点
- 句子长短：短判断句和中长解释句交替。
- 口语化程度：口语化但不散，适合公众号长文阅读。
- 常用表达：建议保留“你会发现 / 换句话说 / 真正的问题是 / 这意味着 / 如果你想要”等解释型表达。
- 禁用表达：避免空泛鸡汤、过度营销、AI 套话、没有事实支撑的宏大结论。

## 6. 判断方式
- 作者如何表达态度：先给明确判断，再用经验、步骤、数据或案例托住。
- 是否会给明确结论：建议明确给，不要让读者自己在材料里找重点。
- 是否喜欢使用反问、类比、对比：适合使用旧路径 vs 新路径、普通做法 vs 高级做法、表面问题 vs 真问题。

## 7. 结尾方式
- 常见收尾方式：回到读者处境，给下一步行动或可执行提醒。
- 是否有行动号召：适合轻行动号召，不要硬广式导流。
- 是否喜欢总结金句：可以保留一句可截图判断，但避免过度口号化。

## 8. 可复用写作规则
1. 标题先写结果、痛点或收益，不要先写背景。
2. 标题尽量包含具体对象、数字、场景或读者身份。
3. 摘要不要复述标题，要补第二个钩子。
4. 开头三段内交代读者为什么要继续读。
5. 正文用小标题推进，每个小标题只承担一个任务。
6. 每一节都要给读者一个判断、方法、例子或可收藏清单。
7. 少写抽象形容词，多写可执行动作。
8. 复杂概念必须翻译成普通读者能感到的收益或代价。
9. 用对比制造理解速度：过去 vs 现在，普通人 vs 高手，表面问题 vs 真问题。
10. 保留口语节奏，但不要碎碎念。
11. 重要句子单独成段，方便截图和传播。
12. 案例服务观点，不要为讲故事而讲故事。
13. 结尾回到读者下一步，而不是泛泛总结。
14. 不编造作者经历、数据、身份或具体事实。
15. 生成前先明确本文的一句话承诺。

## 样本文件
{os.linesep.join('- ' + x for x in files[:20])}

## 后续精修 Prompt
请基于以上统计和样本文件，进一步使用“个人风格提取 Prompt”精修该风格，只分析写作风格，不分析文章内容。
"""
    path.write_text(content, encoding="utf-8")
    return {"id": style_id, "path": path, "display": display, "samples": len(selected)}


def image_features(path: Path) -> dict | None:
    try:
        img = Image.open(path).convert("RGB")
    except Exception:
        return None
    img.thumbnail((180, 180))
    stat = ImageStat.Stat(img)
    mean = stat.mean
    brightness = sum(mean) / 3
    sat_values = []
    dark = 0
    light = 0
    total = 0
    for r, g, b in img.getdata():
        mx, mn = max(r, g, b), min(r, g, b)
        sat_values.append(mx - mn)
        lum = (r + g + b) / 3
        dark += lum < 55
        light += lum > 215
        total += 1
    edges = img.convert("L").filter(ImageFilter.FIND_EDGES)
    edge_mean = ImageStat.Stat(edges).mean[0]
    return {
        "path": path,
        "brightness": brightness,
        "saturation": statistics.mean(sat_values),
        "dark_ratio": dark / max(total, 1),
        "light_ratio": light / max(total, 1),
        "edge": edge_mean,
        "width": img.width,
        "height": img.height,
    }


def kmeans(items: list[dict], k: int, iterations: int = 24) -> list[list[dict]]:
    if not items:
        return []
    k = min(k, len(items))
    vectors = [
        (
            f["brightness"] / 255,
            f["saturation"] / 255,
            f["dark_ratio"],
            f["light_ratio"],
            f["edge"] / 255,
        )
        for f in items
    ]
    centers = [vectors[int(i * len(vectors) / k)] for i in range(k)]
    labels = [0] * len(items)
    for _ in range(iterations):
        for i, vec in enumerate(vectors):
            labels[i] = min(range(k), key=lambda c: sum((vec[j] - centers[c][j]) ** 2 for j in range(len(vec))))
        new_centers = []
        for c in range(k):
            assigned = [vectors[i] for i, lab in enumerate(labels) if lab == c]
            if assigned:
                new_centers.append(tuple(sum(v[j] for v in assigned) / len(assigned) for j in range(len(vectors[0]))))
            else:
                new_centers.append(centers[c])
        centers = new_centers
    clusters = [[] for _ in range(k)]
    for item, label in zip(items, labels):
        clusters[label].append(item)
    return [c for c in clusters if c]


def describe_cover_cluster(cluster: list[dict]) -> tuple[str, str, list[str], list[str]]:
    avg = {key: statistics.mean(x[key] for x in cluster) for key in ("brightness", "saturation", "dark_ratio", "light_ratio", "edge")}
    if avg["dark_ratio"] > 0.45:
        base = "dark-editorial"
        cn = "暗调高反差 editorial 封面风格"
        en = "Dark High-Contrast Editorial Cover Style"
    elif avg["light_ratio"] > 0.45:
        base = "clean-light"
        cn = "高留白浅色极简信息封面风格"
        en = "Clean Light Minimal Information Cover Style"
    elif avg["saturation"] > 75:
        base = "saturated-pop"
        cn = "高饱和流行视觉封面风格"
        en = "Saturated Pop Editorial Cover Style"
    elif avg["edge"] > 34:
        base = "dense-graphic"
        cn = "高线条密度图形化封面风格"
        en = "Dense Graphic Linework Cover Style"
    else:
        base = "muted-editorial"
        cn = "低饱和杂志 editorial 封面风格"
        en = "Muted Magazine Editorial Cover Style"

    cn_rules = [
        f"整体明度约 {avg['brightness']:.0f}/255，暗部占比约 {avg['dark_ratio']:.0%}，亮部占比约 {avg['light_ratio']:.0%}。",
        f"色彩饱和度约 {avg['saturation']:.0f}/255，边缘/线条密度约 {avg['edge']:.0f}/255。",
        "画面应只分析视觉语言，不绑定样本中的文章主题。",
        "生成时优先复刻版式关系、色彩策略、对比度、图像密度和材质感。",
        "避免把文件名、标题或文章内容当作风格本身。",
    ]
    en_rules = [
        f"Average brightness is about {avg['brightness']:.0f}/255, dark-field ratio about {avg['dark_ratio']:.0%}, light-field ratio about {avg['light_ratio']:.0%}.",
        f"Average saturation is about {avg['saturation']:.0f}/255, edge or line density about {avg['edge']:.0f}/255.",
        "Analyze visual language only, not the article topic represented by the sample.",
        "When generating, replicate layout relationships, color strategy, contrast, image density, and texture.",
        "Do not treat filenames, article titles, or subject matter as the style itself.",
    ]
    return base, cn, cn_rules, [en, *en_rules]


def create_contact_sheet(images: list[Path], output: Path, thumb_size=(240, 135), cols: int = 4) -> None:
    thumbs = []
    for path in images:
        try:
            img = Image.open(path).convert("RGB")
        except Exception:
            continue
        img.thumbnail(thumb_size)
        canvas = Image.new("RGB", thumb_size, "white")
        x = (thumb_size[0] - img.width) // 2
        y = (thumb_size[1] - img.height) // 2
        canvas.paste(img, (x, y))
        thumbs.append(canvas)
    if not thumbs:
        return
    rows = math.ceil(len(thumbs) / cols)
    sheet = Image.new("RGB", (cols * thumb_size[0], rows * thumb_size[1]), "white")
    for i, thumb in enumerate(thumbs):
        sheet.paste(thumb, ((i % cols) * thumb_size[0], (i // cols) * thumb_size[1]))
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, quality=92)


def write_cover_style(cluster: list[dict], out_dir: Path, sheets_dir: Path, index: int, max_samples: int) -> dict:
    base, cn_name, cn_rules, en_parts = describe_cover_cluster(cluster)
    style_id = f"cover-{index:02d}-{base}"
    samples = sorted(cluster, key=lambda x: x["path"].name)[:max_samples]
    sample_paths = [x["path"] for x in samples]
    sheet = sheets_dir / f"{style_id}.jpg"
    create_contact_sheet(sample_paths[:24], sheet)
    path = out_dir / f"{style_id}.md"
    en_name, *en_rules = en_parts
    content = f"""# {style_id}

Contact sheet: `../cover-contact-sheets/{sheet.name}`
Sample count: {len(cluster)}

中文版

## 1. 风格名

{cn_name}

## 2. 具体的风格特征拆解（不包含内容本身）

{os.linesep.join('- ' + x for x in cn_rules)}
- 该文件为自动聚类生成的封面风格草案，建议结合 contact sheet 做一次视觉复核后再加入正式封面生成 skill。

English Version

## 1. Style Name

{en_name}

## 2. Breakdown of Style Characteristics

{os.linesep.join('- ' + x for x in en_rules)}
- This is an automatically clustered cover-style draft. Review the contact sheet before promoting it into a production cover-generation skill.

## 样本封面

{os.linesep.join('- ' + p.name for p in sample_paths[:30])}

## 后续精修 Prompt

请分析 contact sheet 中的图片风格，只分析风格，不包含内容，输出中文和英文两版，格式为：1. 风格名；2. 具体的风格特征拆解（不包含内容本身）。
"""
    path.write_text(content, encoding="utf-8")
    return {"id": style_id, "path": path, "sheet": sheet, "samples": len(cluster)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Distill article and cover style files from a local archive.")
    parser.add_argument("--input", required=True, help="ZIP file or extracted archive root.")
    parser.add_argument("--output-dir", required=True, help="Output directory for style library.")
    parser.add_argument("--top-authors", type=int, default=12)
    parser.add_argument("--article-samples", type=int, default=30)
    parser.add_argument("--cover-clusters", type=int, default=10)
    parser.add_argument("--cover-samples", type=int, default=30)
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    out_root = Path(args.output_dir).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    work_dir = out_root / "_work"
    work_dir.mkdir(parents=True, exist_ok=True)
    root = extract_root(input_path, work_dir)

    article_dir = out_root / "article-styles"
    cover_dir = out_root / "cover-styles"
    sheets_dir = out_root / "cover-contact-sheets"
    pipeline_dir = out_root / "pipeline"
    for d in (article_dir, cover_dir, sheets_dir, pipeline_dir):
        d.mkdir(parents=True, exist_ok=True)

    rows = load_rows(root)
    by_author: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        key = row.get("author_handle") or row.get("author_name") or "unknown"
        by_author[key].append(row)
    author_groups = sorted(by_author.items(), key=lambda kv: (-len(kv[1]), kv[0]))[: args.top_authors]
    article_styles = [write_article_style(root, article_dir, author, group, args.article_samples) for author, group in author_groups]

    features = []
    for row in rows:
        p = cover_path(root, row)
        if not p:
            continue
        f = image_features(p)
        if f:
            features.append(f)
    features.sort(key=lambda x: x["path"].name)
    clusters = kmeans(features, args.cover_clusters)
    clusters.sort(key=len, reverse=True)
    cover_styles = [write_cover_style(cluster, cover_dir, sheets_dir, i + 1, args.cover_samples) for i, cluster in enumerate(clusters)]

    index_lines = [
        "# Style Library Index",
        "",
        f"Source: `{root}`",
        f"Articles: {len(rows)}",
        f"Article styles: {len(article_styles)}",
        f"Cover styles: {len(cover_styles)}",
        "",
        "## Article Styles",
        "",
    ]
    for item in article_styles:
        rel = item["path"].relative_to(out_root).as_posix()
        index_lines.append(f"- `{item['id']}`: [{item['display']}]({rel}) ({item['samples']} samples)")
    index_lines.extend(["", "## Cover Styles", ""])
    for item in cover_styles:
        rel = item["path"].relative_to(out_root).as_posix()
        sheet = item["sheet"].relative_to(out_root).as_posix()
        index_lines.append(f"- `{item['id']}`: [style]({rel}), [contact sheet]({sheet}) ({item['samples']} samples)")
    (pipeline_dir / "style-index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    notes = """# Pipeline Integration Notes

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
"""
    (pipeline_dir / "integration-notes.md").write_text(notes, encoding="utf-8")

    shutil.rmtree(work_dir, ignore_errors=True)
    print(f"Created style library: {out_root}")
    print(f"Article styles: {len(article_styles)}")
    print(f"Cover styles: {len(cover_styles)}")
    print(f"Index: {pipeline_dir / 'style-index.md'}")


if __name__ == "__main__":
    main()
