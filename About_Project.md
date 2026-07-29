# Ploan — AI-Generated TUI Art & Terminal Visual Surfaces

Ploan is an MCP tool suite that lets AI coding agents create and render beautiful terminal-native visual surfaces: ASCII art, ANSI gradients, Unicode dashboards, themed banners, Braille pixel art, half-block scenes, and optional Web UI overlays.

The core idea: **the AI is the artist; Ploan is the renderer.**

---

## 1. Architecture

```
User types: /Ploan "cyberpunk 2077 night city"
       │
       ▼
┌────────────────────────────────────────────┐
│ AI CLI Host                                │
│ (OpenCode / Grok Build / Claude Code)      │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │ AI Agent                             │  │
│  │ - interprets the vibe                │  │
│  │ - designs palette                    │  │
│  │ - composes ANSI/Unicode scene        │  │
│  │ - optionally writes Web UI CSS       │  │
│  └──────────────────┬───────────────────┘  │
│                     │ calls MCP tools       │
│  ┌──────────────────▼───────────────────┐  │
│  │ Ploan MCP Server                     │  │
│  │ - render_scene(scene_json)           │  │
│  │ - apply_palette(palette_json)        │  │
│  │ - render_dashboard(layout_json)      │  │
│  │ - customize_environment(composite)   │  │
│  └──────────────────┬───────────────────┘  │
└─────────────────────┼──────────────────────┘
                      │
     ┌────────────────┼────────────────┐
     ▼                ▼                ▼
┌──────────┐   ┌──────────────┐  ┌──────────────┐
│ Terminal │   │ AI CLI Chat  │  │ Web UI       │
│ Palette  │   │ Visual       │  │ Overlay      │
│ + OSC    │   │ Surface      │  │ /Dashboard   │
└──────────┘   └──────────────┘  └──────────────┘
```

### Key Insight

Ploan is **not** a natural-language theme parser and not just a terminal color setter.

The AI designs:
- The visual concept
- The color palette
- The ASCII/Unicode composition
- The layout and framing
- The mood-specific copy
- Optional Web UI CSS

Ploan renders:
- Colored terminal art
- Box-drawing dashboards
- ANSI gradients
- Braille / half-block pixel surfaces
- Optional terminal palette changes
- Optional Web UI CSS injection

---

## 2. Visual Surface Types

Ploan can render visible terminal-native surfaces using only text, Unicode, and ANSI styling.

| Surface Type | Description |
|--------------|-------------|
| **ASCII art** | Classic text scenes, logos, skylines, ships, landscapes |
| **ANSI colored blocks** | Colored panels, swatches, bars, neon strips, status blocks |
| **Unicode box drawing** | `╔═╗`, `╭─╮`, `│`, `┌─┐` frames and dashboard layouts |
| **Braille pixel art** | Dense terminal pixel imagery using `⣿`, `⣶`, `⠿`, etc. |
| **Half-block art** | `▀`, `▄`, `█` based gradients, silhouettes, shadows |
| **ANSI gradients** | Line-by-line or character-by-character truecolor gradients |
| **Themed prompt banner** | Session headers, mode indicators, command banners |
| **Framed dashboard** | Mini control panels with palette swatches and metadata |
| **OpenCode chat visual surface** | A rendered themed scene visible directly in OpenCode output |
| **Mini TUI dashboard** | Optional separate process for live interactive dashboards |

Example direction for `/Ploan "cyberpunk 2077"`:

```text
╔════════════════════════════════════════════════════════════╗
║  PLOAN // NIGHT CITY MODE                                 ║
╠════════════════════════════════════════════════════════════╣
║        ▄▄      ▄████▄         ▄▄       neon skyline        ║
║     ▄██▀▀██▄  ██▀  ▀██     ▄██▀▀██▄                      ║
║     ██ CYBER ██ █▓▒░ ██     ██ GRID ██                    ║
║     ▀██▄▄██▀  ██▄▄▄▄██     ▀██▄▄██▀                      ║
║                                                            ║
║  ░▒▓ scanlines ▓▒░    #ff2bd6   #00f5ff   #b7ff00          ║
╚════════════════════════════════════════════════════════════╝
```

The important point is that the user must **see** the themed surface in the AI CLI session, not only receive a message saying "theme applied".

---

## 3. Components

### A. MCP Server (`mcp/server.py`)

The main interface exposed to AI agents.

| Tool | Purpose |
|------|---------|
| `render_scene` | Render an AI-generated ANSI/Unicode terminal art scene |
| `apply_palette` | Optionally apply terminal ANSI palette / foreground / background / cursor |
| `render_dashboard` | Render framed prompt banners and dashboard panels |
| `customize_environment` | Composite tool: scene + palette + TUI metadata + Web UI CSS |
| `get_terminal_info` | Report terminal size, color support, and host CLI context |
| `restore_environment` | Reset optional terminal palette changes |
| `list_themes` | Show reference palettes the AI can use for inspiration |

All tools use MCP protocol (JSON-RPC over stdio), compatible with any MCP-capable AI CLI.

### B. Terminal Art Renderer (`src/Ploan_skill.py`)

Renders AI-generated scene JSON into terminal-safe visual output.

| Capability | Description |
|------------|-------------|
| Width-aware layout | Detects terminal width and wraps/scales scenes |
| ANSI truecolor | Uses `\033[38;2;R;G;Bm` and `\033[48;2;R;G;Bm` |
| Unicode-safe fallback | Can strip ANSI while preserving box drawing / art |
| Gradients | Applies color ramps to text, borders, bars, and blocks |
| Swatches | Renders palette previews as colored cells |
| Scene layers | Box frames, headers, body art, footer metadata |

### C. AI Prompt Contract

The AI should generate structured scene data, not just choose a preset.

Example input to Ploan:

```json
{
  "scene": {
    "title": "NIGHT CITY",
    "subtitle": "Cyberpunk 2077 inspired terminal surface",
    "width": 80,
    "palette": {
      "background": "#080012",
      "foreground": "#e8e8ff",
      "accent": "#00f5ff",
      "secondary": "#ff2bd6",
      "warning": "#b7ff00"
    },
    "lines": [
      "╔════════════════════════════════════════════════════╗",
      "║  PLOAN // NIGHT CITY MODE                         ║",
      "║  ░▒▓ neon skyline / scanline haze / chrome rain ▓▒░ ║",
      "╚════════════════════════════════════════════════════╝"
    ]
  },
  "apply_terminal_palette": true,
  "web_ui_css": "... optional CSS ..."
}
```

### D. OpenCode Custom Command (`opencode/ploan.md`)

OpenCode custom commands are prompt templates. The `.md` file instructs the AI to:
1. Interpret the user theme creatively
2. Generate a visible terminal art surface
3. Call Ploan tools only when helpful
4. Always show the rendered scene in the chat/output
5. Never only say "theme applied"

### E. Web UI Bridge

Optional bridge for a running Grokbuild dev server. The AI can generate CSS matching the terminal visual surface, and Ploan can inject it into the Web UI dashboard.

### F. Optional Terminal Styler

Terminal palette / opacity changes are secondary enhancements. They can improve immersion but they are **not** the core deliverable. The core deliverable is the rendered visual surface.

---

## 4. Resource Hunt — What to Find & Download

### Terminal Rendering Techniques
- [ ] ANSI truecolor foreground/background helpers
- [ ] Gradient text renderer
- [ ] Box drawing layout utilities
- [ ] Braille pixel art conversion examples
- [ ] Half-block image approximation examples
- [ ] Terminal width detection and wrapping helpers
- [ ] ANSI stripping / no-color fallback

### MCP / Tool-Use Templates
- [x] MCP server boilerplate with stdio transport
- [x] JSON Schema for OpenAI/Anthropic function calling compatibility
- [x] OpenCode `.opencode.json` MCP server config format
- [x] Grok Build plugin marketplace + hook architecture

### Web UI Bridge
- [ ] Grokbuild hot-reload / HMR API
- [ ] WebSocket endpoint for live CSS injection
- [ ] Visual surface to CSS translation rules

---

## 5. Deliverables

| # | File | Description | Status |
|---|------|-------------|--------|
| 1 | `src/Ploan_skill.py` | CLI entrypoint + palette helpers + future scene renderer | in progress |
| 2 | `mcp/server.py` | MCP server with terminal tools | in progress |
| 3 | `opencode/ploan.md` | OpenCode prompt forcing visible AI-generated scene output | in progress |
| 4 | `ploan.sh` | Installer + runner | done |
| 5 | `REGISTRATION.md` | CLI registration guide | done |
| 6 | `ai_cli_analysis/analysis/SUMMARY.md` | Integration report | done |
| 7 | `ai_cli_analysis/analysis/*.json` | Per-repo analysis files | done |

---

## 6. Success Definition

A user types `/Ploan "cyberpunk 2077"` in OpenCode.

The AI agent:
1. Interprets the visual direction creatively
2. Designs a unique terminal art scene
3. Generates palette, frame, ASCII/Unicode composition, and optional CSS
4. Calls Ploan's `render_scene` / `customize_environment` tools
5. The user sees a visible themed terminal visual surface directly in the OpenCode session

Optional enhancements:
- Terminal palette changes to match the scene
- Cursor/background color updates
- Grokbuild Web UI CSS hot-reload
- Separate mini TUI dashboard process

Success is **not** "theme applied" text. Success is a rendered visual object visible in the terminal.

---

## 7. Phases

| Phase | Status | Description |
|-------|--------|-------------|
| **Phase 1: CLI Analysis** | done | 9/9 repos analyzed. Top target: grok-build (10/10) |
| **Phase 2A: Documentation Alignment** | in progress | Reframe Ploan around visual surfaces |
| **Phase 2B: Scene Renderer** | next | Implement `render_scene`, gradients, boxes, swatches |
| **Phase 2C: MCP Tooling** | next | Add `render_scene` and `render_dashboard` tools |
| **Phase 2D: OpenCode UX** | next | Ensure `/Ploan` always renders a visible scene |
| **Phase 3: Web UI Bridge** | planned | Inject matching CSS into Grokbuild dashboard |

---

## 8. See Also

- [README.md](./README.md) — Quick overview and usage
- [Instructions.md](./Instructions.md) — Phase 2 implementation instructions
- [REGISTRATION.md](./REGISTRATION.md) — CLI registration guide
- [ai_cli_analysis/analysis/SUMMARY.md](./ai_cli_analysis/analysis/SUMMARY.md) — Phase 1 integration report
