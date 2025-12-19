---
name: verify
description: Cross-validate physics claims using multiple independent methods
argument-hint: <claim> [--methods=symbolic,numerical,experimental]
allowed-tools:
  - Bash
  - Read
---

# Theory2 Cross-Validation

Verify physics claims by comparing results from multiple independent methods.

## Cross-Check Command

```bash
# Verify fine-structure constant
/home/mikeb/theory2/.venv/bin/theory --json verify cross-check \
  --claim="alpha_inv=137" \
  --methods="symbolic,numerical,experimental" \
  --tolerance=0.001

# Verify molecular energy
/home/mikeb/theory2/.venv/bin/theory --json verify cross-check \
  --claim="H2_bond_length=0.74" \
  --methods="symbolic,numerical"

# Strict tolerance
/home/mikeb/theory2/.venv/bin/theory --json verify cross-check \
  --claim="pi=3.14159" \
  --methods="symbolic,numerical" \
  --tolerance=1e-6
```

## Verification Methods

### Symbolic
- Algebraic/analytic computation
- Exact results where possible
- Uses SymPy, SageMath, mpmath

### Numerical
- High-precision numerical evaluation
- Multiple precision levels (double, quad)
- GPU-accelerated where available

### Experimental
- Comparison with known experimental values
- CODATA fundamental constants
- Literature reference values

## Claim Format

Claims use `name=value` format:
- `alpha_inv=137.036` - Fine-structure constant inverse
- `H2_energy=-1.174` - H2 ground state energy (Hartree)
- `e_charge=1.602e-19` - Electron charge

## Output

The verification returns:
- Individual method results
- Agreement status
- Discrepancy analysis
- Confidence level

```json
{
  "status": "verified" | "discrepancy" | "partial",
  "results": {
    "symbolic": {...},
    "numerical": {...},
    "experimental": {...}
  },
  "agreement": {
    "all_agree": true/false,
    "max_discrepancy": 0.001,
    "within_tolerance": true/false
  }
}
```

## Use Cases

1. **Validating new calculations**: Confirm results using independent methods
2. **Checking experimental values**: Compare theory with experiment
3. **Debugging discrepancies**: Identify which method disagrees
4. **Publication preparation**: Document multi-method verification

Always use `--json` for structured output.
