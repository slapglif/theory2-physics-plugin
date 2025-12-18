---
name: ml
description: Physics ML - neural operators, PINNs, equivariant networks
argument-hint: <operation> [options]
allowed-tools:
  - Bash
  - Read
---

# Theory2 Physics Machine Learning

Train and use physics-informed machine learning models.

## Fourier Neural Operators (FNO)

Learn PDE solution operators:

```bash
# Standard FNO configuration
/home/mikeb/theory2/.venv/bin/theory --json ml train-fno \
  --modes=16 --width=64 --layers=4

# Memory-efficient with Tucker factorization
/home/mikeb/theory2/.venv/bin/theory --json ml train-fno \
  --modes=32 --width=128 --factorization=tucker

# Check available models
/home/mikeb/theory2/.venv/bin/theory --json ml info
```

### FNO Parameters
- **modes**: Fourier modes to keep (12-64, higher = more resolution)
- **width**: Hidden channel dimension (32-256)
- **layers**: Number of Fourier layers (2-6)
- **factorization**: dense, tucker, cp (tucker reduces memory 10x)

## E(3)-Equivariant Networks (E3NN)

For molecular and atomic systems with geometric symmetry:

```bash
# Standard E3NN
/home/mikeb/theory2/.venv/bin/theory --json ml train-e3nn \
  --irreps-hidden="16x0e+16x1o+16x2e" --layers=3

# With gated nonlinearities
/home/mikeb/theory2/.venv/bin/theory --json ml train-e3nn \
  --irreps-hidden="32x0e+16x1o+8x2e" --use-gates
```

### Irreps Format
`NxLp` where:
- N: Multiplicity
- L: Angular momentum (0=scalar, 1=vector, 2=tensor)
- p: Parity (e=even, o=odd)

Example: `16x0e + 16x1o + 8x2e` = 16 scalars + 16 vectors + 8 symmetric tensors

## Physics-Informed Neural Networks (PINNs)

Solve PDEs without training data:

```bash
# Heat equation
/home/mikeb/theory2/.venv/bin/theory --json ml solve-pde \
  --pde-type=heat --alpha=0.01 --iterations=10000

# Poisson equation
/home/mikeb/theory2/.venv/bin/theory --json ml solve-pde \
  --pde-type=poisson --iterations=20000
```

### Available PDEs
- **heat**: 1D heat diffusion ∂u/∂t = α∂²u/∂x²
- **poisson**: 2D Poisson ∇²u = f

## Argument Parsing

1. **train-fno** or **fno**: Train Fourier Neural Operator
2. **train-e3nn** or **e3nn**: Train equivariant network
3. **solve-pde** or **pinn**: Solve PDE with PINN
4. **info**: Show available models and status

Always use `--json` for structured output.
