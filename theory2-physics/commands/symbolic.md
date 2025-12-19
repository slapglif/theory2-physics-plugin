---
name: symbolic
description: Perform symbolic mathematics - Lie algebras, calculus, equation solving
argument-hint: <operation> [options]
allowed-tools:
  - Bash
  - Read
---

# Theory2 Symbolic Mathematics

Execute symbolic math operations using the Theory2 CLI.

## Available Operations

### Lie Algebra Computations
```bash
# Compute fine-structure constant from E7
/home/mikeb/theory2/.venv/bin/theory --json symbolic compute-e7-alpha --verify

# Query Lie algebra properties
/home/mikeb/theory2/.venv/bin/theory --json symbolic lie-algebra --type=E7 --query=dimension
/home/mikeb/theory2/.venv/bin/theory --json symbolic lie-algebra --type=E8 --query=fundamental_rep
```

### Expression Evaluation
```bash
# Evaluate with substitutions
/home/mikeb/theory2/.venv/bin/theory --json symbolic eval --expr="(x+1)**2" --substitutions='{"x": 3}'

# Simplify expressions
/home/mikeb/theory2/.venv/bin/theory --json symbolic simplify --expr="(x**2-1)/(x-1)"

# Expand expressions
/home/mikeb/theory2/.venv/bin/theory --json symbolic expand --expr="(a+b)**3"

# Factor expressions
/home/mikeb/theory2/.venv/bin/theory --json symbolic factor --expr="x**3 - 1"
```

### Equation Solving
```bash
# Solve algebraic equations
/home/mikeb/theory2/.venv/bin/theory --json symbolic solve --expr="x**2 - 4" --symbol=x
```

### Calculus
```bash
# Differentiate
/home/mikeb/theory2/.venv/bin/theory --json symbolic diff --expr="x**3 * sin(x)" --symbol=x

# Integrate
/home/mikeb/theory2/.venv/bin/theory --json symbolic integrate --expr="x**2" --symbol=x
```

## Argument Parsing

Parse user arguments to determine the operation:

1. **compute-e7-alpha** or **e7** or **alpha**: Run E7 alpha computation
2. **lie-algebra** or **lie** with --type: Query Lie algebra
3. **eval** with --expr: Evaluate expression
4. **simplify** with --expr: Simplify expression
5. **solve** with --expr: Solve equation
6. **diff** with --expr: Differentiate
7. **integrate** with --expr: Integrate

Always use `--json` flag for structured output. Display results in a readable format.
