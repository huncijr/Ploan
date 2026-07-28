# Instructions: Phase 2 — Ploan Implementation

Build **Ploan** — an MCP tool suite that AI coding agents use to visually transform terminals, TUIs, and Web UIs in real time.

---

## 0. Quick Reference Card

| Key | Value |
|-----|-------|
| **Goal** | Build the Ploan MCP server, terminal styler, and Web UI bridge |
| **Core concept** | Ploan is **not** a standalone themer — the AI agent generates the theme assets; Ploan applies them |
| **Phase 1 Status** | **COMPLETE** — 9/9 repos analyzed, grok-build ranked #1 at 10/10 |
| **Constraint** | Read existing analysis files first. Do NOT re-clone or re-analyze repos. |
| **Output** | `src/Ploan_skill.py`, `mcp/server.py`, `scripts/`, `opencode/`, `REGISTRATION.md` |

---

## 1. What Ploan Is (and Isn't)

### Ploan IS:
- An **MCP tool suite** exposed to AI agents via stdio transport
- A **terminal styler** that applies color palettes, background images, and opacity to terminal emulators
- A **TUI theme bridge** that sets the host CLI's theme (e.g. OpenCode `tui.theme`)
- A **Web UI bridge** that injects CSS into running Grokbuild dev servers

### Ploan is NOT:
- A standalone theme generator — the AI agent does that
- A natural language → color palette translator — the AI agent does that
- A desktop wallpaper setter — we theme terminals, not OS desktops

### The flow:
```
User says "make it cyberpunk"
  → AI generates: color palette + SVG background + CSS
  → AI calls Ploan MCP tools with those assets
  → Ploan applies everything to the running environment
```

---

## 2. Project Context

See [`About_Project.md`](./About_Project.md) for the full vision, architecture, and deliverables.

---

## 3. Phase 1 Analysis (READ-ONLY — DO NOT REGENERATE)

### Top 3 Integration Points (from Phase 1)

1. **grok-build** (10/10, medium effort) — Dedicated Theme struct with 60+ semantic colors, MCP-native, plugin marketplace, ACP subagent resolution, lock-free theme hot-switching
2. **opencode** (9/10, low effort) — MCP servers in JSON config + `.md` custom commands, 9 built-in themes, Bubble Tea TUI
3. **llm** (9/10, low effort) — Pluggy `register_commands` hook, pip-installable extension

---

## 4. Implementation Plan (Phase 2)

### Step 1: MCP Server (`mcp/server.py`)
- Exposes `customize_environment`, `get_terminal_info`, `restore_environment`, `list_themes`
- Tool schemas in JSON Schema format (compatible with OpenAI/Anthropic function calling)
- Compatible with OpenCode, Claude Code, Grok Build, open-interpreter (stdio transport)

### Step 2: Terminal Styler (`src/Ploan_skill.py`)
- Receives color palette + background SVG + opacity from the AI
- Applies via terminal-specific APIs or OSC escape sequences
- Saves pre-Ploan state and supports restore
- Degrades gracefully across unsupported terminals

### Step 3: Web UI Bridge
- Connects to Grokbuild dev server
- Injects CSS via WebSocket or hot-reload API
- Watches for theme changes and pushes updates live

### Step 4: OpenCode Integration (`opencode/`)
- Custom command `.md` file for `/Ploan` slash command
- MCP server config snippet for `.opencode.json`

### Step 5: Registration (`REGISTRATION.md`)
- Per-CLI install instructions
- Config snippets for OpenCode, Claude Code, Grok Build, etc.

---

## 5. Success Criteria

- [x] Phase 1: All 9 repositories cloned and analyzed
- [x] MCP server running with 4 tools
- [x] Terminal styler applying colors + background + opacity
- [x] OpenCode custom command + MCP config ready
- [x] Installer script working
- [ ] Web UI bridge for Grokbuild
- [ ] Theme state save/restore fully tested
- [ ] Zero access to non-`huncijr/Ploan` GitHub repos

---

## 6. See Also

- [About_Project.md](./About_Project.md) — Full architecture, components, deliverables
- [README.md](./README.md) — Project overview & quick start
- [ai_cli_analysis/analysis/SUMMARY.md](./ai_cli_analysis/analysis/SUMMARY.md) — Phase 1 integration report
