# Ploan Registration Guide

How AI agents access Ploan tools in each target CLI.

---

## Core Concept

Ploan is an **MCP tool suite**.


The AI agent is the creative engine — it generates color palettes, SVG backgrounds, and
CSS. Ploan is the tool that applies the AI's work to the running terminal, TUI, and Web UI.

Every integration follows the same pattern:

```
1. Start Ploan MCP server
2. Register it in the AI CLI's config
3. AI agent discovers and calls Ploan tools
```

---

## 1. OpenCode

### Register the MCP server

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

### Custom command

Copy `opencode/ploan.md` → `~/.config/opencode/commands/ploan.md`.

Then type `/Ploan cyberpunk` in OpenCode — the AI reads the `.md` instructions,
generates the theme, and calls Ploan tools to apply it.

### Available tools

| Tool | Purpose |
|------|---------|
| `customize_environment` | Apply a full theme (colors + bg image + opacity + TUI theme) |
| `get_terminal_info` | Report terminal type and capabilities |
| `restore_environment` | Reset to pre-Ploan state |
| `list_themes` | Show built-in preset library |

---

## 2. Grok Build (xai-org/grok-build)

Grok Build has the richest theming architecture of any CLI — dedicated `Theme` struct with
60+ semantic color fields, 6 built-in themes, and lock-free hot-switching via `AtomicU8` cache.

### Via MCP server

```toml
# ~/.grok/config.toml
[tools.mcp.ploan]
command = "python3"
args = ["~/.ploan/mcp/server.py"]
type = "stdio"
```

### Via Plugin Marketplace

Ploan can be published as a plugin on `xai-org/plugin-marketplace` with:
- MCP server in PluginManifest
- Custom `Theme` implementation injected into the theme cache
- Hook registration for live theme switching

### Via Theme Hot-Swap

For full integration: implement a `Theme` struct following the pattern in
`crates/codegen/xai-grok-pager-render/src/theme/tokyonight.rs`, register via
the plugin system, and use the `AtomicU8`-based cache for lock-free hot-switching.

---

## 3. Claude Code

Claude Code is MCP-native. Register in Claude Code's MCP config:

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

## 4. open-interpreter

Via PluginManifest:

```json
{
    "name": "ploan",
    "skills": ["ploan"],
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

## 5. llm (simonw/llm)

Ploan can be published as a pip package with pluggy hooks:

```bash
pip install ploan-plugin
```

The `register_commands` pluggy hook adds Ploan as an `llm` subcommand. The `register_tools`
hook exposes Ploan tools for the AI agent to call.

---

## 6. ollama

Register Ploan tools in the ollama tool registry:

```go
registry.Register("ploan", &Tool{
    Name:        "customize_environment",
    Description: "Apply a terminal theme (colors, background, opacity)",
    Parameters:  ploanToolSchema,
    Handler:     ploanHandler,
})
```

---

## 7. aichat

YAML config with function declarations:

```yaml
functions:
  - name: customize_environment
    command: python3
    args: ["~/.ploan/src/Ploan_skill.py", "--apply"]
    env:
      PLOAN_THEME_JSON: "$THEME_JSON"
```

---

## Quick Install

```bash
./ploan.sh install
./ploan.sh --opencode
```

Then in any supported AI CLI, type `/Ploan <description>`.
