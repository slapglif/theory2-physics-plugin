---
name: prove
description: Theorem proving - Lean 4 proofs, mathlib search
argument-hint: <operation> [options]
allowed-tools:
  - Bash
  - Read
---

# Theory2 Theorem Proving

Prove mathematical statements using Lean 4 and search mathlib4.

## Proving Theorems

```bash
# Simple arithmetic
/home/mikeb/theory2/.venv/bin/theory --json prove lean \
  --statement="2 + 2 = 4" --tactic=norm_num

# Ring algebra
/home/mikeb/theory2/.venv/bin/theory --json prove lean \
  --statement="∀ x y : Int, x + y = y + x" --tactic=ring

# Using LeanHammer for difficult proofs
/home/mikeb/theory2/.venv/bin/theory --json prove lean \
  --statement="∀ n : Nat, n + 0 = n" --hammer

# Save successful proof
/home/mikeb/theory2/.venv/bin/theory --json prove lean \
  --statement="1 + 1 = 2" --tactic=norm_num --save
```

## Available Tactics

| Tactic | Use Case | Example |
|--------|----------|---------|
| `norm_num` | Numerical computation | `2^10 = 1024` |
| `ring` | Ring equations | `(a+b)² = a²+2ab+b²` |
| `simp` | Simplification | Uses simp lemmas |
| `omega` | Linear arithmetic | Integer inequalities |
| `auto` | Automatic selection | Tries multiple tactics |
| `hammer` | LeanHammer | Complex proofs (external solvers) |

## Searching Theorems

Search mathlib4's 210K+ theorems:

```bash
# Search by name
/home/mikeb/theory2/.venv/bin/theory --json prove search \
  --query="add_comm" --search-in=name

# Search in statements
/home/mikeb/theory2/.venv/bin/theory --json prove search \
  --query="continuous" --search-in=statement

# Search both
/home/mikeb/theory2/.venv/bin/theory --json prove search \
  --query="prime" --search-in=both
```

## Listing Proofs

```bash
# List all saved proofs
/home/mikeb/theory2/.venv/bin/theory --json prove list

# Only verified proofs
/home/mikeb/theory2/.venv/bin/theory --json prove list --verified-only
```

## Lean 4 Statement Syntax

- **Types**: `Nat`, `Int`, `Real`, `Complex`
- **Quantifiers**: `∀` (forall), `∃` (exists)
- **Operators**: `+`, `-`, `*`, `/`, `^`, `=`, `≠`, `<`, `≤`, `>`, `≥`
- **Logic**: `∧` (and), `∨` (or), `→` (implies), `¬` (not)

## Argument Parsing

1. **lean** with --statement: Prove a theorem
2. **search** with --query: Search mathlib
3. **list**: Show saved proofs

Always use `--json` for structured output.
