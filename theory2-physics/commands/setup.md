---
name: setup
description: Configure Theory2 dependencies (Lean 4, mathlib4, Python environment)
argument-hint: [--lean] [--python] [--all]
allowed-tools:
  - Bash
  - Read
---

# Theory2 Setup

Configure and verify Theory2 dependencies.

## Lean 4 Setup

Run the Lean setup script to ensure Lean 4 is properly installed:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/setup-lean.sh
```

This will:
1. Install elan (Lean version manager) if not present
2. Set the correct Lean 4 toolchain version (v4.3.0-rc2)
3. Check LeanDojo cache status
4. Run verification test

## LeanDojo Tracing (First-Time Setup)

LeanDojo requires tracing mathlib4 before theorem proving works. This is a one-time operation that takes ~1 hour and requires 32GB+ RAM.

To trace mathlib4:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/trace-mathlib4.sh
```

Or trace using Python directly:

```python
from lean_dojo import LeanGitRepo, trace
repo = LeanGitRepo("https://github.com/leanprover-community/mathlib4", "v4.3.0-rc2")
trace(repo)
```

## Python Environment

The Theory2 CLI requires a Python virtual environment at `/home/mikeb/theory2/.venv`.

To verify the Python setup:

```bash
/home/mikeb/theory2/.venv/bin/python --version
/home/mikeb/theory2/.venv/bin/theory --help
```

## Full Setup

To run all setup tasks:

```bash
# Lean setup
bash ${CLAUDE_PLUGIN_ROOT}/scripts/setup-lean.sh

# Verify Theory2 CLI
/home/mikeb/theory2/.venv/bin/theory --json symbolic compute-e7-alpha

# Check all modules
/home/mikeb/theory2/.venv/bin/theory --json ml info

# Test theorem proving (will trace mathlib4 if not cached)
/home/mikeb/theory2/.venv/bin/theory --json prove lean --statement="2 + 2 = 4" --tactic=norm_num
```

## Troubleshooting

### Lean not found
```bash
source ~/.elan/env
lean --version
```

### Python packages missing
```bash
cd /home/mikeb/theory2
uv sync
```

### GPU not detected
```bash
/home/mikeb/theory2/.venv/bin/theory --json numerical gpu-status
```

### LeanDojo tracing fails
```bash
# Check available memory
free -h

# Tracing requires ~32GB RAM
# If you have less, try with fewer processes:
export NUM_PROCS=4
bash ${CLAUDE_PLUGIN_ROOT}/scripts/trace-mathlib4.sh
```
