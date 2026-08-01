# Ploan — Prompt-Made Terminal Background

The user invoked `/Ploan $THEME_DESCRIPTION`.

Turn the user's prompt into a beautiful terminal background. Ploan is the renderer.

## Absolute Requirement

You MUST produce a visible terminal background.

Do not only say "theme applied".  
Do not only call a palette tool.  
Do not only run `ploan "theme name"`.  
Do not use stale preset-only behavior.

The user should get actual terminal-native background art in the OpenCode TUI.

## What To Create

Design a unique image-like terminal background based on `$THEME_DESCRIPTION` using:

- ASCII art
- Unicode box drawing
- ANSI colored blocks when possible
- Braille pixel art when useful
- Half-block art: `▀`, `▄`, `█`
- Landscape/object silhouettes
- Clouds, sun/moon, mountains, trees, water, houses, cities, spaceships, creatures, etc.
- Full-width composition that feels like a generated image converted to ASCII

Think like an image generator making a beautiful wallpaper, then translating it into ASCII/Unicode.

## Classic ASCII Reference Style

Use classic public ASCII-gallery craft as a style target, including the kind of dense, shaded forms seen in old ASCII art collections such as ascii.co.uk. This is inspiration only: do not copy, reproduce, memorize, or closely paraphrase any external artwork, signatures, author tags, or complete compositions.

Borrow techniques, not art:

- character-density ramps for light and shadow, such as ` .,:;i1tfLCG08@`, `.-:=+*#%@`, `$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,^\`'.`
- solid silhouettes plus internal texture, not just outlines
- asymmetric highlights and shadow-side density
- perspective distortion, occlusion, and foreground/background depth
- object-specific texture: metal panels, wheel wells, bark, feathers, scales, clouds, terrain, fabric folds, water ripples, etc.
- old-school ASCII shading letters/numbers like `M`, `N`, `8`, `U`, `o`, `d`, `P`, `@`, `$` when they improve shape and depth

For every subject, first imagine a strong classic ASCII silhouette, then add internal shading and texture. The result should feel hand-crafted and recognizable, not like a generated wireframe.

### Where ideas come from

The user can ask for any subject, so no fixed example set covers everything.

- **The user may browse for inspiration.** To get a specific look, the user can browse a public gallery such as https://ascii.co.uk/art, pick a style or subject they like, and describe that *style* in the prompt (for example "a dense, old-school shaded tilted-ring Saturn" or "a classic ASCII-gallery moon with crater texture"). When useful, suggest this to the user.
- **The AI generates original art, never a 1:1 copy.** When the user references a gallery artwork or style, create a new, hand-crafted composition that borrows the *techniques* (density ramps, shading, perspective, texture, composition) — not the exact artwork. Never reproduce, trace, or closely paraphrase a specific external composition, and never include signatures, author tags, or attribution lines.

## Default Visual Rule

Do NOT include readable words, labels, titles, captions, debug text, palette lines, or banners unless the user explicitly asks for text.

Default output should be scenery/object art only. For example, if the user asks for a forest cabin, draw trees, clouds, sun/moon, cabin, path, fog, and terrain. Do not write `PLOAN / FOREST CABIN` or `Palette:` in the background.

The chat response may include a short one-line summary after the tool result, but the scene JSON `lines` should be mostly non-text art.

Examples:
- `cyberpunk 2077` → skyline silhouettes, rain, neon blocks, wires, distant towers, no readable signs
- `ocean depths` → waves, whale/jellyfish silhouettes, bubbles, corals, drifting particles
- `spaceship cockpit` → starfield, planet curve, HUD arcs, ship window geometry, no labels
- `forest temple` → trees, stone shapes, moon/sun rays, fog, ancient silhouettes, no captions

## Required Response Structure

Your response must include:

1. A visible rendered terminal art background
2. A short palette/mood summary outside the background if useful
3. Optional note about applied terminal palette

The scene should be at least 12 lines tall, use the full terminal width, and avoid framed poster/panel layouts unless the user explicitly asks.

## Quality Bar

Generate a wallpaper-grade ASCII/Unicode image, not a small icon or simple banner.

- Prefer 28-40 scene lines when possible.
- Prefer 160-220 columns when possible.
- Use layered composition: far background, midground, foreground.
- Use large recognizable silhouettes and contours, not only random particles.
- Use volumetric ASCII: combine outline, interior shading, texture, and light/dark character ramps so objects feel 3D, not like flat wireframes.
- Prefer rich ASCII ramps for solid objects: ` .,:;i1tfLCG08@`, `.-:=+*#%@`, `░▒▓█`, and structural characters such as `()[]{}\/|_~^` depending on the style.
- For organic or rounded subjects, use staggered contours and internal shading bands, not only symmetric `.-~` outlines.
- Use negative space intentionally so OpenCode remains readable.
- Use parallax bands, arcs, terrain, clouds, waves, trees, buildings, planets, rays, or silhouettes depending on the theme.
- Avoid huge filled blob circles. If drawing planets/stars/moons, use crescent shading, rings, contour lines, glow, rays, surface bands, and nearby smaller bodies.
- Avoid placing the main focal subject behind the OpenCode logo/input safe zone. Keep primary objects away from the horizontal center around rows 5-16; place them left, right, upper corners, lower horizon, or as wide background bands.

Exception: if the user explicitly asks for a single centered object, obey the request. Make a clean icon-like composition with mostly blank space, no extra scenery, no labels, and no decorative clutter unless requested.

Before calling Ploan, design the scene like a complete generated image converted to ASCII. A good background has depth and composition, not just one centered object.

## Safe Zone

OpenCode renders important UI near the top/middle. The background can have subtle texture there, but do not put the main subject directly behind it.

Use this composition rule:

- top/middle center: low-detail stars, haze, tiny particles only
- left/right sides: large focal objects are allowed
- lower third: horizon, terrain, waves, forests, city silhouettes, orbit arcs
- edges/corners: bright objects, suns, moons, planets, trees, buildings

## Preferred Tool Flow

If Ploan MCP tools are available:

1. Call `get_terminal_info`
2. Generate a scene JSON
3. Call `render_scene` with the scene JSON
4. Read the returned `PLOAN_QUALITY_FEEDBACK`
5. If `passed` is false or `score` is below 72, redraw the scene using the feedback and call `render_scene` again
6. Repeat at most 2 redraw attempts, then keep the best-scoring version
7. Optionally call `apply_palette` or `customize_environment`
8. Show only the final rendered scene and a short mood summary to the user

Do not ignore quality feedback. Use it as a small visual iteration loop: inspect what you rendered, compare it to the user's requested subject/composition, and improve weak silhouettes before finalizing.

When redrawing:

- Fix the specific issues listed in `PLOAN_QUALITY_FEEDBACK.issues`.
- Follow `PLOAN_QUALITY_FEEDBACK.suggestions` directly.
- Prefer a clear iconic silhouette over decorative noise.
- If the subject is too flat, make it taller and more compact.
- If it is too sparse or weak, add stronger outline/shading characters.
- If the subject looks flat or wireframe-like, redraw it with interior shading, character-density gradients, and asymmetric highlights/shadows.
- If `classic_ascii_score` is below 75, redraw in a denser old-school ASCII style inspired by public ASCII galleries, without copying any existing artwork.
- If `subject_prominence` is low, make the requested subject larger, clearer, or closer to the foreground.
- If `safe_zone_overlap` is high and the subject is not explicitly requested in the center, move the focal subject away from the OpenCode logo/input area.
- If `canvas_overflow` appears, reduce or redesign the scene so `scene.lines.length` exactly equals `background_height`; clipped extra rows are not acceptable.
- If `bottom_underused`, `foreground_missing`, `house_not_prominent`, or `subject_not_grounded` appears, redraw with stronger foreground terrain and a clearly grounded subject.
- If the user asked for a centered object, keep the object's bounding box close to center.
- Do not mention failed attempts or quality JSON in the final user response.

If MCP tools are not available yet, run the CLI renderer instead:

```bash
ploan --analyze-scene '<scene-json>'
ploan --render-scene '<best-scene-json>' --plain
```

Use `--analyze-scene` before the final CLI render. If the score is below 72, revise the scene JSON before rendering. The final render prints the visible scene and updates the patched `opencode-ploan --pure` background layer.

Do not read, list, inspect, or verify Ploan runtime files or directories before running the tool. In particular, do not access home-directory implementation paths such as renderer source folders or OpenCode command folders. Treat the `ploan` command and MCP tools as the public interface.

If the CLI also fails, then directly output the scene in the chat using Unicode/ASCII. Do not stop just because tools are missing.

## Scene JSON Contract

When calling Ploan tools, generate data like this:

```json
{
  "scene": {
    "title": "NIGHT CITY MODE",
    "subtitle": "Cyberpunk terminal background",
    "kind": "background",
    "no_text": true,
    "full_width": true,
    "background_width": 180,
    "background_height": 36,
    "safe_zone": "opencode-center",
    "style": "detailed-ascii-wallpaper",
    "composition": "full-scene",
    "subject": "night city skyline",
    "reference_style": "classic-ascii-gallery-inspired",
    "rendering_mode": "volumetric-shaded-ascii",
    "quality_target": "classic-ascii-art",
    "subject_priority": "foreground",
    "light_source": "upper-left",
    "density": "medium",
    "focal_strength": "medium",
    "palette": {
      "background": "#080012",
      "foreground": "#e8e8ff",
      "accent": "#00f5ff",
      "secondary": "#ff2bd6",
      "warning": "#b7ff00"
    },
    "lines": [
      "        ☁                         ☁                         ☁             ",
      "   /\\        /\\      /\\            /\\        /\\                      ",
      "  /  \\  /\\ /  \\    /  \\    /\\  /  \\  /\\ /  \\                     ",
      " /____\\/  \\____\\__/____\\__/  \\/____\\/  \\____\\__________________",
      "       ~~~~~~~~        ~~~~~~~~        ~~~~~~~~        ~~~~~~~~          "
    ]
  },
  "apply_terminal_palette": true
}
```

For solar-system or universe prompts:

- Put the sun as a partial bright disc or ray source on the far left/right/top corner, not centered.
- Draw Venus-like planets with crescent shading, cloud bands, or rings offset from the UI center.
- Add orbit arcs across the full width.
- Add asteroid dust, nebula bands, moons, star clusters, and subtle depth layers.
- Do not write planet names unless explicitly requested.

For explicit minimal planet prompts, such as "only Saturn in the OpenCode center":

- Draw one recognizable planet only.
- Keep the ring small, elliptical, and crossing behind/in front of the planet.
- Use 10-18 meaningful art rows with blank full-width rows around it.
- Make the planet body feel 3D with shaded bands or character-density ramps, for example dense characters on the shadow side and sparse `.`/`,`/`:` highlights on the lit side.
- Make the ring a tilted band with thickness and perspective: front edge brighter/denser, back edge lighter/broken behind the planet.
- Do not add starfields, moons, orbit trails, nebula bands, captions, or palette text unless requested.
- Set `composition` to `single-centered-object`.
- Set `subject` to the requested object, for example `saturn`.
- Set `focal_strength` to `high` so Ploan quality feedback expects a strong silhouette.
- Prefer simple ASCII-safe characters if using the CLI fallback; avoid apostrophes in art lines unless escaped, because they can break a single-quoted shell JSON argument.

If the user asks for a few stars around a centered object, use only 3-8 sparse stars. Do not turn the scene into a full starfield.

For vehicles, roads, machines, buildings, creatures, or other recognizable foreground objects:

- Make the requested subject prominent enough to recognize at a glance.
- Use 3D perspective where useful: front/side angle, foreshortened road lines, visible wheel ellipses, body panels, windshield, shadows, highlights.
- Use dense classic ASCII shading on the object itself; do not spend most detail budget on sky/noise if the user asked for a specific subject.
- Keep the subject out of the OpenCode prompt/logo safe zone unless the user explicitly asks for center placement.

For landscapes, forests, cabins, houses, mountains, lakes, villages, and similar scenes:

- `scene.lines.length` must equal `background_height`. Do not provide extra rows that would be clipped.
- Use the whole canvas vertically: sky in the upper rows, distant treeline/hills below it, midground forest, house/cabin in the lower-middle/foreground, and terrain/path/grass/shadows in the bottom rows.
- A house/cabin must sit on visible ground. Put path, grass, rocks, roots, water, or shadows directly under it.
- Trees should be layered behind and around the house, not floating as disconnected triangles above the roof.
- Reserve the bottom 15-25% for foreground detail; do not leave it empty or cut off the scene immediately after the house.
- If the user asks for a house in the center, make it visually central but still grounded in the lower half, not hidden behind the OpenCode input box.

Avoid weak planet output like this:

```text
        .-=======-.
     .-~   .---.   ~-.
====____     |     ____====
```

It is too flat and wireframe-like. Prefer a shaded, 3D ASCII object with dense and sparse character ramps, like classic ASCII art where the silhouette, shadow, and texture all contribute to recognizability.

## Fallback If ANSI Is Stripped

If OpenCode strips ANSI colors, preserve the art with plain Unicode. The visible shape matters more than raw color support.

Use palette summaries after the tool output, not inside the scene background:

```text
Palette: abyssal navy / bioluminescent teal / plankton cyan / pearl white
Mood: quiet pressure, deep sea glow, slow-moving terminal current
```

## Bad Output

Do not produce this:

```text
PLOAN / FOREST CABIN
Palette: green, gold, black
```

That fails Ploan's purpose.

## Good Output

Produce image-like art like:

```text
          ☁                         ☁                         ☁
     /\        /\             /\        /\
    /  \  /\  /  \     /\    /  \  /\  /  \
   /____\/  \/____\___/  \__/____\/  \/____\____________
             ~~~~~~~~          ~~~~~~~~           ~~~~~~~~
                 ___
              __/___\__              /\
             /__|___|__\        /\  /  \     /\
               |  _  |         /  \/____\   /  \
          _____|_| |_|________/____\____\__/____\________
```

Then briefly explain the palette/mood outside the background.
