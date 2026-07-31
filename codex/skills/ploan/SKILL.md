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

## Default Visual Rule

Do NOT include readable words, labels, titles, captions, debug text, palette lines, or banners unless the user explicitly asks for text.

Default output should be scenery/object art only.

## Quality Bar

Generate a compact wallpaper-grade ASCII/Unicode image for the Codex TUI.

- The Codex TUI has less empty space than other terminals: the central message area is covered by chat text, and only the margins, edges, and lower band show the background. Draw SMALL so the art fits in the visible zones.
- Prefer 14-20 scene lines (never more than 22).
- Prefer 50-80 columns, scaled to the terminal width from `get_terminal_info`. Do not build wide 180+ column scenes.
- Keep the main subject in the center-lower band of the canvas so it lands below the chat text area and stays visible.
- Use layered composition sparingly: sky/haze row, then subject, then a thin ground or shadow row. Do not fill the full height with art rows.
- Use recognizable silhouettes and contours, not only random particles.
- Use volumetric ASCII: combine outline, interior shading, texture, and light/dark character ramps so objects feel 3D, not like flat wireframes.
- Prefer rich ASCII ramps for solid objects: ` .,:;i1tfLCG08@`, `.-:=+*#%@`, `░▒▓█`, and structural characters such as `()[]{}\/|_~^`.
- For organic or rounded subjects, use staggered contours and internal shading bands, not only symmetric `.-~` outlines.
- Use negative space intentionally so the TUI remains readable.
- Do not let the art touch the very top rows (reserve them for the Codex header) and do not let it spill off the bottom.

## Subject-Specific Rules

### Moons, Planets, Spheres

- Make the body feel 3D with character-density gradients: use sparse light characters (`.`, `,`, `:`) on the lit side and dense dark characters (`@`, `#`, `0`, `8`) on the shadow side.
- The gradient must be SPATIAL: characters change gradually across the surface from left to right (or following the light source direction).
- Add crater texture using small enclosed shapes: `(  )`, `.--.`, `:::`, `''`, `o`, `O` — each crater has a rim (brighter) and interior (darker).
- Use crescent shading for moons: one side bright/sparse, other side dark/dense, with a gradual transition band.
- For rings (Saturn-like): tilted band with thickness and perspective, front edge brighter/denser, back edge lighter/broken behind the planet.
- Add surface bands, glow, rays, or nearby smaller bodies for visual interest.
- Avoid huge filled blob circles. A planet/moon should have visible surface detail with varied characters.
- Minimum 10-14 art rows for the object itself, not counting stars/space around it.
- Stars around it: 3-12 sparse, asymmetric, varied characters (`.`, `*`, `+`, `·`), not a uniform grid.
- NEVER fill the interior with repeated ramp strings. Each character position should be chosen individually for its shading value.

### Landscapes, Forests, Cabins, Houses, Mountains, Lakes

- `scene.lines.length` must equal `background_height`. Do not provide extra rows that would be clipped.
- Keep the scene compact: sky in 1-3 upper rows, one midground band, subject in the center-lower band, thin ground/shadow at the bottom.
- A house/cabin must sit on visible ground. Put path, grass, rocks, roots, water, or shadows directly under it.
- Trees should be layered behind and around the house, not floating as disconnected triangles above the roof.
- Reserve the bottom 2-3 rows for foreground detail; do not leave it empty.
- Use reflection in water: inverted/distorted version of objects above the waterline.

### Vehicles, Machines, Buildings, Creatures

- Make the requested subject prominent enough to recognize at a glance.
- Use 3D perspective: front/side angle, foreshortened lines, visible panels, shadows, highlights.
- Use dense classic ASCII shading on the object itself; do not spend most detail budget on sky/noise.
- Add object-specific texture: metal panels, wheel wells, rivets, windows, engines, scales, feathers, fur.

### Space Scenes, Solar Systems

- Put the sun as a partial bright disc or ray source on a corner/edge, not centered.
- Draw planets with crescent shading, cloud bands, or rings offset from center.
- Add orbit arcs across the full width.
- Add asteroid dust, nebula bands, moons, star clusters, and subtle depth layers.
- Do not write planet names unless explicitly requested.

### Single Centered Object

If the user explicitly asks for a single centered object:

- Draw one recognizable object only, kept SMALL and compact so it fits the visible center-lower zone of the Codex TUI.
- Use 8-14 meaningful art rows with blank rows above it and a thin ground/shadow row below.
- Keep the object's vertical center in the lower-middle of the canvas so it is not hidden behind the chat message area.
- Make the object feel 3D with shaded bands or character-density ramps.
- Do not add starfields, extra scenery, captions, or palette text unless requested.
- Set `composition` to `single-centered-object`.
- Set `focal_strength` to `high`.

## Safe Zone

The Codex TUI covers the top/middle with the header and the chat message area. The patched Codex renderer paints the background ONLY into empty cells, so art placed behind chat text is invisible.

- Top 2-4 rows: Codex header — keep this area nearly empty (a few sparse stars or haze only).
- Middle band (rows ~5 to ~70% of height): chat messages — do NOT put the main subject here; it will be hidden.
- Center-lower band (roughly the lower quarter-to-third of the canvas): this is the PRIMARY spot for the main subject. It sits below the last message and above the input line, so it stays visible.
- Left/right edges: large focal objects are also acceptable.
- Bottom edge: horizon, terrain, waves, foreground detail.
- Keep the whole drawing compact: fewer rows, tighter silhouette, more negative space.

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
- If `classic_ascii_score` is below 80, redraw in a denser old-school ASCII style with more ramp characters.
- If `subject_prominence` is low, make the requested subject larger, clearer, or closer to the foreground.
- If `interior_texture_ratio` is below 0.6, add more internal detail characters to the subject body.
- If `canvas_overflow` appears, reduce or redesign the scene so `scene.lines.length` exactly equals `background_height`.
- If `bottom_underused`, `foreground_missing`, or `subject_not_grounded` appears, redraw with stronger foreground terrain and a clearly grounded subject.
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
    "safe_zone": "codex-center-lower",
    "style": "detailed-ascii-wallpaper",
    "composition": "center-lower-subject",
    "subject": "full moon with craters in night sky",
    "reference_style": "classic-ascii-gallery-inspired",
    "rendering_mode": "volumetric-shaded-ascii",
    "quality_target": "classic-ascii-art",
    "subject_priority": "compact centered-lower subject",
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

Adapt `background_width`/`background_height` to the terminal size from `get_terminal_info`, keeping height small (14-20 rows).

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

This is a flat wireframe circle. It has no interior texture, no shading gradient, no crater detail, no 3D feel.

ALSO BAD — do not do this:

```text
   .:;i1tfLCG08@@@@@@@@   :;i1tfLCG08@@   .:;i1tfLCG0   .:;i1tfLC
```

This is just the ramp string repeated as text. It looks like gibberish, not shading. Each character must be placed individually for its visual density value.

## Good Output — Produce This Level

A small compact moon with proper spatial shading (lit from upper-left, dark lower-right), placed in the center-lower band so it stays visible in the Codex TUI:

```text
   *        .       *        .        *        .      *
        .            .         *            .
      *         .           .         *
                 .-"""""""""-.
              .-'   ::.  .:   '-.
            .'   :  o   :  :  . '.
           /  .::  .--.  :  o   \
          |  :  (    )  ::  .--. |
          |  : o (  )   :  (    )|
          |  ::  '--'  ::  (  )  |
           \ :  .--.   :   '--' /
            '. :: (  )  :  o  .'
              '-.  '--'  : .-'
                 '-..__..-'
        .   *        .       *      .        *
     *       .        *       .        *     .
```

See: craters as `(  )` and `.--.` shapes with rim highlights, sparse `:` and `.` on the lit side, denser `::` on the shadow side, 3D sphere feel from the gradient. The moon is compact (about 14 rows) and sits in the lower-middle of the canvas, well below where chat text renders.

## Fallback If ANSI Is Stripped

If the terminal strips ANSI colors, preserve the art with plain Unicode. The visible shape matters more than raw color support. Use `plain: true` in the tool call.

Use palette summaries after the tool output, not inside the scene background:

```text
Palette: lunar silver / crater gray / deep space navy / starlight white
Mood: quiet night, ancient surface, silent orbit
```
