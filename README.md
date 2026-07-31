# Ploan — Make Your Terminal Beautiful With One Prompt

Ploan turns a short prompt into terminal-native visual backgrounds: ASCII scenes, ANSI gradients, Unicode dashboards, themed banners, and optional Web UI overlays.

The point is not just to change colors. The point is to make your terminal feel alive with one command.

---

## What Ploan Does

Ploan is an **MCP tool suite and renderer** for prompt-made terminal visuals.

```
User: /Ploan "ocean depths with bioluminescent vibes"
   │
   ▼
Your coding assistant designs a terminal-safe scene
   │
   ▼
Ploan receives structured art: render_scene({scene, palette, lines, layout})
   │
   ▼
Ploan renders the visual surface in your terminal
```

| Prompt flow | Ploan provides |
|-------------|----------------|
| Describe a vibe, place, object, or mood | Terminal-safe rendering |
| Generate ASCII/Unicode composition | ANSI colors, gradients, frames, swatches |
| Pick palette and mood | Terminal size/capability info |
| Optionally style Web UI surfaces | Optional terminal palette / cursor colors |
| Iterate until the scene is good | Quality feedback and restore support |

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
Render a prompt-generated ANSI/Unicode scene.

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
| **Codex CLI** | Pet assets or patched ratatui background | Researched |
| **Grok Build** | MCP server + future theme/visual hooks | Planned |
| **Claude Code** | MCP server | Planned |
| **llm** | pluggy plugin | Planned |
| **open-interpreter** | PluginManifest + MCP | Planned |

See [`docs/cli-background-capabilities.md`](docs/cli-background-capabilities.md) for the current background/session-surface capability matrix.

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

The patched OpenCode reads that file during its OpenTUI render pass and paints it as a low-z-index, full-width ASCII/Unicode background. By default, `/Ploan` generates image-like scenery or object art rather than text banners.

### Codex Skill Integration

Install the Codex skill and MCP server config:

```bash
./ploan.sh --codex
```

Then restart Codex and ask:

```text
Use the ploan skill: misty mountain village, pine trees, lake reflection, cabin in lower foreground, no text
```

Ploan writes Codex-targeted surfaces to:

```text
~/.ploan/codex/background.txt
```

Stock Codex can use the skill/MCP flow for visible rendered output. A full persistent TUI background like `opencode-ploan --pure` may still require a Codex source patch.

---

## Project Status

- OpenCode command + MCP renderer: working
- Persistent OpenCode background layer: working through `opencode-ploan --pure`
- Prompt quality feedback loop: working
- Future targets: Grok Build, Claude Code, `llm`, and open-interpreter
