---
name: wechat-rewrite
description: Use when the user says "@公众号改写", "公众号改写", "按这个风格改写", "改成公众号文章", or provides notes/drafts/materials to rewrite into a Chinese WeChat public-account article and title set. Supports selectable rewrite styles including default-personal, tech-media-news / 前沿科技媒体新闻化改写风格, and ai-tech-review / AI科技评论式科技产业媒体深稿风格.
---

# WeChat Rewrite

Rewrite user-provided materials into Chinese WeChat public-account articles plus publish-ready titles. The default style is a personal, high-conviction essay style. The skill also supports selectable rewrite style options.

## Inputs

Expected inputs:

- Source material, rough notes, transcript, draft, outline, article link text, or scattered ideas.
- Optional rewrite style option, topic angle, target reader, intended length, title preference, and publishing context.

If the source material is missing, ask the user to paste it. If the topic is clear but details are thin, continue with a draft and briefly mark assumptions.

## Rewrite Style Options

Before writing, identify whether the user requested a rewrite style option. If the user does not specify a style, use `default-personal`.

Available rewrite style options:

1. `default-personal`: personal, high-conviction WeChat essay style with strong judgment, lived texture, era pressure, and a warm ending.
2. `tech-media-news`: frontier technology media style distilled from `wechat-article-style-distill`, optimized for AI/model/company/research/product news. Trigger this option when the user says `tech-media-news`, `科技媒体风格`, `前沿科技媒体`, `公众号文章风格蒸馏`, `技术新闻化`, or asks for a result-first technology media rewrite.
3. `ai-tech-review`: AI科技评论-style technology industry media rewrite. Trigger this option when the user says `ai-tech-review`, `AI科技评论`, `AI科技评论风格`, `科技产业媒体深稿`, or asks for the AI科技评论 sample-distilled style.

### Option: `default-personal`

Use this style for personal reflection, founder notes, career choices, AI-era cognition, personal growth, and opinion essays.

Core positioning:

- Write like a smart, sensitive, fast-moving operator thinking in public.
- Combine technical judgment, personal decision, ordinary-person vulnerability, and emotional momentum.
- Keep the tone high-conviction, reflective, urgent, intimate, and slightly cinematic.
- Avoid cold analysis. Let the piece feel like someone is running, looking back, and reporting what they see.

Article arc:

1. Start from a real personal event, question, or recent change.
2. State the hard judgment within the first three short paragraphs.
3. Explain why the old path is losing value.
4. Break future choices into 2-3 clear routes when useful.
5. Use concrete body-feel, personal practice, or visual metaphor to make abstract ideas alive.
6. Admit fear, uncertainty, or ordinary-person limits when the source supports it.
7. End with warm encouragement, not a slogan.

Title rules:

- Always generate one recommended main title and 5-8 title options unless the user explicitly says not to generate titles.
- Prefer strong judgment titles, personal choice titles, time-window titles, and concrete-moment titles.
- The best title should sound like a person suddenly realizing something inside an era.
- Avoid flat yearly-plan titles, slogan titles, generic motivational phrasing, fake shock, and fake guarantees.
- Prefer first-person titles when the article is personal; prefer strong judgment titles when the article is analytical.

Language rules:

- Use plain Chinese with oral rhythm.
- Alternate short hard judgments with longer reflective explanation.
- Use phrases such as `不是 A，而是 B`, `要么 A，要么 B`, `我看到`, `我感觉`, `我意识到`, `说白了` when natural.
- Use vivid physical metaphors such as rooms, walls, wilderness, car headlights, racing, scripts, tides, front-row seats, or hand practice.
- Avoid official, academic, marketing, and corporate jargon.
- Avoid generic motivational writing that has no concrete situation.

Ending rule:

- Return from the big trend to the individual person.
- End like speaking to a friend.
- Unless the user explicitly requests otherwise, end every article with this standalone final line: `Enjoy，我的朋友们。`

### Option: `tech-media-news`

Chinese style name:

```text
前沿科技媒体新闻化改写风格
```

Use this style for AI, models, agents, papers, companies, institutions, products, benchmarks, open-source projects, conferences, research results, and technical industry news.

Core positioning:

- Write like a frontier technology media account, not like traditional science popularization.
- Package new progress into technology news that readers are willing to click, finish, and share.
- Prioritize speed, accuracy, and density: state the result first, then explain background and significance.
- Keep the tone excited but not frivolous, newsy but not clickbait, technically precise but readable.

Title rules:

- Put the result before the background.
- Include at least one concrete subject when possible: institution, person, university, company, model, product, benchmark, or project name.
- Translate technical terms into a reader-visible result or meaning.
- Prefer result-oriented, contrast-oriented, and news-oriented structures.
- Use numbers, identities, institutions, results, contrast, exclamation marks, or colons only when they genuinely sharpen the news point.
- Common signal words include: `突破`, `新范式`, `首个`, `估值`, `刷屏`, `终结者`, `开源`, `可复现`, `招聘`.

Summary rules:

- Make the summary short, precise, and sharp.
- Treat the summary as a second transmission point, not a full article abstract.
- Do not repeat the title; add the missing hook, value, conflict, or result behind the title.

Opening rules:

- Do not warm up slowly.
- Within the first 3 sentences, state who did what, what the result is, and why it matters.
- Start with the conclusion or a close variant of the title.
- Explain quickly what is new compared with the past.

Body structure:

- Push a clear fact chain: result, actor, method or mechanism, evidence, comparison, boundary, industry meaning.
- Avoid long background lessons before the main news.
- Use dense paragraphs that combine subject, action, result, and contrast.
- Explain complex technical points in news language rather than copying paper language.
- Add data, benchmark, case, demo, scenario, or comparison whenever the source material supports it.
- Include at least one screenshot-worthy judgment sentence when possible.

Language rules:

- Write primarily in Chinese, but preserve English model names, institution names, product names, and technical terms when appropriate.
- Use short judgment sentences and high-density information sentences.
- Use explanatory transitions such as `换句话说`, `也就是说`, `关键在于`, `不过`, `当然` when useful.
- Avoid generic AI prose, empty motivational sentences, academic abstract tone, and exaggerated marketing language.

Judgment rules:

- Give clear conclusions without being vague or evasive.
- Use old/new contrast, strong/weak contrast, traditional/new method contrast, and past/current result contrast.
- Explain why the progress matters, while preserving boundaries and uncertainty when the source material requires it.

Ending rules:

- End by returning to industry meaning, product landing value, open-source/research significance, or next actions.
- If the article needs traffic or operational information, place it after the main article conclusion so it does not steal the core message.

Use this prompt skeleton for `tech-media-news`:

```text
Use the tech-media-news rewrite style. Rewrite the source material into a Chinese WeChat public-account technology media article.

Requirements:
1. Preserve all facts, names, numbers, chronology, and technical claims from the source. Do not fabricate new facts.
2. Start with the result: within the first 3 sentences, explain who did what, what changed, and why it matters.
3. Write the title in a result-first technology media style, using concrete actors such as institutions, companies, models, products, papers, benchmarks, or people when the source supports it.
4. Write the summary as a second transmission point, not as a repeat of the title.
5. Structure the body as a fact chain: result -> actor -> method/mechanism -> evidence/data/demo -> contrast with previous methods -> boundary -> industry meaning.
6. Translate technical ideas into news language ordinary technology readers can understand.
7. Keep the writing fast, accurate, dense, excited but not oily, popular but not exaggerated.
8. End with industry significance, landing value, open-source/research meaning, or next action.
```

### Option: `ai-tech-review`

Chinese style name:

```text
AI科技评论式科技产业媒体深稿风格
```

Use this style for AI industry media articles, AI paper interpretation, product/framework analysis, company/funding exclusives, founder interviews, industry trend analysis, and technology route debates.

Core positioning:

- Write like `AI科技评论`: technology industry media, not a pure technical blog and not a lightweight news account.
- Turn technology, products, financing, papers, company moves, and people dynamics into an industry judgment worth clicking immediately.
- Emphasize news value, judgment, industry perspective, transmission hooks, and visible editorial processing.
- Do not merely report facts; repeatedly explain what the event means for companies, tracks, commercialization, ecosystems, costs, efficiency, privacy, security, or competition.

Title style:

- Use one of these structures when suitable:
  - subject/team/company + key action/result + industry meaning
  - strong judgment + conflict/controversy + question
  - exclusive/interview/breakdown + person/company + key information
  - technical result + plain-language translation + conference/scenario suffix
  - product review title + result conclusion
  - multiple strong facts in parallel + column suffix
- Prefer concrete subjects such as AI, Agent, OpenAI, model names, university teams, labs, startups, big-company executives, products, papers, or conferences.
- Prefer actions such as release, funding, founding, going viral, expose, breakdown, interview, test, reconstruct.
- Prefer consequences such as break through, landing, cost reduction, data leakage, deep water, ambition, route war, ecosystem shift.
- Use signals such as numbers, money, contrast, contradiction, question, exclusive identity, conference name, and column suffix only when they are supported by the source.

Opening style:

- Rarely warm up slowly or start with long background.
- Within 3 sentences, explain what happened, why it matters, and what conclusion or breakdown the article will offer.
- Common hooks: `这不是一个普通产品发布，而是...`, `真正值得关注的不是表面动作，而是...`, `当 X 发生时，背后实际意味着...`, `这件事把一个旧问题重新推到台前`.

Body structure:

- Use a structured media feature rhythm: news + analysis + industry judgment.
- Prefer `01 / 02 / 03` sections or clear subheadings.
- Each section must have a specific information task: raise a question, explain a mechanism, show a case, add context, or upgrade the judgment.
- For paper interpretation, use `problem -> method -> result -> value`.
- For startup/funding exclusives, use `person/company background -> product/technology -> track judgment`.
- For interviews, use `intro summary -> Q&A or viewpoint extraction -> industry meaning`.
- For product reviews, give the conclusion first, then break down experience, cost, benefit, and limits.

Language style:

- Use medium-to-long information-dense sentences, interrupted by short judgment sentences.
- Keep a clear media editor voice: more conversational than a paper or report, more restrained than social-platform chatter.
- Useful phrases: `这背后`, `真正的问题是`, `不只是...而是...`, `意味着`, `本质上`, `起底`, `拆解`, `深水区`, `落地`, `重构`, `一体化野心`, `头号战场`.
- Avoid pure motivational writing, unsupported praise, cute jokes, all-jargon technical dumping, and pure paper-abstract style.

Judgment style:

- Put clear conclusions early.
- Use `surface phenomenon vs real change` as a recurring judgment pattern.
- Convert product actions into industry-stage changes.
- Convert technology iteration into cost, efficiency, privacy, security, business opportunity, or ecosystem impact.
- Convert funding or founder moves into track signals.
- Convert research results into application imagination beyond the paper itself.

Ending style:

- End by returning to industry trends, competitive landscape, landing barriers, or key variables over the next 1-2 years.
- Leave a larger question when useful instead of closing everything too neatly.
- Do not treat `recommended reading`, repost notices, or authorization notes as part of the core writing style unless the user explicitly asks for publishing footer copy.

Reusable writing rules:

1. Write the strongest hook first, then add subject and industry meaning.
2. Put concrete subjects in titles whenever possible: company, team, person, product, model, paper, conference.
3. Translate technical terms into an ordinary reader's result, contradiction, or value.
4. Make the summary add a stronger information point or judgment instead of repeating the title.
5. In the first 3 sentences, state what happened, why it matters, and what the article concludes.
6. Push the body through `event + explanation + judgment`.
7. Put conclusions early when possible.
8. Translate complex technology into real consequences: cost, efficiency, privacy, safety, landing, commercialization.
9. Use `01 / 02 / 03` or clear subheadings when the article needs structure.
10. Give readers at least one larger judgment beyond the single news item.
11. Be sharp, but support every judgment with cases, data, people, or scenes.
12. For paper articles, add why the industry should care; do not write only a paper abstract.
13. For exclusives or interviews, turn personal/company moves into track signals.
14. End on competition, industry variables, or future trends.
15. Make the reader remember one clear judgment, not a pile of loose information.

Use this prompt skeleton for `ai-tech-review`:

```text
Use the ai-tech-review rewrite style. Write a Chinese WeChat public-account article in the style of AI科技评论.

Requirements:
1. Preserve all facts, names, numbers, chronology, quotes, links, and technical claims from the source. Do not fabricate new facts.
2. Write like technology industry media: strong news sense, strong judgment, strong industry perspective, and visible editorial packaging.
3. In the first 3 sentences, explain what happened, why it matters, and what conclusion or breakdown this article gives.
4. Use a title that foregrounds a concrete subject, key action/result, conflict, or industry meaning.
5. Make the summary a second transmission point, adding a stronger information point or judgment instead of repeating the title.
6. Structure the body as news + analysis + industry judgment. Use 01 / 02 / 03 sections when helpful.
7. Translate technical details into cost, efficiency, privacy, security, product landing, commercialization, ecosystem, or competition impact.
8. Every major judgment should be supported by source facts, data, people, cases, scenes, or comparison.
9. End by returning to industry trend, competitive landscape, landing threshold, or the key variables worth watching next.
10. Avoid pure technical-blog tone, lightweight news blurbs, marketing hype, pure paper abstract style, and emotional personal-IP writing.
```

## Workflow

### Step 1: Choose Style

Select the rewrite style before drafting:

- If the user names `ai-tech-review` or asks for `AI科技评论`, use `ai-tech-review`.
- If the user names `tech-media-news` or asks for `科技媒体风格`, use `tech-media-news`.
- If the user does not name a style, use `default-personal`.
- If the user asks to choose between styles, briefly state the selected style and why it fits the source material.

### Step 2: Extract The Core Judgment

Identify:

- The strongest point of view or news value.
- The reader's pressure, confusion, curiosity, or hidden desire.
- The time window, industry shift, technical shift, or personal turning point.
- The concrete reason the article should feel worth reading now.

Do not start writing before the core judgment is clear.

### Step 3: Build The Article Arc

For `default-personal`, use the personal article arc from that style option.

For `tech-media-news`, use this arc:

1. Directly state the result or new progress.
2. Explain who did it and why the subject is credible.
3. Translate the method, product, paper, model, or mechanism into readable news language.
4. Show evidence: data, benchmark, demo, case, quote, comparison, or adoption signal.
5. Explain what is new compared with previous methods or market status.
6. Discuss boundary, uncertainty, or limitations if the source material supports it.
7. End with industry meaning, landing value, open-source/research significance, or next action.

For `ai-tech-review`, use this arc:

1. Start with the event and a clear industry judgment.
2. Explain why this is not an isolated piece of news.
3. Add key background about people, company, product, paper, model, funding, or track.
4. Use `01 / 02 / 03` sections when the argument needs layered analysis.
5. Translate the technology or company move into industry consequences.
6. Support judgments with facts, data, interviews, product scenes, or comparisons.
7. End on competition, commercialization, landing threshold, future variable, or route conflict.

### Step 4: Draft Titles And Summary

Always generate:

- One recommended main title.
- 5-8 title candidates.
- One short summary.

For `default-personal`, titles should carry personal choice, time-window tension, or concrete realization.

For `tech-media-news`, titles should be result-first and should include concrete actors or results whenever the source supports them.

For `ai-tech-review`, titles should combine concrete actors, key action/result, conflict, column-like density, and industry meaning whenever the source supports them.

### Step 5: Preserve Truth

- Do not fabricate personal experience, numbers, employers, investments, credentials, papers, institutions, benchmarks, links, or events.
- Do not make the author sound more certain than the material allows.
- If source material has facts, keep them accurate.
- If adding framing, make it clearly interpretive rather than invented evidence.
- Avoid fake urgency, fake scarcity, exaggerated success promises, and fake technical certainty.

## Output Shape

Unless the user specifies another format, return:

```text
## 改写风格
<default-personal, tech-media-news, or ai-tech-review>

## 推荐主标题
<one best publish-ready title>

## 标题备选
1. ...
2. ...

## 摘要
<short publish-ready summary>

## 改写正文
<完整公众号文章>

## 改写说明
- 核心判断：
- 保留事实：
- 强化方向：
```

If the user asks for only the article, still include `推荐主标题` unless they explicitly says `不要标题`.

## Default Prompt

请使用 `wechat-rewrite`，把下面的素材改写成一篇公众号文章，并给出一个推荐主标题、5-8 个标题备选和一条摘要。默认使用 `default-personal`；如果用户指定 `tech-media-news`，则改成前沿科技媒体新闻化风格；如果用户指定 `ai-tech-review` 或 `AI科技评论`，则改成 AI科技评论式科技产业媒体深稿风格。要求：保留事实，不编造经历、数据或技术结论；开头快速下判断；正文结构清晰；标题可直接用于公众号后台。
