# Instructions: Phase 2 — Ploan Terminal Visual Surface Implementation

Build **Ploan** — an MCP tool suite that lets AI coding agents generate and render beautiful terminal-native visual surfaces.

---

## 0. Quick Reference Card

| Key | Value |
|-----|-------|
| **Goal** | Build `render_scene`, `render_dashboard`, and OpenCode visible terminal art flow |
| **Core concept** | AI generates the art; Ploan renders it visibly in terminal / AI CLI output |
| **Primary target** | OpenCode custom command + MCP server |
| **Phase 1 Status** | complete — 9/9 repos analyzed |
| **Output** | `src/Ploan_skill.py`, `mcp/server.py`, `opencode/ploan.md`, docs |

---

## 1. What Ploan Is

Ploan is:
- An MCP tool suite for AI agents
- A terminal art renderer
- A scene/dashboard/prompt banner renderer
- A helper for optional terminal color palette changes
- A future bridge for Web UI overlays

Ploan is not:
- A desktop wallpaper setter
- Merely a terminal color setter
- A standalone natural-language-to-theme generator
- A replacement for the AI's creativity

The successful flow:

```text
User: /Ploan "cyberpunk 2077 night city"
  → AI designs a unique visual terminal scene
  → AI calls render_scene / customize_environment
  → Ploan renders visible ASCII/ANSI/Unicode art
  → User sees the themed surface in OpenCode
```

---

## 2. Visual Surface Requirements

Ploan should support these output types:

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

The renderer must always have a plain-text fallback if ANSI escape sequences are stripped by the host CLI.

---

## 3. Phase 1 Analysis (READ-ONLY)

Read analysis files before making integration decisions:

| File | Content |
|------|---------|
| `ai_cli_analysis/analysis/SUMMARY.md` | Ranked integration report |
| `ai_cli_analysis/analysis/opencode.json` | OpenCode command + MCP architecture |
| `ai_cli_analysis/analysis/grok-build.json` | Grok Build TUI/theme architecture |

OpenCode facts:
- `.md` commands are prompt templates sent to the AI
- OpenCode has no dynamic plugin system
- MCP stdout is captured as tool output
- OpenCode has no native background-image layer
- Therefore the first working UX is a **chat/output visual surface**, not a hidden TUI background layer

---

## 4. Implementation Plan

### Step 1: Scene Renderer (`src/Ploan_skill.py`)

Add:
- `render_scene(scene: dict) -> str`
- `render_dashboard(layout: dict) -> str`
- `strip_ansi(text: str) -> str`
- `gradient_text(text, colors) -> str`
- `render_swatches(palette) -> str`
- CLI mode: `ploan --render-scene '<json>'`
- CLI mode: `ploan --demo cyberpunk`

Scene JSON shape:

```json
{
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
    "╔════════════════════════════════╗",
    "║  PLOAN // NIGHT CITY MODE      ║",
    "╚════════════════════════════════╝"
  ]
}
```

### Step 2: MCP Tools (`mcp/server.py`)

Add or update tools:

| Tool | Required |
|------|----------|
| `render_scene` | yes |
| `render_dashboard` | yes |
| `customize_environment` | yes, should accept `scene` + optional palette |
| `get_terminal_info` | yes |
| `restore_environment` | optional palette restore |

### Step 3: OpenCode Command (`opencode/ploan.md`)

Must instruct the AI:
- Always render a visible terminal surface
- Never only say "theme applied"
- Generate unique art for the user's description
- Use `render_scene` or direct visible output
- Include a short description after the visual

### Step 4: Testing

Test in OpenCode:

```text
/Ploan cyberpunk 2077 night city
/Ploan ocean depths with bioluminescent vibes
/Ploan spacecraft cockpit orbiting saturn
```

Expected behavior:
- A visible Unicode/ASCII/ANSI scene appears in chat/output
- Palette summary follows
- Optional terminal palette may change
- No stale preset-only fallback

---

## 5. Success Criteria

- [ ] `render_scene` returns a visible terminal art block
- [ ] ANSI mode works in normal terminal
- [ ] Plain Unicode fallback works in OpenCode if ANSI is stripped
- [ ] OpenCode `/Ploan` produces visible art, not only an "applied" message
- [ ] AI is instructed to generate unique scenes, not use static presets
- [ ] `customize_environment` can compose scene + palette + optional Web UI CSS

---

## 6. See Also

- [About_Project.md](./About_Project.md) — Full architecture and visual surface concept
- [README.md](./README.md) — Quick overview
- [REGISTRATION.md](./REGISTRATION.md) — CLI registration guide
- [ai_cli_analysis/analysis/SUMMARY.md](./ai_cli_analysis/analysis/SUMMARY.md) — Integration report
