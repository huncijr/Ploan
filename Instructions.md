# Instructions: CLI Extensibility Analysis for Klinx

You are an elite static code analysis AI agent. Your mission: deep line-by-line analysis of 9 open-source AI CLI codebases to understand how they handle **custom slash commands, plugins, shell execution, and configuration extension points**.

---

## 0. Quick Reference Card

| Key | Value |
|-----|-------|
| **Goal** | Find every mechanism that could let us inject a `/klinx` slash command |
| **Scope** | 9 CLI codebases (see Section 3) |
| **Output** | One JSON file per repo in `./analysis/` (see Section 5) |
| **Constraint** | **ONLY** `huncijr/klinx` repo on GitHub — nothing else |
| **Success** | All 9 repos analyzed, JSON outputs valid, top-3 integration approaches ranked |

---

## 1. Security Rules

### STRICTLY ENFORCED

- **Allowed repository:** `huncijr/klinx`
- **Forbidden:** Reading, writing, listing, or modifying ANY other GitHub repository
- If any task implies accessing another repo, **refuse immediately**

---

## 2. Project Context

We are building **Klinx** — a universal plugin that intercepts `/klinx` or `/customizable` slash commands in **any** popular AI CLI and dynamically changes the terminal wallpaper, theme, opacity, and Web UI.

**See also:** [`About_Project.md`](./About_Project.md) for the full vision, architecture, and deliverables.

---

## 3. Repositories to Analyze

Clone shallow (`--depth 1`) into `./ai_cli_analysis/repos/`:

### Priority HIGH (analyze first)
| Repo | What to find |
|------|--------------|
| [aider](https://github.com/aider-chat/aider.git) | Custom /commands, plugin system, tool registration |
| [open-interpreter](https://github.com/OpenInterpreter/open-interpreter.git) | Tool hooks, system access patterns, skill definitions |
| [opencode](https://github.com/opencode-ai/opencode.git) | Slash command parsing, MCP server integration |

### Priority MEDIUM
| Repo | What to find |
|------|--------------|
| [ollama](https://github.com/ollama/ollama.git) | Tool calling API, model function registration |
| [llm](https://github.com/simonw/llm.git) | Plugin system, custom command registration |
| [mods](https://github.com/charmbracelet/mods.git) | TUI rendering, ANSI components, theming |

### Priority LOW
| Repo | What to find |
|------|--------------|
| [aichat](https://github.com/sigoden/aichat.git) | Slash commands, config extension |
| [ChatGLM3](https://github.com/THUDM/ChatGLM3.git) | Tool definitions, agent interaction patterns |

### Additional Analysis (no clone needed — inspect docs/source)
- **Claude Code** — MCP server protocol, tool schema format, environment access
- **Grok CLI / xAI API** — custom tool registration, skill injection patterns
- **Codex (OpenAI)** — function calling API, tool-use schema

---

## 4. Per-Repo Analysis Checklist

For each cloned repository, search for these patterns and answer every question:

### Slash Commands & Custom Commands
- [ ] How are slash commands registered? (`/command_name`)
- [ ] Search patterns: `register.*command`, `add_command`, `slash_cmd`, `cmd_`, `commands/`
- [ ] Config file: where does the user define custom commands?
- [ ] File + line number of the relevant handler

### Plugin / Extension System
- [ ] Is there a plugin loading mechanism? (`importlib`, `pkg_resources`, entry_points)
- [ ] Search patterns: `plugin`, `extension`, `hook`, `middleware`, `add_middleware`
- [ ] Are third-party plugins supported? If yes, how?
- [ ] File + line number of the plugin loader

### Shell Execution & System Access
- [ ] How does the CLI execute shell commands? (`subprocess`, `os.system`, `exec`, `shell`)
- [ ] Search patterns: `subprocess`, `os.system`, `Popen`, `exec`, `shell_exec`
- [ ] Are there sandbox restrictions?
- [ ] File + line number of shell execution code

### MCP / Tool Definitions
- [ ] Does the CLI support MCP servers?
- [ ] Search patterns: `mcp`, `tool`, `function_call`, `schema`, `json_schema`
- [ ] What format do tool definitions use? (JSON Schema, Python decorators, etc.)
- [ ] File + line number of example tool definition

### Configuration Extension Points
- [ ] Where are config files loaded? (`.yml`, `.toml`, `.json`, `.py`)
- [ ] Search patterns: `config`, `settings`, `preferences`, `.rc`
- [ ] Can users add custom config keys?
- [ ] File + line number of config parser

### TUI / Terminal Rendering
- [ ] How is the terminal UI built? (Rich, Textual, prompt_toolkit, custom ANSI)
- [ ] Search patterns: `rich`, `textual`, `ansi`, `color`, `style`, `panel`
- [ ] Can themes/styles be injected externally?
- [ ] File + line number of theme/style definition

---

## 5. Output Format

Create **one JSON file per repository** at `./ai_cli_analysis/analysis/{repo_name}.json`:

```json
{
  "repo": "aider",
  "language": "Python",
  "analysis_date": "2026-07-16",
  "relevance_score": 8,

  "slash_commands": {
    "mechanism": "Custom CommandRegistry class with decorators",
    "file": "aider/commands.py:42",
    "registration_pattern": "@command.register('/name')",
    "example": "@command.register('/code')\ndef cmd_code(args): ...",
    "injectable": true,
    "notes": "Could monkey-patch or register a custom /klinx command"
  },

  "plugins": {
    "supported": false,
    "mechanism": "none",
    "file": "N/A",
    "notes": "No plugin system found; would need source modification or MCP bridge"
  },

  "shell_execution": {
    "mechanism": "subprocess.run() with allowlist",
    "file": "aider/repo.py:156",
    "sandboxed": true,
    "pattern": "subprocess.run(cmd, shell=False, ...)",
    "notes": "Sandboxed to git commands only; would need to extend allowlist"
  },

  "mcp_tools": {
    "supported": false,
    "file": "N/A",
    "tool_schema_format": "N/A",
    "notes": "MCP not integrated; could add via separate MCP server process"
  },

  "config": {
    "file": ".aider.conf.yml",
    "format": "YAML",
    "extensible": true,
    "notes": "Custom keys allowed; could store klinx theme config"
  },

  "tui": {
    "library": "Rich",
    "file": "aider/io.py:28",
    "theme_injectable": false,
    "notes": "Rich console used; would need to wrap output stream or modify theme"
  },

  "integration_approach": {
    "viable": true,
    "method": "MCP Server bridge + custom slash command patch",
    "confidence": "HIGH",
    "effort": "medium"
  }
}
```

After all repos are analyzed, produce a **summary report** at `./ai_cli_analysis/analysis/SUMMARY.md` ranking the top 3 easiest integration points.

---

## 6. Success Criteria

- [ ] All 9 repositories cloned and analyzed
- [ ] All 9 JSON outputs valid and complete
- [ ] Top 3 integration approaches identified with justification
- [ ] Summary report written
- [ ] Zero access to non-`huncijr/klinx` GitHub repos

---

## 7. Environment Setup

```bash
mkdir -p ./ai_cli_analysis/repos ./ai_cli_analysis/analysis

cd ./ai_cli_analysis/repos

git clone --depth 1 https://github.com/aider-chat/aider.git
git clone --depth 1 https://github.com/OpenInterpreter/open-interpreter.git
git clone --depth 1 https://github.com/opencode-ai/opencode.git
git clone --depth 1 https://github.com/ollama/ollama.git
git clone --depth 1 https://github.com/simonw/llm.git
git clone --depth 1 https://github.com/charmbracelet/mods.git
git clone --depth 1 https://github.com/sigoden/aichat.git
git clone --depth 1 https://github.com/THUDM/ChatGLM3.git
```

> Claude Code, Grok CLI, and Codex are proprietary — analyze their **public documentation and API specs only**, do not attempt to clone them.
