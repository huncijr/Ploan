# Ploan — AI-Generated Terminal Background

The user invoked `/Ploan $THEME_DESCRIPTION`.

You are the creative engine. Ploan is the renderer.

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
- Use negative space intentionally so OpenCode remains readable.
- Use parallax bands, arcs, terrain, clouds, waves, trees, buildings, planets, rays, or silhouettes depending on the theme.
- Avoid huge filled blob circles. If drawing planets/stars/moons, use crescent shading, rings, contour lines, glow, rays, surface bands, and nearby smaller bodies.
- Avoid placing the main focal subject behind the OpenCode logo/input safe zone. Keep primary objects away from the horizontal center around rows 5-16; place them left, right, upper corners, lower horizon, or as wide background bands.

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
4. Optionally call `apply_palette` or `customize_environment`
5. Show the rendered scene to the user

If MCP tools are not available yet, run the CLI renderer instead:

```bash
python3 ~/.ploan/src/Ploan_skill.py --render-scene '<scene-json>' --plain
```

This both prints the visible scene and writes it to:

```text
~/.ploan/opencode/background.txt
```

The patched `opencode-ploan --pure` binary reads that file as its background layer.

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
