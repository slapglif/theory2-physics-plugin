---
name: numerical
description: Numerical physics - quantum chemistry, quantum circuits, simulations
argument-hint: <operation> [options]
allowed-tools:
  - Bash
  - Read
---

# Theory2 Numerical Physics

Execute numerical physics computations using the Theory2 CLI.

## Quantum Chemistry

Calculate molecular energies using various methods:

```bash
# Hartree-Fock (fastest)
/home/mikeb/theory2/.venv/bin/theory --json numerical quantum-chemistry \
  --molecule="H2O" --method=hf --basis=def2-svp

# DFT with B3LYP functional
/home/mikeb/theory2/.venv/bin/theory --json numerical quantum-chemistry \
  --molecule="H2O" --method=dft --xc=b3lyp --basis=def2-svp

# CCSD (most accurate)
/home/mikeb/theory2/.venv/bin/theory --json numerical quantum-chemistry \
  --molecule="CH4" --method=ccsd --basis=cc-pVDZ
```

### Molecule Formats

**Shortcuts**: H2O, CH4, NH3, CO2, H2, N2, O2

**XYZ format**:
```
"H 0 0 0; H 0 0 0.74"
"O 0 0 0; H 0.757 0.587 0; H -0.757 0.587 0"
```

### Available Basis Sets
- sto-3g (minimal, fast)
- 6-31G (split-valence)
- cc-pVDZ (correlation consistent)
- def2-svp (balanced accuracy/speed)

## Quantum Circuits

Create and simulate quantum circuits:

```bash
# Bell state with measurements
/home/mikeb/theory2/.venv/bin/theory --json numerical quantum-circuit \
  --circuit=bell --shots=1024

# GHZ state with statevector
/home/mikeb/theory2/.venv/bin/theory --json numerical quantum-circuit \
  --circuit=ghz3 --statevector

# Check GPU availability
/home/mikeb/theory2/.venv/bin/theory --json numerical gpu-status
```

## Argument Parsing

1. **quantum-chemistry** or **qchem**: Run molecular calculation
   - --molecule: Required
   - --method: hf, dft, ccsd
   - --basis: Basis set
   - --xc: DFT functional

2. **quantum-circuit** or **circuit**: Run quantum simulation
   - --circuit: bell, ghz3, ghz4
   - --shots: Measurement count
   - --statevector: Return amplitudes

Always use `--json` for structured output.
