# Klinx — Universal AI-Driven Terminal & Web UI Customization

A plugin/extension module that intercepts `/klinx` or `/customizable` slash commands in **any AI CLI** (Claude Code, Grok, Aider, Open Interpreter, etc.) and dynamically transforms the entire development environment.

**Type `/klinx "make it cyberpunk"` → your terminal, wallpaper, and Web UI dashboard transform instantly.**

---

## 1. Architecture

```
User types: /klinx "ship theme"
       │
       ▼
┌─────────────────┐
│   AI CLI Host    │  (Claude Code / Grok / Aider / Open Interpreter)
│  ┌─────────────┐ │
│  │ Klinx Skill │ │  ← Our injected module
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
    ▼            ▼
┌────────┐  ┌──────────┐
│ OS     │  │Grokbuild │
│Wallpaper│ │Dev Server│
│Terminal│  │(hot-reload│
│Theme   │  │ UI code) │
└────────┘  └──────────┘
```

---

## 2. Components to Build

### A. CLI Interceptor
Hooks into the host AI CLI to detect `/klinx` or `/customizable` commands.

**Input:** Slash command with theme description (e.g., `"ship theme"`)
**Output:** Triggers the Unified Styler with parsed parameters

### B. Terminal Styler (OS-specific)
Scripts that programmatically modify terminal and OS appearance:

| OS | Target | Method |
|----|--------|--------|
| **Windows** | Windows Terminal `settings.json` | PowerShell injector for `backgroundImage`, `backgroundImageOpacity`, color schemes |
| **macOS** | iTerm2 / Terminal.app | AppleScript to set background image, transparency, color profile |
| **Linux** | GNOME/KDE + terminal | `pywal` (color palette from wallpaper), `gsettings`, `konsole` profiles |

### C. Web UI Bridge (Grokbuild)
Connects the CLI to Grokbuild's dev server for live Web UI theming:
- Watch for generated HTML/React/CSS from the LLM
- Pipe code directly into Grokbuild's hot-reload pipeline
- Inject matching components on-the-fly

### D. MCP Server Wrapper
Exposes all Klinx functions as MCP tools so any MCP-compatible CLI (Claude Code, OpenCode) can call them natively:
- `customize_environment(theme, opacity, wallpaper, web_ui_code)`
- Tool schema following standard JSON Schema format

---

## 3. Resource Hunt — What to Find & Download

Before building, scout the open-source ecosystem for existing tools that already do parts of this:

### Terminal Manipulation Scripts
- [ ] Windows Terminal `settings.json` injector (PowerShell)
- [ ] macOS iTerm2 AppleScript theming utilities
- [ ] Linux `pywal` integration scripts
- [ ] Cross-platform wallpaper setter (e.g., `wallpaper` crate, Python `ctypes`)

### MCP / Tool-Use Templates
- [ ] MCP server boilerplate with filesystem/system access
- [ ] Aider custom tool schema examples
- [ ] Claude Code tool definition JSON format
- [ ] Open Interpreter skill/tool decorator templates

### Grokbuild Bridge
- [ ] Grokbuild file-watcher scripts
- [ ] Hot-reload / HMR configuration
- [ ] API for injecting code into running dev server

**Save everything to `./scripts/` with attribution.**

---

## 4. Deliverables

| # | File | Description |
|---|------|-------------|
| 1 | `./scripts/` | All downloaded utilities, themed scripts by OS |
| 2 | `./src/klinx_skill.py` (or `.ts`) | Unified Python/TypeScript module: `customize_environment()` |
| 3 | `./mcp/server.py` | MCP server wrapping all Klinx functions |
| 4 | `./ai_cli_analysis/analysis/SUMMARY.md` | Integration report from CLI analysis mission |
| 5 | `./REGISTRATION.md` | How to register Klinx inside Claude Code, Grok, Aider |

---

## 5. Success Definition

A user can type `/klinx "make it cyberpunk"` in their AI CLI of choice and within seconds:
1. Their terminal wallpaper and color scheme change to match the theme
2. Their OS desktop wallpaper updates
3. A themed TUI dashboard renders in the terminal
4. Their local Grokbuild Web UI hot-reloads with matching components

---

## 6. See Also

- [Instructions.md](./Instructions.md) — CLI analysis mission for AI agents (scout the 9 codebases)
- [README.md](./README.md) — Project overview & quick start
