#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SRC_DIR="${OPENCODE_SOURCE:-$ROOT/ai_cli_analysis/repos/opencode}"
PATCH_FILE="$ROOT/patches/opencode/ploan-background.patch"
OUT="${PLOAN_OPENCODE_BIN:-$HOME/.local/bin/opencode-ploan}"

if [ ! -d "$SRC_DIR/.git" ]; then
  echo "OpenCode source not found: $SRC_DIR" >&2
  echo "Set OPENCODE_SOURCE=/path/to/opencode or clone OpenCode into ai_cli_analysis/repos/opencode." >&2
  exit 1
fi

mkdir -p "$(dirname "$OUT")"

cd "$SRC_DIR"

if ! grep -q 'internal/tui/ploanbg' internal/tui/tui.go 2>/dev/null; then
  git apply "$PATCH_FILE"
fi

gofmt -w internal/tui/tui.go internal/tui/ploanbg/background.go
go build -o "$OUT" .

echo "Built patched OpenCode: $OUT"
echo "Run it with: opencode-ploan"
echo "Ploan scenes are read from: ~/.ploan/opencode/background.txt"
