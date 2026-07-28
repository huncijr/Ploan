#!/usr/bin/env bash
# ── Ploan macOS Theme Installer ─────────────────────────────────────
set -euo pipefail

PLOAN_HOME="${PLOAN_HOME:-$HOME/.ploan}"
PLOAN_SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

info()  { echo "  → $*"; }
ok()    { echo "  ✓ $*"; }

install_ploan() {
    info "Installing Ploan to ${PLOAN_HOME}..."
    mkdir -p "$PLOAN_HOME"
    cp -r "$PLOAN_SRC/src" "$PLOAN_HOME/src"
    cp -r "$PLOAN_SRC/mcp" "$PLOAN_HOME/mcp"

    chmod +x "$PLOAN_HOME/src/Ploan_skill.py"
    chmod +x "$PLOAN_HOME/mcp/server.py"

    # Brew dependencies
    if command -v brew >/dev/null 2>&1; then
        brew install imagemagick librsvg 2>/dev/null || true
    fi

    # iTerm2 dynamic profile
    ITERM_DIR="$HOME/Library/Application Support/iTerm2/DynamicProfiles"
    mkdir -p "$ITERM_DIR"

    ok "Ploan installed"
}

setup_opencode() {
    info "Setting up OpenCode..."
    OPENCODE_DIR="$HOME/.config/opencode"
    mkdir -p "$OPENCODE_DIR/commands"

    cat > "$OPENCODE_DIR/commands/ploan.md" <<'EOF'
# Ploan — Dynamic Terminal Theming

When invoked, run the Ploan theme engine:
1. Run: `python3 ~/.ploan/src/Ploan_skill.py "$THEME_DESCRIPTION"`
2. Report the result — theme name, terminal, wallpaper status.
EOF

    if [ ! -f "$HOME/.opencode.json" ]; then
        cat > "$HOME/.opencode.json" <<'EOF'
{"mcpServers":{"ploan":{"command":"python3","args":["~/.ploan/mcp/server.py"],"type":"stdio"}}}
EOF
    fi

    ok "OpenCode ready"
}

main() {
    install_ploan
    setup_opencode
    echo "Done! Run: python3 ~/.ploan/src/Ploan_skill.py cyberpunk"
}

main "$@"
