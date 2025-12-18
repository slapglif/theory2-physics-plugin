# Theory2 Physics Plugin for Claude Code

A comprehensive mathematical physics tooling plugin that provides access to symbolic math, numerical physics, physics ML, theorem proving, and scientific verification through the Theory2 CLI.

## Features

- **Symbolic Mathematics**: Lie algebras (E7→α⁻¹=137), SymPy operations, high-precision arithmetic
- **Numerical Physics**: Quantum chemistry (HF, DFT, CCSD), quantum circuit simulation
- **Physics ML**: Fourier Neural Operators, PINNs, E3NN equivariant networks
- **Theorem Proving**: Lean 4 with mathlib4 (210K+ theorems), LeanHammer
- **Scientific Verification**: Multi-method cross-validation, hermeneutic methodology

## Installation

### Prerequisites

1. Theory2 must be installed at `/home/mikeb/theory2`
2. Python virtual environment with dependencies activated

### Plugin Installation

```bash
# Clone or copy to Claude plugins directory
cp -r theory2-plugin ~/.claude/plugins/

# Or use with --plugin-dir
claude --plugin-dir /path/to/theory2-plugin
```

## Usage

### Slash Commands

```bash
/theory2-physics:symbolic compute-e7-alpha --verify
/theory2-physics:numerical quantum-chemistry --molecule="H2O" --method=dft
/theory2-physics:ml solve-pde --pde-type=heat --iterations=10000
/theory2-physics:prove lean --statement="2 + 2 = 4" --tactic=norm_num
/theory2-physics:verify cross-check --claim="alpha_inv=137"
```

### MCP Tools

The plugin provides rich MCP tools with detailed descriptions:

- `theory2_symbolic_compute_e7_alpha` - E7 Lie algebra → fine-structure constant
- `theory2_symbolic_lie_algebra` - Query Lie algebra properties
- `theory2_symbolic_eval/simplify/solve/diff/integrate` - SymPy operations
- `theory2_numerical_quantum_chemistry` - HF/DFT/CCSD calculations
- `theory2_numerical_quantum_circuit` - Quantum circuit simulation
- `theory2_ml_train_fno/train_e3nn/solve_pde` - Physics ML models
- `theory2_prove_lean/search` - Lean 4 theorem proving
- `theory2_verify_cross_check` - Multi-method verification

### Agents

- **physics-solver**: Autonomous multi-step physics problem solving
- **physics-verifier**: Cross-validation and verification specialist

## Scientific Validation Methodology

The plugin implements a rigorous validation workflow:

1. **Hermeneutic Circle**: Iterative part↔whole understanding
2. **Prior Knowledge Search**: Task memory integration
3. **Multi-Method Verification**: Symbolic + numerical + experimental
4. **Deep Exploration**: Systematic hypothesis testing
5. **Resolution**: Uncertainty quantification and documentation

## Components

```
theory2-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── commands/                 # Slash commands
│   ├── symbolic.md
│   ├── numerical.md
│   ├── ml.md
│   ├── prove.md
│   └── verify.md
├── agents/                   # Autonomous agents
│   ├── physics-solver.md
│   └── physics-verifier.md
├── skills/
│   └── theory2-physics/
│       └── SKILL.md          # Usage skill
├── hooks/
│   └── hooks.json            # Event hooks
├── mcp/
│   └── theory2_server.py     # MCP server
└── .mcp.json                 # MCP configuration
```

## Repository

- **Theory2 Source**: https://github.com/slapglif/theory2
- **Plugin Source**: Part of Theory2 repository

## License

MIT
