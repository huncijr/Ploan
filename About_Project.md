# Ploan — Universal AI-Driven Terminal & Web UI Customization

An MCP tool suite that lets AI coding agents transform your entire development environment visually.

---

## 1. Architecture

```
User types: /Ploan "make it cyberpunk"
       │
       ▼
┌─────────────────┐
│   AI CLI Host    │  (OpenCode / Grok Build / Claude Code)
│  ┌─────────────┐ │
│  │ AI Agent    │ │  ← Interprets the request, generates colors + assets
│  └──────┬──────┘ │
│         │ calls MCP tools
│  ┌──────┴──────┐ │
│  │ Ploan MCP   │ │  ← Our MCP server (this project)
│  │   Server    │ │
│  └──────┬──────┘ │
└─────────┼────────┘
          │
    ┌─────┴──────┐
    ▼            ▼
┌────────┐  ┌──────────┐
│Terminal│  │  Web UI  │
│Styler  │  │  Bridge  │
└───┬────┘  └────┬─────┘
    │            │
    │  Applies   │  Injects
    │  colors    │  CSS themes
    │  + bg img  │  via hot-
    │  + opacity │  reload API
    │            │
    ▼            ▼
Running       Grokbuild
Terminal      Dev Server
(Kitty,       (live web
Alacritty,    dashboard
Ghostty,      theme update)
GNOME Term,
Foot, etc.)
```

### Key insight: Ploan is an AI tool, not a standalone themer

The AI agent (not Ploan) decides what "cyberpunk" means. The AI:
1. Interprets natural language → generates a color palette
2. Generates an SVG for the terminal background
3. Writes CSS for the Web UI dashboard
4. Calls Ploan MCP tools with the completed assets

Ploan receives those assets and **applies** them to the running environment.

---

## 2. Components

### A. MCP Server (`mcp/server.py`)
The main interface. Exposes three tools to the AI agent:

| Tool | Purpose |
|------|---------|
| `customize_environment` | Apply a complete theme: colors, background image, opacity, TUI theme, Web UI CSS |
| `get_terminal_info` | Report terminal type, color depth, OS — helps the AI generate compatible assets |
| `restore_environment` | Reset terminal, TUI, and Web UI to their pre-Ploan state |
| `list_themes` | Show built-in theme presets the AI can use as starting points |

All tools use MCP protocol (JSON-RPC over stdio), compatible with any MCP-capable AI CLI.

### B. Terminal Styler (`src/styler.py`)
Applies the AI-generated assets to the running terminal:

| What | How |
|------|-----|
| **Color palette** | OSC escape sequences (`\033]4;N;#RRGGBB`) for universal support, plus terminal-specific APIs |
| **Background image** | Kitty `set-background-image`, Alacritty live config, Foot `.ini`, GNOME Terminal `gsettings` |
| **Window opacity** | Kitty `set-background-opacity`, GNOME Terminal `background-transparency-percent`, Alacritty `window.opacity` |
| **TUI theme** | Writes to the host CLI's theme config (e.g. OpenCode `.opencode.json` `tui.theme`) |
| **State save/restore** | Saves current settings before applying; restores on `reset` |

### C. Web UI Bridge
Connects to a running Grokbuild dev server via WebSocket or hot-reload API to inject CSS themes into the live dashboard.

### D. Theme Presets Library
A set of hand-crafted color palettes the AI can use as starting points or fallbacks — Tokyo Night, Catppuccin, Dracula, Cyberpunk, Gruvbox, etc.

---

## 3. Resource Hunt — What to Find & Download

Before building, scout the open-source ecosystem for tools that already handle parts of terminal theming:

### Terminal Manipulation Scripts
- [x] Kitty remote control (`kitty @ set-colors`, `set-background-image`, `set-background-opacity`)
- [x] Alacritty IPC (`alacritty msg config`)
- [x] GNOME Terminal profiles (`gsettings` / `dconf`)
- [x] Foot `.ini` config with `SIGUSR1` hot-reload
- [x] Ghostty `set-colors` CLI
- [x] Direct OSC escape sequence injection (universal fallback)

### MCP / Tool-Use Templates
- [x] MCP server boilerplate with stdio transport
- [x] JSON Schema for OpenAI/Anthropic function calling compatibility
- [x] OpenCode `.opencode.json` MCP server config format
- [x] Grok Build plugin marketplace + theme hook architecture

### Grokbuild Web UI Bridge
- [ ] Grokbuild hot-reload / HMR API
- [ ] WebSocket endpoint for live CSS injection
- [ ] File-watcher for auto-deploy of theme assets

---

## 4. Deliverables

| # | File | Description | Status |
|---|------|-------------|--------|
| 1 | `src/` | Terminal styler + theme presets + CLI entrypoint | Done |
| 2 | `mcp/server.py` | MCP server with 4 tools | Done |
| 3 | `opencode/` | OpenCode custom command `.md` + MCP config | Done |
| 4 | `ploan.sh` | One-command installer + runner | Done |
| 5 | `ai_cli_analysis/analysis/SUMMARY.md` | Integration report from CLI analysis mission | Done |
| 6 | `ai_cli_analysis/analysis/*.json` | Per-repo analysis (9 JSON files) | Done |
| 7 | `REGISTRATION.md` | How to register Ploan in each target CLI | Done |
| 8 | `scripts/` | OS-specific installer scripts | Done |

---

## 5. Success Definition

A user types `/Ploan "make it cyberpunk"` in their AI CLI of choice. The AI agent:

1. Interprets the description and generates a color palette + background SVG + CSS
2. Calls Ploan's `customize_environment` MCP tool with those assets
3. The terminal colors, background image, and opacity update instantly
4. The host CLI's TUI theme switches to match
5. If a Grokbuild Web UI is running, it hot-reloads with the new CSS

All in seconds. No manual config editing. No restarting.

---

## 6. Phases

| Phase | Status | Description |
|-------|--------|-------------|
| **Phase 1: CLI Analysis** | Done | 9/9 repos analyzed. Top target: grok-build (10/10) |
| **Phase 2: Core Implementation** | In progress | MCP server, terminal styler, CLI tools |
| **Phase 3: Registration** | Planned | Install guides for each target CLI |

---

## 7. See Also

- [README.md](./README.md) — Quick overview & quick start
- [Instructions.md](./Instructions.md) — Phase 2 implementation instructions
- [ai_cli_analysis/analysis/SUMMARY.md](./ai_cli_analysis/analysis/SUMMARY.md) — Phase 1 integration report
