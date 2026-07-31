# CLI Background Capability Review

Date: 2026-07-30

This review tracks whether each CLI can show a persistent session/TUI background or durable visual surface for Ploan. Theme colors, MCP tools, and one-off ASCII output are useful integration surfaces, but they are not the same as a persistent background layer.

## Summary

| CLI | Native Persistent Background? | Closest Built-In Surface | Best Ploan Path |
|---|---|---|---|
| OpenCode Anomaly | No stock support; patched locally | OpenTUI render tree + theme/plugin slots | Keep `~/.ploan/opencode/background.txt` + `PloanSurface` |
| Codex CLI | No full background | Ambient `pet` image layer | Use pets for small visuals; patch ratatui render path for wallpaper |
| grok-build | No full background | Rich ratatui theme system | Patch central pager render path |
| ollama / mods | No full background | Bubble Tea views/styles | Patch view render path to draw a file-backed background |
| aichat / aider / llm / ChatGLM3 | No persistent TUI canvas | Prompt, banner, or command output | Use one-off output, prompt styling, or a wrapper TUI |

## Current Best Target

OpenCode Anomaly is the best working target because Ploan already has a source patch that renders a file-backed background behind the OpenTUI app content.

Key files:

- `patches/opencode/ploan-background.patch`
- `scripts/opencode/install_patched_opencode.sh`
- `opencode/ploan.md`
- `opencode/ploan-reset.md`

Runtime files:

- `~/.ploan/opencode/background.txt`
- `~/.local/bin/opencode-ploan`

## Codex CLI

Codex CLI is a promising target, but full Ploan wallpaper parity requires a source patch.

Findings:

- Framework: Rust `ratatui` + `crossterm` with a custom terminal/frame pipeline.
- Closest no-patch visual feature: ambient pets under `CODEX_HOME/pets/<pet-id>/pet.json`.
- Limitation: pets are anchored companion images, not full-session wallpapers.
- Theme config: `.tmTheme` syntax/UI colors only.
- Slash commands: hard-coded enum variants, not dynamically extensible.
- MCP: useful for tools/status/file updates, but not arbitrary TUI drawing.

Useful source paths in Codex:

- `codex-rs/tui/src/app.rs`
- `codex-rs/tui/src/tui.rs`
- `codex-rs/tui/src/custom_terminal.rs`
- `codex-rs/tui/src/pets/ambient.rs`
- `codex-rs/tui/src/chatwidget/pets.rs`
- `codex-rs/config/src/types.rs`

Recommended paths:

1. Low effort: generate a Codex pet asset for a small persistent visual.
2. Medium effort: patch the TUI to read `~/.ploan/codex/background.txt` and render it before the main chat widget.
3. MCP-only: expose Ploan tools and render art in chat output, but do not claim persistent background support.

## Patch Pattern

For ratatui, Bubble Tea, and similar fullscreen TUIs, the expected Ploan background pattern is:

1. Store generated background text in `~/.ploan/<cli>/background.txt`.
2. Read and cache the file inside the TUI process.
3. Render the background before the main transcript/input widgets.
4. Draw primary UI after the background or on a higher layer.
5. Provide an explicit reset command/tool that deletes the background file.

## Decision Rules

- Do not treat theme support as persistent background support.
- Do not treat MCP/plugin support as a TUI drawing API unless the host exposes an actual render slot.
- For non-fullscreen CLIs, prefer output/prompt/banner surfaces or a wrapper TUI.
- For true Ploan wallpaper behavior, prioritize CLIs with central fullscreen render loops that can be patched cleanly.
