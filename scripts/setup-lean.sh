#!/bin/bash
# Theory2 Plugin - Lean 4 + LeanDojo Setup
# This script installs Lean 4 and pre-traces mathlib4 for LeanDojo
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LEAN_TOOLCHAIN="leanprover/lean4:v4.3.0-rc2"
# Use commit that's pre-traced in LeanDojo's remote cache (downloads ~2.4GB vs hours of tracing)
MATHLIB_COMMIT="29dcec074de168ac2bf835a77ef68bbe069194c5"
LEAN_DOJO_CACHE="${LEAN_DOJO_CACHE_DIR:-$HOME/.cache/lean_dojo}"

echo "=== Theory2 Lean 4 + LeanDojo Setup ==="
echo "Cache directory: $LEAN_DOJO_CACHE"

# Install elan if missing
if ! command -v elan &> /dev/null; then
    echo "[1/5] Installing elan (Lean version manager)..."
    curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh -s -- -y --default-toolchain ${LEAN_TOOLCHAIN}
    export PATH="$HOME/.elan/bin:$PATH"
else
    echo "[1/5] elan already installed"
fi

# Ensure toolchain installed
echo "[2/5] Installing Lean toolchain: ${LEAN_TOOLCHAIN}..."
elan toolchain install ${LEAN_TOOLCHAIN} 2>/dev/null || true
elan default ${LEAN_TOOLCHAIN} 2>/dev/null || true

# Verify Lean
echo "[3/5] Verifying Lean installation..."
lean --version

# Check if lean-dojo is installed
echo "[4/5] Checking lean-dojo Python package..."
if python3 -c "import lean_dojo" 2>/dev/null; then
    echo "lean-dojo is installed"
else
    echo "lean-dojo not found in current Python environment"
    echo "Install with: pip install lean-dojo"
fi

# Check if mathlib4 is already traced
echo "[5/5] Checking LeanDojo cache for mathlib4..."
CACHE_DIR_NAME="leanprover-community-mathlib4"

CACHED_PATH=$(ls -d "$LEAN_DOJO_CACHE"/${CACHE_DIR_NAME}* 2>/dev/null | head -1)
if [ -n "$CACHED_PATH" ] && [ -d "$CACHED_PATH" ]; then
    echo "mathlib4 appears to be cached at: $CACHED_PATH"
else
    echo ""
    echo "================================================================"
    echo "IMPORTANT: mathlib4 has not been traced yet."
    echo ""
    echo "First-time tracing takes ~1 hour and requires 32GB+ RAM."
    echo "Run the following to trace mathlib4:"
    echo ""
    echo "  python3 -c \""
    echo "from lean_dojo import LeanGitRepo, trace"
    echo "repo = LeanGitRepo('https://github.com/leanprover-community/mathlib4', '${MATHLIB_COMMIT}')"
    echo "trace(repo)"
    echo "\""
    echo ""
    echo "Or run: theory prove lean --statement='2+2=4' --tactic=norm_num"
    echo "to trigger tracing automatically."
    echo "================================================================"
fi

echo ""
echo "Setup complete!"
