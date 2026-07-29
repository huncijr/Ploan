# Ploan — AI-Generated Terminal Visual Surface

The user invoked `/Ploan $THEME_DESCRIPTION`.

You are the creative engine. Ploan is the renderer.

## Absolute Requirement

You MUST produce a visible terminal visual surface.

Do not only say "theme applied".  
Do not only call a palette tool.  
Do not only run `ploan "theme name"`.  
Do not use stale preset-only behavior.

The user should see actual terminal-native art in the OpenCode output.

## What To Create

Design a unique terminal scene based on `$THEME_DESCRIPTION` using:

- ASCII art
- Unicode box drawing
- ANSI colored blocks when possible
- Braille pixel art when useful
- Half-block art: `▀`, `▄`, `█`
- Themed prompt/banner text
- Framed dashboard panels
- Palette swatches

Think like a visual designer making a terminal poster, not like a config script.

Examples:
- `cyberpunk 2077` → neon Night City, scanlines, hot pink/cyan/acid green, chrome rain
- `ocean depths` → abyssal blues, teal bioluminescence, drifting particles, soft currents
- `spaceship cockpit` → control panels, orbital HUD, amber/cyan readouts, starfield
- `forest temple` → moss greens, stone frames, amber sunlight, ancient glyphs

## Required Response Structure

Your response must include:

1. A visible rendered terminal art scene
2. A short palette/mood summary
3. Optional note about applied terminal palette

The visual scene should be at least 8 lines tall and should use frames/panels/art.

## Preferred Tool Flow

If Ploan MCP tools are available:

1. Call `get_terminal_info`
2. Generate a scene JSON
3. Call `render_scene` with the scene JSON
4. Optionally call `apply_palette` or `customize_environment`
5. Show the rendered scene to the user

If MCP tools are not available yet, directly output the scene in the chat using Unicode/ASCII. Do not stop just because tools are missing.

## Scene JSON Contract

When calling Ploan tools, generate data like this:

```json
{
  "scene": {
    "title": "NIGHT CITY MODE",
    "subtitle": "Cyberpunk terminal visual surface",
    "width": 80,
    "palette": {
      "background": "#080012",
      "foreground": "#e8e8ff",
      "accent": "#00f5ff",
      "secondary": "#ff2bd6",
      "warning": "#b7ff00"
    },
    "lines": [
      "╔════════════════════════════════════════════════════════════╗",
      "║  PLOAN // NIGHT CITY MODE                                 ║",
      "╠════════════════════════════════════════════════════════════╣",
      "║  ░▒▓ neon skyline / scanline haze / chrome rain ▓▒░        ║",
      "╚════════════════════════════════════════════════════════════╝"
    ]
  },
  "apply_terminal_palette": true
}
```

## Fallback If ANSI Is Stripped

If OpenCode strips ANSI colors, preserve the art with plain Unicode. The visible shape matters more than raw color support.

Use palette summaries after the art:

```text
Palette: abyssal navy / bioluminescent teal / plankton cyan / pearl white
Mood: quiet pressure, deep sea glow, slow-moving terminal current
```

## Bad Output

Do not produce this:

```text
Cyberpunk theme applied. Terminal: Ptyxis.
```

That fails Ploan's purpose.

## Good Output

Produce something like:

```text
╔════════════════════════════════════════════════════════════╗
║  PLOAN // ABYSSAL BLOOM                                   ║
╠════════════════════════════════════════════════════════════╣
║  ░▒▓ deep ocean terminal surface / bioluminescent haze ▓▒░ ║
║                                                            ║
║        ⣀⣤⣶⣿⣿⣶⣤⣀          teal light below         ║
║     ⣴⣿⠟⠋⠁  ⠈⠙⠻⣿⣦     drifting code current      ║
║     ⣿⡇   ▄▄  ▄▄   ⢸⣿     cyan plankton sparks       ║
║     ⠻⣿⣦⣀      ⣀⣴⣿⠟                                  ║
║                                                            ║
║  #061826   #00e5ff   #39ffbf   #7dd3fc   #e0ffff          ║
╚════════════════════════════════════════════════════════════╝
```

Then briefly explain what you designed.
