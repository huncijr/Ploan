#!/usr/bin/env bash
# ── Ploan — One-command install & run ───────────────────────────────
# Usage:
#   ./ploan.sh install          # Install Ploan system-wide
#   ./ploan.sh --opencode       # Setup OpenCode integration
#   ./ploan.sh --list           # Show available theme presets
#   ./ploan.sh --info           # Show terminal info
#   ./ploan.sh --restore        # Restore terminal to pre-Ploan state
#   ./ploan.sh --reset          # Clear patched OpenCode background

set -euo pipefail

BOLD="\033[1m"
GREEN="\033[32m"
CYAN="\033[36m"
RESET="\033[0m"

PLOAN_HOME="${PLOAN_HOME:-$HOME/.ploan}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

print_banner() {
    echo -e "${CYAN}"
    echo '  ╔═╗╦  ╔═╗╔═╗╔╗╔'
    echo '  ╠═╝║  ║ ║╠═╣║║║'
    echo '  ╩  ╩═╝╚═╝╩ ╩╝╚╝'
    echo -e "${RESET}"
    echo "  AI-Generated Terminal Visual Surfaces"
    echo
}

install() {
    print_banner
    echo "Installing Ploan..."

    mkdir -p "$PLOAN_HOME"/{src,mcp,opencode}
    mkdir -p "$HOME/.local/bin"

    cp "$SCRIPT_DIR/src/Ploan_skill.py" "$PLOAN_HOME/src/" 2>/dev/null || {
        echo "Run from Ploan project root: ./ploan.sh install"
        exit 1
    }
    cp "$SCRIPT_DIR/mcp/server.py" "$PLOAN_HOME/mcp/"
    cp "$SCRIPT_DIR/opencode/ploan.md" "$PLOAN_HOME/opencode/"
    cp "$SCRIPT_DIR/opencode/ploan-reset.md" "$PLOAN_HOME/opencode/"

    chmod +x "$PLOAN_HOME/src/Ploan_skill.py"
    chmod +x "$PLOAN_HOME/mcp/server.py"

    # Create wrapper
    cat > "$HOME/.local/bin/ploan" <<'WRAPPER'
#!/usr/bin/env bash
exec python3 "$HOME/.ploan/src/Ploan_skill.py" "$@"
WRAPPER
    chmod +x "$HOME/.local/bin/ploan"

    cat > "$HOME/.local/bin/ploan-reset" <<'WRAPPER'
#!/usr/bin/env bash
exec python3 "$HOME/.ploan/src/Ploan_skill.py" --reset
WRAPPER
    chmod +x "$HOME/.local/bin/ploan-reset"

    # PATH
    if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
        for rc in "$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.zprofile"; do
            touch "$rc" 2>/dev/null
            grep -q '.local/bin' "$rc" 2>/dev/null || \
                echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$rc"
        done
    fi

    # Check if we're in a real terminal (not a subprocess)
    local term_type="unknown"
    if [ -n "${KITTY_PID:-}" ]; then term_type="kitty"
    elif [ -n "${ALACRITTY_SOCKET:-}" ] || [ -n "${ALACRITTY_LOG:-}" ]; then term_type="alacritty"
    elif [ -n "${WEZTERM_PANE:-}" ]; then term_type="wezterm"
    elif [ -n "${TERM_PROGRAM:-}" ]; then term_type="$TERM_PROGRAM"
    elif command -v gsettings >/dev/null 2>&1 && gsettings list-schemas 2>/dev/null | grep -q org.gnome.Ptyxis; then
        term_type="ptyxis (Fedora default terminal)"
    elif command -v gsettings >/dev/null 2>&1; then term_type="gnome-terminal compatible (detected via gsettings)"
    fi

    echo -e "  ${GREEN}✓ Ploan installed${RESET}"
    echo
    echo -e "  Terminal detected: ${CYAN}${term_type}${RESET}"
    echo
    echo -e "  ${BOLD}In OpenCode, type:${RESET} /Ploan cyberpunk 2077 night city"
    echo -e "  ${BOLD}The AI will design a visible terminal art surface.${RESET}"
    echo
    echo -e "  Direct usage:"
    echo -e "    ploan --render-scene '<json>'  Render AI-designed terminal art"
    echo -e "    ploan --demo cyberpunk         Show a demo visual surface"
    echo -e "    ploan --apply '<json>'         Render scene + optional palette"
    echo -e "    ploan --reset                  Clear OpenCode background"
    echo -e "    ploan-reset                    Clear OpenCode background"
    echo -e "    ploan --restore           Reset terminal to defaults"
    echo -e "    ploan --list              Show built-in presets"
    echo
}

setup_opencode() {
    echo "Setting up OpenCode /Ploan command..."

    OPENCODE_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/opencode"
    mkdir -p "$OPENCODE_DIR/commands"

    cp "$SCRIPT_DIR/opencode/ploan.md" "$OPENCODE_DIR/commands/ploan.md"
    cp "$SCRIPT_DIR/opencode/ploan-reset.md" "$OPENCODE_DIR/commands/ploan-reset.md"
    mkdir -p "$PLOAN_HOME/src" && cp "$SCRIPT_DIR/src/Ploan_skill.py" "$PLOAN_HOME/src/" 2>/dev/null || true
    mkdir -p "$PLOAN_HOME/mcp" && cp "$SCRIPT_DIR/mcp/server.py" "$PLOAN_HOME/mcp/" 2>/dev/null || true

    if [ ! -f "$HOME/.opencode.json" ]; then
        cat > "$HOME/.opencode.json" <<'EOF'
{
    "mcpServers": {
        "ploan": {
            "command": "python3",
            "args": ["~/.ploan/mcp/server.py"],
            "type": "stdio"
        }
    }
}
EOF
        echo "  ✓ Created ~/.opencode.json with Ploan MCP server"
    else
        echo "  ! ~/.opencode.json exists — manually add:"
        echo '    "ploan": {"command": "python3", "args": ["~/.ploan/mcp/server.py"], "type": "stdio"}'
    fi

    echo -e "  ${GREEN}✓ OpenCode /Ploan ready${RESET}"
    echo "  In OpenCode, type: /Ploan cyberpunk 2077 night city"
    echo "  To clear the background, type: /Ploan-reset"
    echo "  The AI will generate visible terminal art and render it via Ploan."
    echo "  Restart OpenCode to reload the /Ploan command."
    echo
}

# ── Main ────────────────────────────────────────────────────────────

case "${1:-}" in
    install)
        install
        ;;
    --opencode|opencode)
        setup_opencode
        ;;
    --list|list)
        python3 "$PLOAN_HOME/src/Ploan_skill.py" --list 2>/dev/null || \
            python3 "$SCRIPT_DIR/src/Ploan_skill.py" --list 2>/dev/null || \
            { echo "Run ./ploan.sh install first"; exit 1; }
        ;;
    --info|info)
        python3 "$PLOAN_HOME/src/Ploan_skill.py" --info 2>/dev/null || \
            python3 "$SCRIPT_DIR/src/Ploan_skill.py" --info 2>/dev/null || \
            { echo "Run ./ploan.sh install first"; exit 1; }
        ;;
    --restore|restore)
        python3 "$PLOAN_HOME/src/Ploan_skill.py" --restore 2>/dev/null || \
            python3 "$SCRIPT_DIR/src/Ploan_skill.py" --restore 2>/dev/null || \
            { echo "Run ./ploan.sh install first"; exit 1; }
        ;;
    --reset|reset|--reset-background|reset-background)
        python3 "$PLOAN_HOME/src/Ploan_skill.py" --reset 2>/dev/null || \
            python3 "$SCRIPT_DIR/src/Ploan_skill.py" --reset 2>/dev/null || \
            { echo "Run ./ploan.sh install first"; exit 1; }
        ;;
    --help|help|-h)
        echo "Ploan — AI-Generated Terminal Visual Surfaces"
        echo
        echo "Usage:"
        echo "  ./ploan.sh install       Install Ploan + OpenCode integration"
        echo "  ./ploan.sh --opencode    Setup OpenCode /Ploan command only"
        echo "  ./ploan.sh --list        List built-in reference palettes"
        echo "  ./ploan.sh --info        Show detected terminal info"
        echo "  ./ploan.sh --restore     Restore terminal to pre-Ploan state"
        echo "  ./ploan.sh --reset       Clear patched OpenCode background"
        echo
        echo "AI agent usage (from OpenCode/Claude Code):"
        echo "  ploan --render-scene '<json>'  Render AI-generated terminal art"
        echo "  ploan --demo cyberpunk        Show a demo visual surface"
        echo "  ploan --apply '<json>'        Render scene + optional palette"
        echo "  ploan --reset            Clear OpenCode background"
        echo "  ploan --info             Detect terminal capabilities"
        echo "  ploan --restore          Restore after Ploan"
        ;;
    "")
        echo "Usage: ./ploan.sh [install|--opencode|--list|--info|--restore|--reset]"
        echo "Try: ./ploan.sh install"
        ;;
    *)
        python3 "$PLOAN_HOME/src/Ploan_skill.py" "$@" 2>/dev/null || \
            python3 "$SCRIPT_DIR/src/Ploan_skill.py" "$@" 2>/dev/null || {
            echo "Run ./ploan.sh install first"
            exit 1
        }
        ;;
esac
