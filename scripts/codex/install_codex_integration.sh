#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
PLOAN_HOME="$HOME/.ploan"
SKILL_DIR="$CODEX_HOME/skills/ploan"
CONFIG_FILE="$CODEX_HOME/config.toml"
PLOAN_MCP_INSTALLED="$PLOAN_HOME/mcp/server.py"
PLOAN_SRC_INSTALLED="$PLOAN_HOME/src/Ploan_skill.py"

GREEN='\033[0;32m'
BOLD='\033[1m'
RESET='\033[0m'

echo -e "${BOLD}Ploan — Codex Integration Installer${RESET}"
echo ""

mkdir -p "$PLOAN_HOME/src" "$PLOAN_HOME/mcp" "$SKILL_DIR" "$CODEX_HOME"

cp "$ROOT/src/Ploan_skill.py" "$PLOAN_SRC_INSTALLED"
cp "$ROOT/mcp/server.py" "$PLOAN_MCP_INSTALLED"
cp "$ROOT/codex/skills/ploan/SKILL.md" "$SKILL_DIR/SKILL.md"

echo -e "  ${GREEN}✓${RESET} Ploan renderer installed: $PLOAN_SRC_INSTALLED"
echo -e "  ${GREEN}✓${RESET} Ploan MCP server installed: $PLOAN_MCP_INSTALLED"
echo -e "  ${GREEN}✓${RESET} Ploan skill installed: $SKILL_DIR/SKILL.md"

if [ ! -f "$CONFIG_FILE" ]; then
  cat > "$CONFIG_FILE" <<EOF
[mcp_servers.ploan]
command = "python3"
args = ["$PLOAN_MCP_INSTALLED"]
supports_parallel_tool_calls = true
default_tools_approval_mode = "auto"
EOF
  echo -e "  ${GREEN}✓${RESET} Created $CONFIG_FILE with Ploan MCP server"
elif ! grep -q '^\[mcp_servers\.ploan\]' "$CONFIG_FILE"; then
  cat >> "$CONFIG_FILE" <<EOF

[mcp_servers.ploan]
command = "python3"
args = ["$PLOAN_MCP_INSTALLED"]
supports_parallel_tool_calls = true
default_tools_approval_mode = "auto"
EOF
  echo -e "  ${GREEN}✓${RESET} Added Ploan MCP server to $CONFIG_FILE"
else
  if grep -q "args = \[\"$PLOAN_MCP_INSTALLED\"\]" "$CONFIG_FILE"; then
    echo -e "  ${GREEN}✓${RESET} Ploan MCP server already configured in $CONFIG_FILE"
  else
    sed -i "s|args = \[\"[^\"]*mcp/server.py\"\]|args = [\"$PLOAN_MCP_INSTALLED\"]|" "$CONFIG_FILE"
    echo -e "  ${GREEN}✓${RESET} Updated Ploan MCP path in $CONFIG_FILE"
  fi
fi

if command -v codex-ploan >/dev/null 2>&1 || [ -f "$HOME/.local/bin/codex-ploan" ]; then
  echo -e "  ${GREEN}✓${RESET} Patched Codex binary found: codex-ploan (background layer active)"
else
  echo ""
  echo "  Note: For persistent TUI background, build the patched Codex binary:"
  echo "    scripts/codex/install_patched_codex.sh"
  echo "  Without it, Ploan art appears in chat output (still works great)."
fi

echo ""
echo -e "${GREEN}Done!${RESET} Restart Codex, then ask:"
echo ""
echo "  Use the ploan skill: misty mountain village, pine trees, cabin, no text"
echo ""
