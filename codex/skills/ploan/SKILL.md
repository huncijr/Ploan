---
name: ploan
description: Render prompt-made terminal backgrounds with Ploan. Use when the user asks for /Ploan, terminal scenery, ASCII/Unicode wallpaper, visual backgrounds, landscapes, cabins, space scenes, moons, planets, vehicles, creatures, dashboards, or terminal beautification.
---

# Ploan — Prompt-Made Terminal Background

Turn the user's prompt into a beautiful terminal background. Ploan is the renderer; you design the scene.

## Absolute Requirement

You MUST produce visible terminal background art.

Do not only say "theme applied".
Do not only call a palette tool.
Do not produce a small icon or simple wireframe.

The user should get actual wallpaper-grade ASCII/Unicode art.

## What To Create

Design a unique image-like terminal background based on the user's prompt using:

- ASCII art with dense character shading
- Unicode box drawing and block elements
- Half-block art: `▀`, `▄`, `█`, `░`, `▒`, `▓`
- Braille pixel art when useful
- Landscape/object silhouettes with interior texture
- Clouds, sun/moon, mountains, trees, water, houses, cities, spaceships, creatures
- Full-width composition that feels like a generated image converted to ASCII

Think like an image generator making a beautiful wallpaper, then translating it into ASCII/Unicode.

## Classic ASCII Reference Style

Use classic public ASCII-gallery craft as a style target, including the kind of dense, shaded forms seen in old ASCII art collections. This is inspiration only: do not copy, reproduce, or closely paraphrase any external artwork.

Borrow techniques, not art:

- Use INDIVIDUAL characters from density ramps to create gradients. Pick ONE character per position based on how dark/light that spot should be:
  - Brightest/lit areas: space, `.`, `,`, `:`
  - Light areas: `;`, `i`, `1`, `t`
  - Medium areas: `f`, `L`, `C`, `G`
  - Dark/shadow areas: `0`, `8`, `@`, `#`, `%`
  - Block fills: `░`, `▒`, `▓`, `█`
- CRITICAL: Do NOT write the ramp string itself (like `.:;i1tfLCG08@`) as visible content. Use individual characters FROM the ramp, placed one at a time to create a spatial gradient across the object surface.
- Solid silhouettes plus internal texture, not just outlines
- Asymmetric highlights and shadow-side density (one side bright/sparse chars, other side dark/dense chars)
- Perspective distortion, occlusion, and foreground/background depth
- Object-specific texture: metal panels, bark, feathers, scales, clouds, terrain, fabric folds, water ripples, crater rims, rock faces
- Old-school ASCII shading letters/numbers like `M`, `N`, `8`, `U`, `o`, `d`, `P`, `@`, `$` when they improve shape and depth

For every subject, first imagine a strong classic ASCII silhouette, then add internal shading and texture. The result should feel hand-crafted and recognizable, not like a generated wireframe.

### Where ideas come from

The user can ask for any subject, so no fixed example set covers everything.

- **The user may browse for inspiration.** To get a specific look, the user can browse a public gallery such as https://ascii.co.uk/art, pick a style or subject they like, and describe that *style* in the prompt (for example "a dense, old-school shaded tilted-ring Saturn" or "a classic ASCII-gallery moon with crater texture"). When useful, suggest this to the user.
- **The AI generates original art, never a 1:1 copy.** When the user references a gallery artwork or style, create a new, hand-crafted composition that borrows the *techniques* (density ramps, shading, perspective, texture, composition) — not the exact artwork. Never reproduce, trace, or closely paraphrase a specific external composition, and never include signatures, author tags, or attribution lines.

## Default Visual Rule

Do NOT include readable words, labels, titles, captions, debug text, palette lines, or banners unless the user explicitly asks for text.

Default output should be scenery/object art only.

### Explicit Text And ASCII Typography

If the user explicitly asks for a word, phrase, slogan, name, logo text, banner, or ASCII typography, readable text is the requested subject and MUST NOT be removed or down-ranked merely for being readable.

- Preserve the requested wording exactly, including apostrophes and capitalization.
- Set `no_text` to `false` and `include_text` to `true`.
- Set `composition` to `codex-footer-strip ascii-typography` and `subject` to the exact requested phrase.
- Use a large 4-6 row FIGlet-like or hand-built letter silhouette when it fits. Do not replace a good large banner with a tiny decorative sentence just to satisfy object-art shading metrics.
- Keep the upper canvas rows blank and put the complete typography in the final 4-6 scene rows. The patched renderer reserves the bottom composer/status rows and raises the art automatically.
- Do not add `PLOAN`, `Palette:`, `Mood:`, debug text, or any wording the user did not request.
- Quality feedback about `contains_readable_text`, volumetric object depth, crater texture, or grounding does not apply when text was explicitly requested. Fix only clipping, misspelling, weak letter structure, or placement.

## Quality Bar

Generate a compact footer-strip ASCII/Unicode image for the Codex TUI.

- The patched Codex renderer paints only empty cells. Near the end of an active session, the conversation covers almost the whole viewport and usually leaves only 3-5 visible rows above the input.
- Keep `scene.lines.length` equal to the terminal height from `get_terminal_info`, but leave the upper rows blank and place ALL meaningful art in the final 3-5 rows (up to 6 for explicitly requested large ASCII typography).
- Prefer 50-80 columns, scaled to the terminal width. Use the available width to make a recognizable horizontal silhouette; do not make a tall wallpaper that will be hidden behind chat.
- Set `composition` to `codex-footer-strip` and `safe_zone` to `codex-footer-3-5-rows`.
- Compress detail into silhouette, windows/eyes/panels, one shading row, and a final ground/shadow row. Every visible row must contribute to recognizability.
- Use recognizable silhouettes and contours, not only random particles.
- Use volumetric ASCII: combine outline, interior shading, texture, and light/dark character ramps so objects feel 3D, not like flat wireframes.
- Prefer rich ASCII ramps for solid objects: ` .,:;i1tfLCG08@`, `.-:=+*#%@`, `░▒▓█`, and structural characters such as `()[]{}\/|_~^`.
- For organic or rounded subjects, use staggered contours and internal shading bands, not only symmetric `.-~` outlines.
- Do not spend rows on stars, empty sky, distant layers, or decorative particles unless they fit on the same rows as the subject.

## Subject-Specific Rules

### Moons, Planets, Spheres

- Use a 3-5 row micro-silhouette: a crescent, partial disc, or tiny sphere with a clear light and shadow side.
- Make the body feel 3D with a short spatial gradient: sparse light characters (`.`, `,`, `:`) on the lit side and dense dark characters (`@`, `#`, `0`, `8`) on the shadow side.
- The gradient must be SPATIAL: characters change gradually across the surface from left to right (or following the light source direction).
- Add crater texture using small enclosed shapes: `(  )`, `.--.`, `:::`, `''`, `o`, `O` — each crater has a rim (brighter) and interior (darker).
- Use crescent shading for moons: one side bright/sparse, other side dark/dense, with a gradual transition band.
- For rings (Saturn-like): tilted band with thickness and perspective, front edge brighter/denser, back edge lighter/broken behind the planet.
- Add surface bands or glow only within the same 3-5 rows.
- Avoid huge filled blob circles. A planet/moon should have visible surface detail with varied characters.
- Never use more than 5 non-empty rows for a Codex background subject.
- NEVER fill the interior with repeated ramp strings. Each character position should be chosen individually for its shading value.
- Do not arrange `=+*#%8@` as smooth concentric bands around a disc. That is a procedural ramp blob, not lunar texture; use broken crater rims, irregular basins, a curved terminator, and negative space instead.

### Landscapes, Forests, Cabins, Houses, Mountains, Lakes

- `scene.lines.length` must equal `background_height`. Do not provide extra rows that would be clipped.
- Use a 4-5 row icon-like skyline: roof/silhouette, facade, windows/door, foundation, then one ground/path row.
- A house/cabin must sit on visible ground in the immediately following row. Do not spend separate rows on sky or distant mountains.
- Put trees, peaks, grass, rocks, or reflections beside the subject on those same rows, not above or below it as extra layers.

### Vehicles, Machines, Buildings, Creatures

- Make the requested subject prominent enough to recognize at a glance.
- Use compressed 3D perspective within 3-5 rows: front/side outline, one panel/detail row, shadow edge, and ground/contact row.
- Use dense classic ASCII shading on the object itself; do not spend most detail budget on sky/noise.
- Add object-specific texture: metal panels, wheel wells, rivets, windows, engines, scales, feathers, fur.

### Space Scenes, Solar Systems

- Put the sun or planet as a partial edge silhouette within the footer rows.
- Draw planets with compressed crescent shading or rings; use a horizontal orbit arc on the same row instead of extra sky layers.
- Do not write planet names unless explicitly requested.

### Single Centered Object

If the user explicitly asks for a single centered object:

- Draw one recognizable object only, compressed into the final 3-5 rows.
- Keep all earlier canvas rows blank. The object's bottom row should be the final canvas row or one row above it.
- Make the object feel 3D with shaded bands or character-density ramps.
- Do not add starfields, extra scenery, captions, or palette text unless requested.
- Obey left/right placement too. If the user asks for one moon or planet on a side, keep that object there and do not invent terrain, mountains, or a skyline.
- Set `composition` to `single-centered-object`.
- Set `focal_strength` to `high`.

## Safe Zone

The patched Codex renderer paints the background ONLY into empty cells after chat rendering. In a long conversation, the reliable empty area is a footer strip roughly 3-5 rows tall.

- All rows before the footer strip: blank spaces only. Art there would usually be hidden and fragments would leak through unpredictably between messages.
- Final 3-5 rows: the complete composition, including silhouette, detail, and contact shadow/ground.
- Do not vertically center the object in the full canvas. Bottom-align it.
- Left/right placement is allowed, but preserve the complete object within the footer rows.

## Preferred Tool Flow

If Ploan MCP tools are available:

1. Call `get_terminal_info`
2. Generate a scene JSON
3. Call `render_scene` with `target: "codex"`
4. Read the returned `PLOAN_QUALITY_FEEDBACK`
5. If `passed` is false or `score` is below 78, redraw the scene using the feedback and call `render_scene` again
6. Repeat at most 3 redraw attempts, then keep the best-scoring version
7. Show only the final rendered scene and a short mood summary to the user
8. If the user re-asks or says "put it as the background" / "make it the background" / "tedd be háttérnek", ALWAYS call `render_scene` again with `target: "codex"` — even if you already rendered it. Re-render and re-save so the background file updates. Do not just reply with text.

Do not ignore quality feedback. Use it as a visual iteration loop.

When redrawing:

- Fix the specific issues listed in `PLOAN_QUALITY_FEEDBACK.issues`.
- Follow `PLOAN_QUALITY_FEEDBACK.suggestions` directly.
- Prefer a clear iconic silhouette over decorative noise.
- If the subject is too flat, make it taller and more compact.
- If it is too sparse or weak, add stronger outline/shading characters.
- If the subject looks flat or wireframe-like, redraw it with interior shading, character-density gradients, and asymmetric highlights/shadows.
- If `classic_ascii_score` is below 80, improve the 3-5 visible rows with stronger silhouette and selective texture; do not add rows.
- If `subject_prominence` is low, make the requested subject larger, clearer, or closer to the foreground.
- If `interior_texture_ratio` is below 0.6, add more internal detail characters to the subject body.
- If `canvas_overflow` appears, reduce or redesign the scene so `scene.lines.length` exactly equals `background_height`.
- If `bottom_underused`, `foreground_missing`, `subject_not_grounded`, or `subject_not_lower` appears, move the complete subject and its contact row into the final 3-5 canvas rows.
- Do not mention failed attempts or quality JSON in the final user response.

## CLI Fallback

If MCP tools are not available, use the Ploan CLI:

```bash
ploan --analyze-scene '<scene-json>'
ploan --render-scene '<best-scene-json>' --target codex --plain
```

If the score is below 78, revise the scene JSON before rendering. If the CLI also fails, directly output the scene in chat using Unicode/ASCII.

## Scene JSON Contract

```json
{
  "scene": {
    "kind": "background",
    "no_text": true,
    "full_width": true,
    "background_width": 80,
    "background_height": 20,
    "safe_zone": "codex-footer-3-5-rows",
    "style": "detailed-ascii-wallpaper",
    "composition": "codex-footer-strip",
    "subject": "compact modern house with glowing windows",
    "reference_style": "classic-ascii-gallery-inspired",
    "rendering_mode": "volumetric-shaded-ascii",
    "quality_target": "classic-ascii-art",
    "subject_priority": "bottom-aligned 3-5-row silhouette",
    "light_source": "upper-left",
    "density": "medium-high",
    "focal_strength": "high",
    "palette": {
      "background": "#0a0e1a",
      "foreground": "#e8e4d4",
      "accent": "#f5f3ce",
      "secondary": "#9a9480",
      "warning": "#c9c4a8"
    },
    "lines": []
  },
  "target": "codex",
  "plain": true
}
```

Adapt `background_width`/`background_height` to the terminal size from `get_terminal_info`. `lines` must contain exactly `background_height` entries: use blank strings for every row except the final 3-5 entries containing the art.

## Bad Output — Do NOT Produce This

```text
        .-=======-.
     .-'           '-.
    /                 \
   |                   |
    \                 /
     '-.           .-'
        '-=======-'
```

This is too tall for the Codex footer and is also a flat wireframe circle. Most of it will be hidden behind the conversation.

ALSO BAD — do not do this:

```text
   .:;i1tfLCG08@@@@@@@@   :;i1tfLCG08@@   .:;i1tfLCG0   .:;i1tfLC
```

This is just the ramp string repeated as text. It looks like gibberish, not shading. Each character must be placed individually for its visual density value.

## Good Output — Produce This Layout

Only the final five canvas rows contain this complete house; all earlier rows are blank:

```text
                         /\____/\
              __________/  []   \__________
             |  []  ##  |  __   |  ##  []  |
             |__________|_|__|__|___________|
        ~~~~~~~..,,____/          \____,,..~~~~~~~
```

The roof, facade, windows, door, foundation, and path all survive together in the 5-row footer. For other subjects, use the same compression principle rather than copying the house.

## Fallback If ANSI Is Stripped

If the terminal strips ANSI colors, preserve the art with plain Unicode. The visible shape matters more than raw color support. Use `plain: true` in the tool call.

Use palette summaries after the tool output, not inside the scene background:

```text
Palette: lunar silver / crater gray / deep space navy / starlight white
Mood: quiet night, ancient surface, silent orbit
```
