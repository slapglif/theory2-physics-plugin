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
2. Set the correct Lean 4 toolchain version
3. Create mathlib4 theorem cache directory
4. Run a verification test

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
