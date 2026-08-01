<img src="Images/ploan-logo.png" width="90" align="left" alt="Ploan logo">

# Ploan — Make Your Terminal Beautiful With One Prompt

> One prompt. One terminal visual. No theme files, no plugins.

Ploan is an **MCP tool suite and renderer** for prompt-made terminal visuals.
It turns a short prompt into terminal-native visual backgrounds: ASCII scenes,
ANSI gradients, Unicode dashboards, themed banners, and optional Web UI overlays.

The point is not just to change colors. The point is to make your terminal feel
alive with one command.

---

## Getting Started

### Prerequisites

- **git**
- **python3** (3.8+)
- A supported AI coding CLI: [OpenCode](https://github.com/anomalyco/opencode) or [Codex](https://github.com/openai/codex)

### 1. Download Ploan

```bash
git clone https://github.com/huncijr/Ploan.git
cd Ploan
```

That's it. No package manager, no registry. The repo is the whole tool.

### 2. Install

```bash
./ploan.sh install
```

This copies the renderer and MCP server to `~/.ploan/`, creates `ploan` and
`ploan-reset` wrappers in `~/.local/bin/`, and adds them to your PATH.

### 3. Connect your CLI

**OpenCode:**

```bash
./ploan.sh --opencode
```

Installs the `/Ploan` and `/Ploan-reset` slash commands and registers the Ploan
MCP server in `~/.opencode.json`. Restart OpenCode after this.

**Codex:**

```bash
./ploan.sh --codex
```

Installs the Ploan skill into `~/.codex/skills/ploan/` and registers the MCP
server in `~/.codex/config.toml`. Restart Codex after this.

### 4. Generate a background

In OpenCode:

```text
/Ploan cyberpunk 2077 night city
/Ploan ocean depths with bioluminescent vibes
/Ploan spaceship dashboard orbiting saturn
```

In Codex:

```text
Use the ploan skill: misty mountain village, pine trees, lake reflection, no text
```

### 5. Reset

```text
/Ploan-reset
```

Or from any terminal:

```bash
ploan --reset
```

---

## What Ploan Does

```
User: /Ploan "create a saturn at the middle of the background"
   │
   ▼
Your coding assistant designs a terminal-safe scene
   │
   ▼
Ploan receives structured art: render_scene({scene, palette, lines, layout})
   │
   ▼
Ploan renders the visual surface in your terminal
```

And this is what that one prompt produces — a ringed Saturn drawn from a single sentence:

```text
              _.oo.
          _.u[[/;:,.         .odMMMMMM'
       .o888UU[[[/;:-.   .o@P^    MMM^
      oN88888UU[[[/;::-.       dP^
     dNMMNN888UU[[[/;:--.  .o@P^
    ,MMMMMMN888UU[[/;::-.o@^
    NNMMMNN888UU[[[/~.o@P^
    888888888UU[[[/o@^-..
   oI8888UU[[[/o@P^:--..
.@^  YUU[[[/o@^;::---..
oMP     ^/o@P^;:::---..
.dMMM    .o@^  ^;::---...
dMMMMMMM@^`       `^^^^
YMMMUP^
^^
```

`/Ploan create a saturn at the middle of the background`

---

## Persistent TUI Background Layer (Optional)

By default, Ploan renders scenes into chat/output. For a **persistent background
layer behind the TUI itself**, build the patched OpenCode binary:

```bash
scripts/opencode/install_patched_opencode.sh
opencode-ploan --pure
```

Requires: `bun`, `node-gyp`, and the OpenCode source (auto-cloned on first run).

Then generate or replace the background from the OpenCode chatbox:

```text
/Ploan misty mountain village, pine trees, clouds, lake reflection, no text
```

Ploan reads the scene from `~/.ploan/opencode/background.txt` and paints it as a
full-width background behind the TUI.

For Codex, build the patched binary (requires Rust/cargo):

```bash
scripts/codex/install_patched_codex.sh
```

This produces `~/.local/bin/codex-ploan` which reads
`~/.ploan/codex/background.txt`.
