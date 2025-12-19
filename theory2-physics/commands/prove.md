---
name: prove
description: Theorem proving - Lean 4 with RobustLeanProver (auto fallback, parallel search, caching)
argument-hint: <operation> [options]
allowed-tools:
  - Bash
  - Read
---

# Theory2 Theorem Proving

Prove mathematical statements using Lean 4 with RobustLeanProver, which provides intelligent tactic selection, parallel proof search, and caching.

## Quick Start (Recommended)

```bash
# Automatic proof search - tries 14+ tactics intelligently
/home/mikeb/theory2/.venv/bin/theory --json prove lean \
  --statement="2 + 2 = 4"

# Quantified statements
/home/mikeb/theory2/.venv/bin/theory --json prove lean \
  --statement="∀ n : Nat, n + 0 = n"
```

## Tactic Tiers (Auto Mode)

RobustLeanProver tries tactics in order:

| Tier | Tactics | Speed | Mode |
|------|---------|-------|------|
| fast | rfl, trivial, decide | ~100ms | Parallel |
| arithmetic | norm_num, omega, ring, simp | ~500ms | Parallel |
| search | simp_all, aesop, tauto | ~3s | Sequential |
| combined | simp; ring, norm_num; simp | ~10s | Sequential |

## Specific Tactics

```bash
# Reflexivity (fastest)
theory --json prove lean --statement="2 + 2 = 4" --tactic=rfl

# Decidable propositions
theory --json prove lean --statement="10 * 10 = 100" --tactic=decide

# Linear arithmetic
theory --json prove lean --statement="∀ n : Nat, n ≤ n + 1" --tactic=omega

# Simplification
theory --json prove lean --statement="∀ x, x + 0 = x" --tactic=simp

# Ring algebra (requires mathlib in REPL)
theory --json prove lean --statement="∀ a b : Int, a + b = b + a" --tactic=ring
```

## Options

```bash
--statement="..."    # Lean 4 statement to prove (required)
--tactic=auto        # RobustLeanProver (default, recommended)
--tactic=<name>      # Specific tactic: rfl, simp, decide, omega, ring
--timeout=60         # Timeout in seconds (default: 60)
--no-cache           # Disable proof caching
--save               # Save to proof certificate store
```

## Problem Type → Best Tactics

| Problem Type | Example | Suggested Tactics |
|--------------|---------|-------------------|
| Numeric equality | `2 + 2 = 4` | rfl, decide |
| Linear arithmetic | `n + 0 = n` | omega, simp |
| Ring/polynomial | `(a+b)^2 = ...` | ring (needs mathlib) |
| Decidable prop | `True`, `1 < 2` | decide |
| Inductive | `List.length ...` | induction, cases |

## Proof Caching

- Successful proofs are cached to `~/.cache/theory2/proofs/`
- Same statement = instant cache hit (no REPL call)
- Use `--no-cache` to force re-computation

## Searching & Listing Proofs

```bash
# Search by keyword
theory --json prove search --query="add_comm" --search-in=name
theory --json prove search --query="continuous" --search-in=statement
theory --json prove search --query="prime" --search-in=both

# List saved proofs
theory --json prove list
theory --json prove list --verified-only
```

## Lean 4 Statement Syntax

- **Types**: `Nat`, `Int`, `Real`, `Complex`
- **Quantifiers**: `∀` (forall), `∃` (exists)
- **Operators**: `+`, `-`, `*`, `/`, `^`, `=`, `≠`, `<`, `≤`, `>`, `≥`
- **Logic**: `∧` (and), `∨` (or), `→` (implies), `¬` (not)

## Expected Output

### Successful Proof
```json
{
  "status": "success",
  "result": {
    "proof_complete": true,
    "theorem": "theorem_123456",
    "statement": "2 + 2 = 4",
    "proof_text": "theorem theorem_123456 : 2 + 2 = 4 := rfl",
    "tactics_used": ["rfl"],
    "proof_steps": 1
  },
  "metadata": {
    "mode": "robust_fallback",
    "duration_ms": 403
  }
}
```

### Failed Proof
```json
{
  "status": "error",
  "error": {
    "type": "ProofFailed",
    "message": "Exhausted all 14 tactics across 4 tiers"
  }
}
```

## Python API

```python
from theorem_proving import RobustLeanProver, analyze_problem

# Automatic proof
prover = RobustLeanProver(verbose=True, use_cache=True)
result = prover.prove("2 + 2 = 4", timeout=30)

# Problem analysis
analysis = analyze_problem("(a + b)^2 = a^2 + 2*a*b + b^2")
print(f"Type: {analysis.problem_type}")  # "algebraic"
print(f"Suggested: {analysis.suggested_tactics}")  # ["ring", ...]
```
