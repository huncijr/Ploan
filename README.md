<img src="Images/ploan-logo.png" width="90" align="left" alt="Ploan logo">

# Ploan — Make Your Terminal Beautiful With One Prompt

> One prompt. One terminal visual. No theme files, no plugins.

Ploan is an **MCP tool suite and renderer** for prompt-made terminal visuals.
It turns a short prompt into terminal-native visual backgrounds: ASCII scenes,
ANSI gradients, Unicode dashboards, themed banners, and optional Web UI overlays.

The point is not just to change colors. The point is to make your terminal feel
alive with one command.

---

## What Ploan Does

```
User: /Ploan "ocean depths with bioluminescent vibes"
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

And this is what one prompt produces — a ringed Saturn drawn from a single sentence:

```text
                                                  --------
                                          -----_____________-----
                                      ----__===================___---
                                   ---__====___             ___====__--
                                 --__===__       #oooo          __===__--
                               --__==__        ###oooo~~           _===__--
                              --_==__         ###oooo~~~:            _==__--
                            --_===_          ###@oooo~~~::            _==__--
                           --_===_           ##@oooo~~~:::             _==_--
                           -_===_           ###@oooo~~~:::,            _==__-
                          --_==_            ##@oooo~~~:::,,            _===_-
                          -__==_            ##@oooo~~~:::,,            _==__-
                          -_===_            ##oooo~~~:::,,,            _==_--
                          -__==_            ##ooo~~~~:::,,,           _===_-
                          --_==_             oooo~~~:::,,,           _===_--
                          --__==_            ooo~~~~:::,,,          _===_--
                           --__==_            oo~~~:::,,,         __==_--
                            --__===_           ~~~~:::,,        __==__--
                              --__===__          ~:::,       __===__--
                                --__====___             ___====__---
                                  ---___===================__----
                                      -----_____________-----
                                             --------
```

`/Ploan create a saturn at the middle of the background`

---

## Try It In OpenCode

Ploan ships as an OpenCode custom command plus an MCP server. The AI reads your
prompt, designs an image-like ASCII/Unicode scene, and renders it straight into
your terminal — no plugins, no theme files.

### 1. Install

```bash
./ploan.sh install
./ploan.sh --opencode
```

This installs the `/Ploan` and `/Ploan-reset` commands into OpenCode, copies the
MCP server to `~/.ploan/`, and configures `~/.opencode.json` automatically.

### 2. Restart OpenCode

The `/Ploan` command and the Ploan MCP server load on OpenCode startup.

### 3. Generate a background

Type in the OpenCode chatbox:

```text
/Ploan cyberpunk 2077 night city
/Ploan ocean depths with bioluminescent vibes
/Ploan spaceship dashboard orbiting saturn
```

The expected result is a visible themed terminal surface — not just "theme
applied" text. OpenCode shows the rendered art directly in the conversation.

### 4. Persistent TUI background layer (optional)

To paint the scene as an OpenCode TUI background layer behind the UI, use the
patched build:

```bash
scripts/opencode/install_patched_opencode.sh
opencode-ploan --pure
```

Then generate or replace the background from the OpenCode chatbox:

```text
/Ploan misty mountain village, pine trees, clouds, lake reflection, no text
```

### 5. Reset

Clear the current background:

```text
/Ploan-reset
```

Or from a terminal:

```bash
ploan --reset
# or
ploan-reset
```

Ploan writes the current OpenCode surface to:

```text
~/.ploan/opencode/background.txt
```
