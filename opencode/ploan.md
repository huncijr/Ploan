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
      "width": 140,
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
