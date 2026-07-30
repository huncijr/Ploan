# Ploan Registration Guide

How terminal clients connect to Ploan's one-prompt visual renderer.

---

## Core Concept

Ploan is an **MCP renderer for prompt-made terminal art**.

A coding assistant or CLI host turns the user's prompt into a scene. Ploan renders it.

The minimum successful integration is not terminal palette mutation. The minimum successful integration is:

```text
/Ploan cyberpunk
→ the prompt becomes visible ASCII/Unicode/ANSI terminal art
→ Ploan renders it in the terminal output or background layer
```

---

## Tool Contract

### Required Tools

| Tool | Purpose |
|------|---------|
| `render_scene` | Render a prompt-generated terminal visual surface |
| `get_terminal_info` | Return terminal width, color support, OS, host context |

### Recommended Tools

| Tool | Purpose |
|------|---------|
| `render_dashboard` | Render framed dashboards / prompt banners |
| `apply_palette` | Optional terminal color palette changes |
| `customize_environment` | Composite: scene + palette + Web UI CSS |
| `restore_environment` | Restore optional palette changes |
| `list_themes` | Reference palettes for inspiration |

### Scene Input Shape

```json
{
  "scene": {
    "title": "NIGHT CITY MODE",
    "subtitle": "Cyberpunk 2077 terminal visual surface",
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
      "║  ░▒▓ neon skyline / scanline haze / chrome rain ▓▒░        ║",
      "╚════════════════════════════════════════════════════════════╝"
    ]
  },
  "apply_terminal_palette": true
}
```

---

## 1. OpenCode

OpenCode is the primary test target.

### Register MCP Server

Add to `~/.opencode.json`:

```json
{
    "mcpServers": {
        "ploan": {
            "command": "python3",
            "args": ["~/.ploan/mcp/server.py"],
            "type": "stdio"
        }
    }
}
```

### Install Custom Command

Copy:

```bash
cp opencode/ploan.md ~/.config/opencode/commands/ploan.md
```

Then restart OpenCode and type:

```text
/Ploan cyberpunk 2077 night city
/Ploan ocean depths with bioluminescent vibes
/Ploan spaceship cockpit orbiting saturn
```

Expected behavior:
- OpenCode sends `ploan.md` as prompt instructions to the AI
- The assistant creates visible terminal art
- Ploan renders it or the assistant prints it directly
- The output is a visual surface, not only "theme applied"

### Patched OpenCode Background Layer

Standard OpenCode can only show the scene as chat/output. To use it as a persistent TUI layer, build and run the patched binary:

```bash
scripts/opencode/install_patched_opencode.sh
opencode-ploan --pure
```

Inside OpenCode:

```text
/Ploan sunset forest cabin, clouds, pine trees, no text
/Ploan-reset
```

From a terminal:

```bash
ploan --reset
ploan-reset
```

The patch adds a small OpenTUI render hook that reads:

```text
~/.ploan/opencode/background.txt
```

and paints it as a full-width low-z-index OpenTUI background inside the root TUI component.

---

## 2. Grok Build

Grok Build has the richest native TUI architecture. Future integration should target:

- MCP tool registration
- Plugin marketplace package
- Visual-surface rendering as conversation blocks
- Optional `Theme` struct integration for matching palettes

Config sketch:

```toml
[tools.mcp.ploan]
command = "python3"
args = ["~/.ploan/mcp/server.py"]
type = "stdio"
```

---

## 3. Claude Code

Claude Code is MCP-native. Register Ploan as an MCP server and instruct Claude to call `render_scene` when the user asks for `/Ploan`-style visual theming.

```json
{
  "mcpServers": {
    "ploan": {
      "command": "python3",
      "args": ["~/.ploan/mcp/server.py"],
      "type": "stdio"
    }
  }
}
```

---

## 4. Other CLIs

| CLI | Integration |
|-----|-------------|
| `llm` | pluggy command + tool registration |
| `open-interpreter` | PluginManifest + MCP server |
| `ollama` | Tool registry exposing `render_scene` |
| `aichat` | YAML function declarations calling `ploan --render-scene` |

---

## Quick Install

```bash
./ploan.sh install
./ploan.sh --opencode
```

Important: after updating `opencode/ploan.md`, copy it into `~/.config/opencode/commands/ploan.md` and restart OpenCode. Otherwise OpenCode may keep using an older command prompt.
