#!/bin/bash
# Theory2 Plugin - Lean 4 Setup
set -e

LEAN_TOOLCHAIN="leanprover/lean4:v4.26.0"

# Install elan if missing
if ! command -v elan &> /dev/null; then
    curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh -s -- -y --default-toolchain ${LEAN_TOOLCHAIN}
    export PATH="$HOME/.elan/bin:$PATH"
fi

# Ensure toolchain installed
elan toolchain install ${LEAN_TOOLCHAIN} 2>/dev/null || true
elan default ${LEAN_TOOLCHAIN} 2>/dev/null || true

# Verify
lean --version
