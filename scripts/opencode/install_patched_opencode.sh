#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SRC_DIR="${OPENCODE_SOURCE:-$ROOT/ai_cli_analysis/repos/opencode-anomaly}"
OPENCODE_REPO="${OPENCODE_REPO:-https://github.com/anomalyco/opencode.git}"
OPENCODE_REF="${OPENCODE_REF:-v1.18.9}"
PATCH_FILE="$ROOT/patches/opencode/ploan-background.patch"
OUT="${PLOAN_OPENCODE_BIN:-$HOME/.local/bin/opencode-ploan}"

if [ ! -d "$SRC_DIR/.git" ]; then
  mkdir -p "$(dirname "$SRC_DIR")"
  git clone --depth 1 --branch "$OPENCODE_REF" "$OPENCODE_REPO" "$SRC_DIR"
fi

mkdir -p "$(dirname "$OUT")"

cd "$SRC_DIR"

if ! grep -q 'PloanSurface' packages/tui/src/app.tsx 2>/dev/null; then
  git apply "$PATCH_FILE"
fi

if ! command -v bun >/dev/null 2>&1; then
  echo "bun is required to build the current OpenCode CLI." >&2
  exit 1
fi

if ! command -v node-gyp >/dev/null 2>&1; then
  npm install --prefix /tmp/opencode node-gyp
  export PATH="/tmp/opencode/node_modules/.bin:$PATH"
fi

bun install --frozen-lockfile
bun run --cwd packages/tui typecheck
bun run --cwd packages/opencode script/build.ts --single --skip-install --skip-embed-web-ui

cp packages/opencode/dist/opencode-linux-x64/bin/opencode "$OUT.new"
chmod +x "$OUT.new"
mv -f "$OUT.new" "$OUT"

echo "Built patched OpenCode: $OUT"
echo "Run it with: opencode-ploan --pure"
echo "Ploan scenes are read from: ~/.ploan/opencode/background.txt"
