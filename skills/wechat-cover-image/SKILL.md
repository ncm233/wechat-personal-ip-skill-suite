---
name: wechat-cover-image
description: Use when the user says "@公众号封面", "公众号封面图", "给这篇公众号配封面", "根据改写文章生成封面", or wants to generate a WeChat public-account cover image from a rewritten article using APiYi ChatGPT/GPT Image 2. Supports selectable cover styles including default-editorial, every.to, abstract-magazine / 高端思想杂志式抽象 editorial 封面艺术风格, science-collage / 观念型科学杂志拼贴插画风格, classical-dark-poster / 古典艺术底图融合现代极简排版的暗调 editorial 社交海报风格, and dark-woodcut / 复古黑白木刻版画与迷幻暗黑线描风格.
---

# WeChat Cover Image

Generate a WeChat public-account cover image from a rewritten article. The default visual style is a neo-classical engraved collage editorial cover: 19th-century engraving linework, high-contrast black-and-white figures, saturated flat color fields, symbolic composition, and modern op-ed/concept-art clarity.

## Inputs

Expected inputs:

- Rewritten article text, draft, outline, or final title.
- Optional cover title, visual metaphor, style option, output folder, model choice, or whether to actually call the image API.

If the article is missing, ask for the article. If only the topic/title is provided, generate a cover prompt from that title and mark the concept as inferred.

## WeChat Cover Size

Use these defaults for public-account article covers:

- Main article cover: `900x383` px, about `2.35:1`.
- Secondary/square cover: `500x500` px or `200x200` px depending on publishing UI and use case.
- Safe area: keep the key figure, visual metaphor, and any short text near the center so square crops still work.

Because `gpt-image-2` requires generated sizes to use dimensions divisible by 16, generate at `1808x768` first, then crop/resize to exact WeChat outputs.

## API Setup

Use APiYi token management at:

```text
https://api.apiyi.com/token
```

Do not write API keys into this skill or committed files. Before generation, require one of:

```bash
export APIYI_API_KEY="..."
# or
export YI_API_KEY="..."
```

The default API base is:

```text
https://api.apiyi.com/v1
```

## Style Options

Before building the final prompt, identify whether the user requested a cover style option. If the user does not specify a style, use the default neo-classical engraved collage editorial style.

Available style options:

1. `default-editorial`: the existing WeChat cover style in this skill, optimized for public-account article covers.
2. `every.to`: use the specific every.to-style image prompt below. Trigger this option when the user says `every.to 配图Prompt`, `every.to 风格`, `新古典雕版拼贴插画风格`, or asks for the style copied from every.to.
3. `abstract-magazine`: use the high-end intellectual magazine abstract editorial cover art prompt below. Trigger this option when the user says `高端思想杂志式抽象 editorial`, `高端思想杂志封面`, `抽象 editorial 封面`, `High-End Intellectual Magazine`, or asks for a more abstract, premium magazine-like cover.
4. `science-collage`: use the conceptual science-magazine collage illustration prompt below. Trigger this option when the user says `观念型科学杂志拼贴`, `科学杂志拼贴`, `Conceptual Science-Magazine Collage`, or asks for an intellectual mixed-media science-journal collage cover.
5. `classical-dark-poster`: use the classical-art-plus-modern-minimal-typography dark editorial social poster prompt below. Trigger this option when the user says `古典艺术底图融合现代极简排版`, `暗调 editorial 社交海报`, `古典艺术暗调海报`, or asks for a classical artwork base with bold modern typography.
6. `dark-woodcut`: use the vintage black-and-white woodcut / detailed pen-and-ink cross-hatching / psychedelic dark illustration prompt below. Trigger this option when the user says `复古黑白木刻版画`, `细腻钢笔线描`, `交错网线`, `迷幻暗黑插画`, `dark-woodcut`, or asks for a pure black-and-white engraving cover.

### Option: `every.to`

Chinese style name:

```text
新古典雕版拼贴插画风格
```

English style name:

```text
Neo-classical engraved collage editorial illustration
```

Style breakdown, style only:

- Rooted in the visual language of 19th-century engraving, etching, and woodcut illustration, with a distinctly antique printmaking feel.
- Uses dense hatching, cross-hatching, stippling, and etched line texture to create volume instead of modern gradients.
- Combines black-and-white engraved subjects with bold, saturated flat-color backgrounds for strong historical contrast and visual punch.
- The palette is restrained but intense: black-and-white forms plus one or two dominant colors with a small accent color.
- Extremely high contrast, with crisp relationships between black contour, white highlight, and flat color fields.
- Composition follows editorial-illustration logic rather than naturalistic realism, prioritizing symbolism, metaphor, and conceptual clarity.
- Built as a collage system, mixing classical engraved elements with contemporary graphic blocks and surreal visual juxtapositions.
- Backgrounds are simplified into stripes, flat planes, grain, or minimal spatial cues to keep focus on the main forms.
- Poster-like readability: bold silhouette, strong thumbnail presence, and immediate recognition from a distance.
- Texture feels like a hybrid of vintage printed matter and contemporary magazine/op-ed illustration.
- Mood is intellectual, controlled, slightly ironic, and allegorical, fitting commentary-driven editorial visuals.
- Not traditional academic painting and not purely flat digital illustration; it is classical engraving aesthetics fused with modern editorial concept design.

Use this prompt skeleton for the `every.to` option:

```text
Create a horizontal WeChat public-account article cover, 2.35:1 aspect ratio, in a Neo-classical engraved collage editorial illustration style.

Central concept: <one symbolic editorial metaphor from the article>.

Style: rooted in the visual language of 19th-century engraving, etching, and woodcut illustration, with a distinctly antique printmaking feel. Use dense hatching, cross-hatching, stippling, and etched line texture to create volume instead of modern gradients. Combine black-and-white engraved subjects with bold, saturated flat-color backgrounds for strong historical contrast and visual punch.

Palette: restrained but intense, usually black-and-white forms plus one or two dominant flat colors and a small accent color. Keep extremely high contrast, with crisp relationships between black contour, white highlight, and flat color fields.

Composition: editorial-illustration logic rather than naturalistic realism. Prioritize symbolism, metaphor, and conceptual clarity. Build the image as a collage system, mixing classical engraved elements with contemporary graphic blocks and surreal visual juxtapositions. Simplify the background into stripes, flat planes, grain, or minimal spatial cues. Make the image poster-readable, with bold silhouettes, strong thumbnail presence, and immediate recognition from a distance.

Mood and texture: a hybrid of vintage printed matter and contemporary magazine/op-ed illustration. Intellectual, controlled, slightly ironic, and allegorical. Neither traditional academic painting nor purely flat digital illustration.

Text: no full article title. Use no text by default. If labels are essential, use only 1-4 tiny Chinese labels, each 2-4 characters, integrated like editorial annotations.

Avoid: photorealism, glossy 3D, anime, polished vector art, corporate SaaS illustration, decorative gradients, long text, fake logos, watermarks, UI screenshots, and literal step-by-step infographics.
```

### Option: `abstract-magazine`

Chinese style name:

```text
高端思想杂志式抽象 editorial 封面艺术风格
```

English style name:

```text
High-End Intellectual Magazine Abstract Editorial Cover Art Style
```

Style breakdown, style only:

- The overall impression is highly curated, exhibition-like, and rooted in the visual culture of premium intellectual magazines.
- This is concept-driven cover art, closer to contemporary art publishing than commercial storytelling imagery.
- Compositions are restrained and centered, with generous white space that frames the image like an artwork within a publication system.
- Typography and image should feel deliberately related: title, margins, image window, and small footer text form a stable editorial structure.
- The central image leans abstract, semi-abstract, or symbolic, relying on form, materiality, color, and spatial tension rather than literal depiction.
- The visual language may span abstract painting, digital compositing, conceptual photography, sculptural still life, and experimental image-making.
- Material presence is crucial: canvas texture, mineral surfaces, misty grain, sprayed pigment, paper feel, dust-like particles, and subtle print noise.
- Color is bold yet controlled, often one dominant statement hue supported by a small number of contrasting or neutral tones.
- Muted stone-like palettes, dusty pinks, aged-paper warmth, or gallery-like subdued color fields can heighten sophistication.
- Abstract form language may involve geometry, fracture, layering, cut planes, spray effects, granular diffusion, and material transformation or rupture.
- Space is built through tonal depth, overlap, material contrast, and localized atmospherics rather than classical perspective.
- If photographic realism appears, it should be stylized, conceptualized, and art-directed rather than documentary.
- The cover should have strong object-quality, like both a magazine cover and a collectible art print.
- The mood is cool, reflective, elite, modernist with a hint of postmodern experimentation, balancing intellectual seriousness with art-world polish.

Use this prompt skeleton for the `abstract-magazine` option:

```text
Create a horizontal WeChat public-account article cover, 2.35:1 aspect ratio, in a High-End Intellectual Magazine Abstract Editorial Cover Art Style.

Central concept: <one abstract or symbolic visual thesis from the article>.

Style: highly curated, exhibition-like, and rooted in the visual culture of premium intellectual magazines. This is not narrative illustration; it is concept-driven cover art, closer to contemporary art publishing, culture journals, and high-end editorial design than commercial storytelling imagery.

Composition: restrained, centered, and spacious. Use generous white space or a clean publication-like field that frames the central image as an artwork inside a stable editorial system. Make the relationship between title area, margins, image window, and small footer-like details feel deliberate and premium. The image should feel like a collectible printed object, not a crowded promotional poster.

Image language: abstract, semi-abstract, or symbolic. Communicate intellectual density through form, materiality, color, and spatial tension rather than literal depiction. The visual language may combine abstract painting, digital compositing, conceptual photography, sculptural still life, and experimental image treatment.

Materiality: emphasize canvas texture, mineral surfaces, misty grain, sprayed pigment, paper feel, dust-like particles, subtle print noise, or tactile art-object surfaces. Use geometry, fracture, layering, cut planes, spray effects, granular diffusion, and a sense of material transformation or rupture.

Color and space: use bold but controlled color. Prefer one dominant statement hue with a few contrasting or neutral tones, or a muted stone-like, dusty pink, aged-paper, or gallery-like subdued palette. Build space through tonal depth, overlap, material contrast, and localized atmospherics rather than classical perspective.

Mood: cool, reflective, elite, modernist, slightly postmodern and experimental. Balance intellectual seriousness with art-world polish.

Text: no long article title inside the image. If text is needed, use only minimal magazine-like typography, small footer marks, or 1-3 tiny Chinese words, integrated as part of the editorial system.

Avoid: literal storytelling scenes, commercial poster clutter, stock photos, influencer-style design, glossy 3D, anime, corporate SaaS illustration, decorative gradients, fake logos, watermarks, dense infographic text, and documentary realism.
```

### Option: `science-collage`

Chinese style name:

```text
观念型科学杂志拼贴插画风格
```

English style name:

```text
Conceptual Science-Magazine Collage Illustration Style
```

Style breakdown, style only:

- Use a high-concept editorial illustration style focused on visualizing ideas rather than simple decoration or narrative.
- Build the image through mixed-media collage: paper, photography, drawing, pattern, scanned textures, and digital layout can coexist in one composition.
- Keep the composition flat and poster-like, arranging elements through juxtaposition, floating placement, layering, cutouts, and collage logic rather than realistic space.
- Use torn paper edges, cropped fragments, offset panels, ruptured surfaces, and visible assembly marks to reinforce a handmade, constructed quality.
- Make materiality essential: paper grain, print texture, rough surfaces, aged stock, scan noise, and fabric-like finishes should be visible.
- Shift between representational source material and abstract forms to create an intellectual, metaphor-driven editorial tone.
- Favor geometric shapes, circles, patterned fills, linear structures, and decorative repeated motifs for abstract components.
- Use hand-drawn elements only when they feel thoughtful, restrained, and slightly experimental rather than cute or whimsical.
- Prefer dark grounds with selective bright accents, or muted retro tones punctuated by a few high-clarity highlight colors.
- Keep color relationships print-minded, closer to cultural magazine covers or literary/science journal illustrations than glossy commercial advertising.
- Minimize perspective and physical volume; build depth through overlap, scale jumps, occlusion, and material contrast.
- Preserve occasional photographic or archival realism to create tension against abstract or illustrated elements.
- Treat backgrounds as atmospheric fields: brushy paint, paper surfaces, night-sky depth, printed texture, or emotionally charged grounds.
- Aim for an intellectual, curated, metaphorical, slightly retro mood merging science-journal sensibility with art-collage aesthetics.

Use this prompt skeleton for the `science-collage` option:

```text
Create a horizontal WeChat public-account article cover, 2.35:1 aspect ratio, in a Conceptual Science-Magazine Collage Illustration Style.

Central concept: <one intellectual visual metaphor from the article, expressed through collage logic>.

Style: high-concept editorial illustration focused on visualizing ideas rather than simple decoration or linear narrative. Use a mixed-media collage language that combines paper, photography, drawing, pattern, scanned textures, archival fragments, and digital layout within one composition.

Composition: flat, poster-like, and concept-driven. Arrange elements through juxtaposition, floating placement, layering, cutout logic, offset panels, ruptured surfaces, and visible assembly marks rather than realistic spatial perspective. Use torn paper edges, cropped fragments, collage seams, and broken white space to make the image feel handmade, constructed, and intellectually assembled.

Materiality: make paper grain, print texture, rough surfaces, aged stock, scan noise, fabric-like finishes, brushy paint, and subtle ink or risograph-like imperfections visible. The background should not be a neutral blank; treat it as an atmospheric field such as a paper surface, printed texture, dark science-journal ground, brushed field, or night-sky-like depth.

Image language: shift between representational source material and abstract forms. Combine occasional photographic or archival realism with geometric blocks, circles, patterned fills, linear structures, decorative repeated motifs, restrained hand-drawn marks, and symbolic fragments. Keep hand-drawn elements thoughtful, cool, and experimental, not cute or whimsical.

Color: use print-minded color relationships. Prefer a dark ground with selective bright accents, or muted retro tones punctuated by a few high-clarity highlight colors. Keep the palette restrained but not monotonous, more like a cultural magazine or science journal illustration than glossy commercial advertising.

Space and mood: minimize traditional perspective and physical volume. Create rhythm through overlap, scale jumps, occlusion, and material contrast. The final mood should be intellectual, curated, metaphorical, slightly retro, and quietly experimental, merging science-journal sensibility with art-collage aesthetics.

Text: no full article title. Use no text by default. If labels are essential, use only 1-4 tiny Chinese labels, each 2-4 characters, integrated as archival annotations, diagram marks, or magazine-like micro typography.

Avoid: glossy commercial poster design, generic corporate illustration, cute doodles, cartoon whimsy, photorealistic hero scenes, polished 3D, anime, decorative gradients, fake logos, watermarks, dense infographic text, and literal step-by-step diagrams.
```

### Option: `classical-dark-poster`

Chinese style name:

```text
古典艺术底图融合现代极简排版的暗调 editorial 社交海报风格
```

English style name:

```text
Dark Editorial Social Poster Style Combining Classical Art Imagery with Modern Minimal Typography
```

Style breakdown, style only:

- Merge classical art reproduction with contemporary content-poster design, combining cultural prestige with internet-native editorial clarity.
- Use a systemized cover layout. The original social-poster logic is vertical with imagery above and a large dark typographic field below; adapt that structure to the required horizontal WeChat cover while preserving the image-to-dark-field relationship.
- Let the image layer carry oil painting, classical painting, museum print, or old art-reproduction texture, with muted tones, soft aging, and a reflective historical mood.
- Use soft vignettes, faded transitions, misty masks, or gentle overlays to blend classical imagery into the dark typographic field.
- Make the black ground tactile rather than flat digital black, with visible grain, noise, paper texture, or film-like roughness.
- Use oversized, heavy, geometric sans-serif typography as a modern information-design element.
- Create deliberate contrast between atmospheric, culturally loaded classical imagery and crisp, rational, high-impact modern typography.
- Let the headline behave as a primary visual element, usually left-aligned and dominant, rather than as a small caption.
- Use generous negative space and dark empty fields to create sophistication through tension between image, type, and black ground.
- Keep branding or imprint-like marks minimal and near the bottom or lower center, like a magazine masthead or publisher mark.
- Keep the color strategy restrained. Apart from the source artwork palette, introduce few or no extra accent colors.
- Aim for a final impression between an art poster, an intellectual media cover, and a social content card.

Use this prompt skeleton for the `classical-dark-poster` option:

```text
Create a horizontal WeChat public-account article cover, 2.35:1 aspect ratio, in a Dark Editorial Social Poster Style Combining Classical Art Imagery with Modern Minimal Typography.

Central concept: <one cultural or intellectual visual thesis from the article, expressed through a classical-art image base and modern editorial typography>.

Layout: adapt the vertical social-poster system to a horizontal WeChat cover. Use classical artwork imagery as the main atmospheric image layer across the upper or left portion, then reserve a large dark typographic field across the lower or right portion. Keep a stable series-like editorial structure with clear image area, dark text area, generous margins, and restrained imprint-like details.

Image layer: use the texture of oil painting, classical painting, museum reproduction, or aged art print. Muted tones, soft aging, low saturation, historical mood, and reflective cultural weight. Blend the image into the dark field using soft vignettes, misty transitions, faded masks, and subtle atmospheric overlays rather than a hard cutoff.

Dark ground: use black or near-black with visible grain, noise, paper texture, or film-like roughness. Avoid perfectly flat digital black. The dark field should feel like printed matter or a tactile social editorial card.

Typography: oversized, heavy, geometric sans-serif, with broad letterforms and clear modern information-design impact. Let the headline behave as a primary visual element, usually left-aligned and dominant. Use high contrast between the atmospheric classical image and the crisp rational modern text system. If Chinese text is used, keep it short and bold; avoid long paragraphs.

Color: restrained and serious. Let the classical image provide most of the color. Add few or no extra accent colors. Keep the final tone calm, mature, dark, cultural, and editorial.

Mood: a cross between an art museum poster, an intellectual media cover, and a social content card. Efficient for distribution, but clearly art-directed, calm, serious, and refined.

Text: no full article title unless the user explicitly provides a short cover title. If text is needed, use 1-8 large Chinese characters or a very short phrase as the main typographic element, plus tiny imprint-like footer text if useful.

Avoid: bright commercial poster colors, glossy advertising effects, cluttered layouts, decorative gradients, stock-photo realism, influencer-style graphics, fake logos, watermarks, ornate serif typography overload, and long unreadable Chinese text.
```

### Option: `dark-woodcut`

Chinese style name:

```text
复古黑白木刻版画风格 / 细腻钢笔线描（交错网线）风格 / 迷幻暗黑插画风格
```

English style name:

```text
Vintage Black and White Woodcut Engraving Style / Detailed Pen and Ink Cross-Hatching / Psychedelic Dark Illustration
```

Style breakdown, style only:

- Use a pure bi-tonal palette: no grayscale gradients, no soft color, only pure black and solid white.
- Build every shadow, transition, highlight, and surface through the density and direction of black-and-white linework.
- Use dense hatching and cross-hatching with extremely fine directional line work.
- Let short strokes, wavy lines, contour-following lines, and intricate cross-hatching define volume, texture, and rhythm.
- Use extreme contrast and heavy negative space, with large solid black areas for background, voids, or deep shadows.
- Create a heavy, cosmic, mysterious, oppressive, and occult-adjacent atmosphere through the balance of black fields and white linework.
- Use fine stippling and dot work in light-shadow transition zones, faint reflections, dust, cosmic particles, or distant texture.
- Make the image feel vintage, hand-engraved, tactile, and printmade rather than digitally smooth.
- Let line patterns swirl, ripple, spiral, smoke, or mimic woodgrain and tree rings.
- Give cold dark compositions a surreal, hypnotic, psychedelic quality through organic non-linear line flow.

Use this prompt skeleton for the `dark-woodcut` option:

```text
Create a horizontal WeChat public-account article cover, 2.35:1 aspect ratio, in a Vintage Black and White Woodcut Engraving Style / Detailed Pen and Ink Cross-Hatching / Psychedelic Dark Illustration style.

Central concept: <one symbolic dark editorial metaphor from the article>.

Palette: pure bi-tonal black and white only. No grayscale gradients, no color, no soft airbrush shading. All shadows, transitions, highlights, depth, and atmosphere must be implied through the density, rhythm, and direction of black-and-white lines.

Linework: use extremely fine, directional hatching and cross-hatching. Short strokes, wavy contour lines, dense parallel hatching, intricate cross-hatching, stippling, and dot work should follow the shape of the forms. The linework should define volume while creating strong texture, movement, and handmade engraved rhythm.

Contrast and space: use extreme black-white contrast with large fields of solid black as background, void, or deep shadow. Let negative space dominate parts of the composition to create a mysterious, oppressive, cosmic, and occult-like atmosphere. Keep the central metaphor readable as a WeChat thumbnail.

Texture: add fine stippling and grainy dot textures in transition zones between light and dark, around faint reflections, dust, star-like particles, or atmospheric fragments. The image should feel like vintage woodcut, copper engraving, or pen-and-ink printmaking, not smooth digital illustration.

Psychedelic organic flow: let hatching patterns swirl, ripple, spiral, or mimic smoke, tree rings, and woodgrain. Use non-linear organic line flow to add surreal, hypnotic, psychedelic energy to an otherwise stark dark composition.

Composition: strong editorial poster logic, not naturalistic realism. Prefer one bold central figure, symbolic object, threshold, tunnel, machine, eye, hand, mask, landscape, or abstract omen. Keep the main visual centered enough for square cropping while using the wide frame for black negative space and flowing line texture.

Text: no full article title. Use no text by default. If labels are essential, use only 1-3 tiny Chinese labels in pure black/white, integrated like engraved annotations.

Avoid: grayscale gradients, color, glossy 3D, anime, cute illustration, polished vector art, photorealistic rendering, soft painterly blending, decorative gradients, fake logos, watermarks, dense infographic text, and long unreadable Chinese text.
```

## Workflow

### Step 1: Read The Article

Extract:

- Core judgment.
- Emotional temperature.
- Target reader pressure.
- One visual metaphor that can be understood without reading the article.
- 3-6 short keywords that can appear as tiny labels if needed.

### Step 2: Choose A Cover Concept

Prefer one strong concept, not a collage of many ideas.

Good concepts:

- A central decision-maker, traveler, founder, or thinker standing at the threshold of a path.
- A winding road from tunnel/darkness toward a bright doorway, market, machine, or future signal.
- Symbolic checkpoints that map to the article's core stages: users, product, cashflow, market, freedom, feedback, courage, time.
- A classical figure plus modern flat color blocks, machinery, targets, cubes, pipes, audience silhouettes, charts, or doors.
- One editorial metaphor with allegorical weight rather than a literal infographic.

Avoid:

- Photorealistic portraits or glossy 3D renderings.
- Corporate SaaS illustration.
- Glossy cyberpunk, anime, decorative gradients, or polished vector art.
- Dense infographic text.
- Full article title rendered as long Chinese text.
- Stock-photo vibes, realistic office scenes, fake UI screenshots, and fake logos.

### Step 3: Build The Prompt

Write the image prompt in English with any necessary short Chinese text explicitly quoted. Keep in-image text minimal.

First choose the style option:

- If the user names `every.to`, use the `every.to` prompt skeleton from Style Options.
- If the user names `abstract-magazine` or asks for `高端思想杂志式抽象 editorial`, use the `abstract-magazine` prompt skeleton from Style Options.
- If the user names `science-collage` or asks for `观念型科学杂志拼贴`, use the `science-collage` prompt skeleton from Style Options.
- If the user names `classical-dark-poster` or asks for `古典艺术底图融合现代极简排版`, use the `classical-dark-poster` prompt skeleton from Style Options.
- If the user names `dark-woodcut` or asks for `复古黑白木刻版画`, use the `dark-woodcut` prompt skeleton from Style Options.
- If the user does not name a style, use `default-editorial`.
- If the user asks to choose between styles, briefly state the selected style and why it fits the article before generation.

Prompt structure:

```text
Create a horizontal WeChat public-account article cover, 2.35:1 aspect ratio, in a neo-classical engraved collage editorial illustration style.

Central concept: <one symbolic editorial metaphor from the article>.

Style: rooted in 19th-century copperplate engraving, woodcut, and etching. Black-and-white engraved figures and objects with dense hatching, cross-hatching, stippling, etched contours, antique printed-paper grain, and crisp high-contrast linework. Combine these classical engraved elements with bold saturated flat color fields such as burnt orange, cobalt blue, warm parchment, black, and small accents of gold or red. The mood is intellectual, allegorical, controlled, slightly ironic, and contemporary editorial.

Composition: modern op-ed / magazine cover logic, not naturalistic realism. Use a strong silhouette and a poster-like layout that remains readable as a small thumbnail. Prefer one central human figure or symbolic object, a winding path or threshold, and a few surreal collage elements. Keep the key subject and main metaphor centered within the safe square crop while using the full wide frame for secondary symbols.

Text: no full article title. Use no text by default. If labels are essential, use only 1-4 tiny Chinese labels, each 2-4 characters, integrated like editorial annotations.

Avoid: photorealism, glossy 3D, anime, polished vector art, corporate SaaS illustration, decorative gradients, long text, fake logos, watermarks, UI screenshots, and literal step-by-step infographics.
```

For Founder-style articles, prefer this reusable pattern:

```text
Create a horizontal WeChat public-account article cover, 2.35:1 aspect ratio, in a neo-classical engraved collage editorial illustration style.

Scene: an engraved young founder/traveler stands near the center holding a compass and notebook, facing a winding elevated path that begins in a dark tunnel and leads toward a glowing doorway. Along the path, place symbolic checkpoints for "<label1>", "<label2>", "<label3>", and "<label4>" using simple engraved icons such as audience silhouettes, a product cube, a cashflow coin/pipe, a target, or a market machine. Use large flat color fields: burnt orange on the left/middle, cobalt blue on the right, warm parchment paper texture, and black engraved linework.

Text: no title. Optional tiny Chinese labels only: "<label1>", "<label2>", "<label3>", "<label4>".

Style and avoid rules: <use the default style block above>.
```

### Step 4: Generate The Image

Use the bundled script:

```bash
python $env:USERPROFILE\.codex\skills\wechat-cover-image\scripts\generate_cover.py \
  --prompt "<final image prompt>" \
  --output-dir "<target-output-folder>" \
  --basename "<slug>"
```

Defaults:

- Model: `gpt-image-2`
- API base: `https://api.apiyi.com/v1`
- Generation size: `1808x768`
- Quality: `high`
- Exact main output: `900x383`
- Square output: `500x500`

For lower predictable per-image cost, use `--model gpt-image-2-all` and put the aspect ratio into the prompt. For strict size with the lower fixed-price reverse channel, use `--model gpt-image-2-vip --size 2048x864` if that size is accepted by the token/model.

### Step 5: Validate

Check:

- The final main cover is exactly `900x383`.
- The square cover is exactly `500x500`.
- The key concept remains visible in the center crop.
- There is no long or unreadable text.
- The image matches the neo-classical engraved collage editorial style.
- The image has etched line texture, high contrast, restrained saturated color fields, and strong thumbnail readability.

If generation fails, report the API error and keep the final prompt so the user can retry.

## Style DNA

### 中文风格名

新古典雕版拼贴编辑插画风格

### English Style Name

Neo-classical Engraved Collage Editorial Illustration Style

### Visual Rules

- Root the image in 19th-century engraving, copperplate etching, woodcut, and antique printed illustration.
- Use dense hatching, cross-hatching, stippling, etched contours, halftone dots, and visible paper grain to build volume.
- Combine black-and-white engraved subjects with bold saturated flat-color backgrounds.
- Prefer a restrained but intense palette: black, white, warm parchment, burnt orange/red, cobalt blue, and a small gold or red accent.
- Keep contrast very high: crisp black contour, white highlights, and clearly separated flat color planes.
- Compose like an editorial/op-ed cover rather than a naturalistic scene.
- Prioritize symbolism, metaphor, and conceptual clarity over literal illustration.
- Use collage logic: classical figures, modern machinery, geometric blocks, paths, doors, targets, audiences, and surreal juxtapositions can coexist.
- Simplify the background into flat planes, grain, stripes, or minimal spatial cues.
- Make the image poster-readable from a distance and robust as a WeChat thumbnail.
- Keep the mood intellectual, controlled, allegorical, slightly ironic, and serious enough for opinion essays.
- Avoid pure vintage nostalgia; the target is classical engraving technique fused with contemporary editorial concept design.

## Output Shape

Return:

```text
## 封面概念
<one-sentence concept>

## 风格选项
<default-editorial, every.to, abstract-magazine, science-collage, classical-dark-poster, or dark-woodcut>

## 生成提示词
<final prompt>

## 输出文件
- 主封面：<path>-900x383.jpg
- 方形封面：<path>-500x500.jpg
- 原始图：<path>-raw.<ext>

## 检查结果
- 尺寸：
- 中心安全区：
- 风格一致性：
```
