# Ploan — AI-Driven Terminal & TUI Theming Toolkit

Ploan gives AI coding agents (OpenCode, Grok Build, Claude Code) the power to visually transform your terminal environment in real time.

---

## What Ploan Does

Ploan is an **MCP tool suite** — not a standalone theming engine. The AI agent decides what the theme should look like; Ploan handles the application.

```
User: /Ploan "make it cyberpunk with neon green"
   │
   ▼
AI Agent interprets the request, generates colors and assets
   │
   ▼
AI calls Ploan MCP tools: customize_environment({colors, background, opacity, ...})
   │
   ▼
Ploan applies everything to the running terminal, TUI, and Web UI
```

| The AI does | Ploan does |
|-------------|------------|
| Understands natural language ("cyberpunk", "ocean vibes") | Receives structured color palette + assets |
| Generates color palettes and SVG backgrounds | Applies colors to the terminal via escape sequences / terminal APIs |
| Writes CSS for the Web UI dashboard | Sets terminal background image and opacity |
| Decides which TUI theme fits best | Writes TUI theme config for OpenCode, Grok Build, etc. |
| Orchestrates the full theming flow | Injects CSS into the running Grokbuild dev server |
| | Saves theme state and can restore the original appearance |

---

## Tools Exposed

### `customize_environment`
The main tool. Takes a complete theme description from the AI and applies it.

| Parameter | Type | Description |
|-----------|------|-------------|
| `palette` | object | 16 ANSI colors + foreground + background + cursor + accent in hex |
| `background_svg` | string | SVG markup to render as terminal background image |
| `opacity` | number | Terminal window opacity (0.0 – 1.0) |
| `tui_theme` | string | TUI theme name to set for the host AI CLI (e.g. `"tokyonight"`) |
| `web_ui_css` | string | CSS to inject into a running Grokbuild Web UI |

### `get_terminal_info`
Returns terminal type, color support level, and OS so the AI can generate compatible assets.

### `restore_environment`
Resets the terminal, TUI theme, and Web UI to their state before Ploan was invoked.

---

## Supported Targets

| Target | Integration | Status |
|--------|-------------|--------|
| **OpenCode** | MCP server + custom command (`.md`) | Ready |
| **Grok Build** | MCP server + theme hook + plugin marketplace | Ready |
| **Claude Code** | MCP server (stdio transport) | Ready |
| **llm** | pip-installable pluggy plugin | Planned |
| **open-interpreter** | PluginManifest + MCP server | Planned |
| **ollama** | Tool registry registration | Planned |

---

## Quick Start

```
# Install
./ploan.sh install

# In OpenCode, after AI generates a theme:
/Ploan cyberpunk
```

The AI in your CLI now has the power to make your terminal beautiful.

---

## Project Status

**Phase 1:** 9 AI CLI codebases analyzed for extensibility patterns — Done  
**Phase 2:** Ploan MCP server + core application engine — In Progress  
**Phase 3:** Registration guides for all target CLIs — Planned

See [ai_cli_analysis/analysis/SUMMARY.md](./ai_cli_analysis/analysis/SUMMARY.md) for the full Phase 1 report with grok-build ranked #1.

---

## Repository

`huncijr/Ploan`
