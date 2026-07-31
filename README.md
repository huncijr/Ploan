```
  ╔═╗╦  ╔═╗╔═╗╔╗╔
  ╠═╝║  ║ ║╠═╣║║║
  ╩  ╩═╝╚═╝╩ ╩╝╚╝
```

# Ploan — Make Your Terminal Beautiful With One Prompt

![Ploan logo](Images/ploan-logo.png)

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

## Try It In OpenCode

Ploan ships as an OpenCode custom command plus an MCP server. The AI reads your
prompt, designs an image-like ASCII/Unicode scene, and renders it straight into
your terminal — no plugins, no theme files.

### 1. Install

```bash
./ploan.sh install
./ploan.sh --opencode
```

This installs the `/Ploan` and `/Ploan-reset` commands into OpenCode, copies the
MCP server to `~/.ploan/`, and configures `~/.opencode.json` automatically.

### 2. Restart OpenCode

The `/Ploan` command and the Ploan MCP server load on OpenCode startup.

### 3. Generate a background

Type in the OpenCode chatbox:

```text
/Ploan cyberpunk 2077 night city
/Ploan ocean depths with bioluminescent vibes
/Ploan spaceship dashboard orbiting saturn
```

The expected result is a visible themed terminal surface — not just "theme
applied" text. OpenCode shows the rendered art directly in the conversation.

### 4. Persistent TUI background layer (optional)

To paint the scene as an OpenCode TUI background layer behind the UI, use the
patched build:

```bash
scripts/opencode/install_patched_opencode.sh
opencode-ploan --pure
```

Then generate or replace the background from the OpenCode chatbox:

```text
/Ploan misty mountain village, pine trees, clouds, lake reflection, no text
```

### 5. Reset

Clear the current background:

```text
/Ploan-reset
```

Or from a terminal:

```bash
ploan --reset
# or
ploan-reset
```

Ploan writes the current OpenCode surface to:

```text
~/.ploan/opencode/background.txt
```

---

## Universal Usage

The Ploan renderer and MCP tools work the same way everywhere — OpenCode, Codex,
Claude Code, or any MCP-capable agent. The AI calls the same tools; only the host
integration differs.

### Tools Exposed

| Tool | Purpose |
|------|---------|
| `render_scene` | Render a prompt-generated ANSI/Unicode scene |
| `render_dashboard` | Render a framed mini dashboard or prompt banner |
| `customize_environment` | Composite: scene + optional palette + optional Web UI CSS |
| `get_terminal_info` | Terminal width, color support, OS, host context |
| `restore_environment` | Reset optional terminal palette changes |
| `reset_background` | Clear the current patched host background layer |
| `list_themes` | List built-in reference palettes |

### CLI

```bash
ploan --info                # Show terminal info for the AI agent
ploan --demo cyberpunk      # Render a demo visual surface
ploan --render-scene '<json>' --plain
ploan --analyze-scene '<json>'
ploan --apply '<json>'      # Composite: render scene + optional palette
ploan --list                # List built-in reference palettes
ploan --restore             # Restore terminal palette state
ploan --reset               # Clear the current background
ploan --target codex        # Save/reset a host-specific background
```

### Visual Outputs

- ASCII art
- ANSI colored blocks
- Unicode box drawing
- Braille pixel art
- Half-block art: `▀`, `▄`, `█`
- ANSI gradients
- Themed prompt banners
- Framed dashboards
- Chat response visual surfaces
- Optional mini TUI dashboards

### Codex

Install the Codex skill and MCP config:

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

---

## Project Status

- OpenCode command + MCP renderer: working
- Persistent OpenCode background layer: working through `opencode-ploan --pure`
- Prompt quality feedback loop: working
- Codex skill + MCP flow: working
