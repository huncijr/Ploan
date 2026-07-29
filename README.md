# Ploan — AI-Generated Terminal Visual Surfaces

Ploan gives AI coding agents the ability to create visible terminal-native art: ASCII scenes, ANSI gradients, Unicode dashboards, themed banners, and optional Web UI overlays.

The point is not just to change colors. The point is for the AI to **make something beautiful in the terminal**.

---

## What Ploan Does

Ploan is an **MCP tool suite and renderer**. The AI agent is the creative engine.

```
User: /Ploan "ocean depths with bioluminescent vibes"
   │
   ▼
AI Agent imagines the scene and designs the surface
   │
   ▼
AI calls Ploan tools: render_scene({scene, palette, lines, layout})
   │
   ▼
Ploan renders visible terminal art in the AI CLI session
```

| The AI does | Ploan does |
|-------------|------------|
| Interprets the vibe and visual direction | Renders the AI's scene as terminal-safe output |
| Designs ASCII/Unicode composition | Applies ANSI colors, gradients, frames, swatches |
| Chooses palette and mood | Provides terminal size/capability info |
| Writes optional Web UI CSS | Optionally applies terminal palette / cursor colors |
| Orchestrates the experience | Can restore optional terminal changes |

---

## Visual Outputs

Ploan can render:

- ASCII art
- ANSI colored blocks
- Unicode box drawing
- Braille pixel art
- Half-block art: `▀`, `▄`, `█`
- ANSI gradients
- Themed prompt banners
- Framed dashboards
- OpenCode chat response visual surfaces
- Optional mini TUI dashboards

Example target output:

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

---

## Tools Exposed

### `render_scene`
Render an AI-generated ANSI/Unicode scene.

### `render_dashboard`
Render a framed mini dashboard or prompt banner.

### `customize_environment`
Composite tool: render scene, optionally apply palette, optionally inject Web UI CSS.

### `get_terminal_info`
Returns terminal width, color support, OS, and host context so the AI can generate compatible art.

### `restore_environment`
Resets optional terminal palette changes.

---

## Supported Targets

| Target | Integration | Status |
|--------|-------------|--------|
| **OpenCode** | MCP server + custom command prompt | Primary test target |
| **Grok Build** | MCP server + future theme/visual hooks | Planned |
| **Claude Code** | MCP server | Planned |
| **llm** | pluggy plugin | Planned |
| **open-interpreter** | PluginManifest + MCP | Planned |

---

## Quick Start

```bash
./ploan.sh install
./ploan.sh --opencode
```

Then in OpenCode:

```text
/Ploan cyberpunk 2077 night city
/Ploan ocean depths with bioluminescent vibes
/Ploan spaceship dashboard orbiting saturn
```

The expected result is a visible themed terminal surface, not just "theme applied" text.

### OpenCode Background Layer

To make the generated visual surface appear as an OpenCode TUI layer, use the patched OpenCode build:

```bash
scripts/opencode/install_patched_opencode.sh
opencode-ploan --pure
```

Generate or replace the background from the OpenCode chatbox:

```text
/Ploan misty mountain village, pine trees, clouds, lake reflection, no text
```

Clear the current background from the OpenCode chatbox:

```text
/Ploan-reset
```

Clear it from a terminal:

```bash
ploan --reset
# or
ploan-reset
```

Ploan writes the current surface to:

```text
~/.ploan/opencode/background.txt
```

The patched OpenCode reads that file during its OpenTUI render pass and paints it as a low-z-index, full-width ASCII/Unicode background. By default, `/Ploan` should generate image-like scenery or object art rather than text banners.

---

## Project Status

**Phase 1:** 9 AI CLI codebases analyzed for extensibility patterns — done  
**Phase 2A:** Documentation realigned around terminal visual surfaces — in progress  
**Phase 2B:** `render_scene` / ANSI renderer — next  
**Phase 2C:** OpenCode UX validation — next

See [About_Project.md](./About_Project.md) for the full architecture.
