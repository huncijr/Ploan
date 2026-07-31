#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CODEX_REPO="$ROOT/ai_cli_analysis/repos/codex"
PATCH_FILE="$ROOT/patches/codex/ploan-background.patch"
OUT="${PLOAN_CODEX_OUT:-$HOME/.local/bin/codex-ploan}"

if [ ! -d "$CODEX_REPO/codex-rs" ]; then
  echo "Error: Codex repo not found at $CODEX_REPO" >&2
  echo "Clone it first: git clone https://github.com/openai/codex.git $CODEX_REPO" >&2
  exit 1
fi

if [ ! -f "$PATCH_FILE" ]; then
  echo "Error: Patch file not found at $PATCH_FILE" >&2
  exit 1
fi

echo "Applying Ploan background patch to Codex TUI..."

cd "$CODEX_REPO"

if grep -q 'ploan_background' codex-rs/tui/src/app.rs 2>/dev/null; then
  echo "Patch already applied, skipping."
else
  git apply --check "$PATCH_FILE" 2>/dev/null && git apply "$PATCH_FILE" || {
    echo "Warning: git apply failed, trying patch -p1..." >&2
    patch -p1 < "$PATCH_FILE"
  }
  echo "Patch applied."
fi

if ! command -v cargo >/dev/null 2>&1; then
  echo "Error: cargo not found. Install Rust first:" >&2
  echo "  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh" >&2
  echo "  source ~/.cargo/env" >&2
  exit 1
fi

echo "Building patched Codex TUI (this may take several minutes)..."
cd "$CODEX_REPO/codex-rs"
cargo build --release -p codex-tui --bin codex-tui 2>&1 | tail -5

BUILT="$CODEX_REPO/codex-rs/target/release/codex-tui"
if [ ! -f "$BUILT" ]; then
  echo "Error: Build did not produce $BUILT" >&2
  exit 1
fi

mkdir -p "$(dirname "$OUT")"
cp "$BUILT" "$OUT"
chmod +x "$OUT"

echo ""
echo "Built patched Codex: $OUT"
echo "Ploan scenes are read from: ~/.ploan/codex/background.txt"
echo ""
echo "Usage:"
echo "  $OUT"
echo ""
echo "Then in Codex, ask:"
echo "  Use the ploan skill: misty mountain village, pine trees, cabin, no text"
