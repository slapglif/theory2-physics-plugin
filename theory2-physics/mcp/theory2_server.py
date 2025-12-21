#!/usr/bin/env python3
"""Theory2 MCP Server - Mathematical Physics Tooling Suite.

Exposes Theory2 CLI capabilities as MCP tools with rich descriptions and examples.
"""

import json
import subprocess
import sys
from typing import Any
import os
import datetime

DEBUG_LOG = "/tmp/theory2_debug.log"

def log(msg: str):
    """Log debug message to file."""
    with open(DEBUG_LOG, "a") as f:
        timestamp = datetime.datetime.now().isoformat()
        f.write(f"[{timestamp}] {msg}\n")

USE_HEADERS = True

# MCP protocol implementation
def send_response(response: dict) -> None:
    """Send JSON-RPC response to stdout."""
    msg = json.dumps(response)
    log(f"Sending response: {msg[:200]}...")
    
    if USE_HEADERS:
        sys.stdout.write(f"Content-Length: {len(msg)}\r\n\r\n{msg}")
    else:
        sys.stdout.write(f"{msg}\n")
        
    sys.stdout.flush()

def read_request() -> dict | None:
    """Read JSON-RPC request from stdin."""
    global USE_HEADERS
    try:
        first_line = sys.stdin.readline()
        if not first_line:
            log("Stdin closed")
            return None
        
        # Check if it's a header or direct JSON
        if first_line.startswith('{'):
            log(f"Received direct JSON line: {first_line[:200]}...")
            USE_HEADERS = False
            return json.loads(first_line)
            
        USE_HEADERS = True
        # Parse headers
        headers = {}
        if ":" in first_line:
            key, value = first_line.split(":", 1)
            headers[key.strip()] = value.strip()
            log(f"Read header: {key}={value}")
        
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            
            if line == "\r\n" or line == "\n":
                break
                
            if ":" in line:
                key, value = line.split(":", 1)
                headers[key.strip()] = value.strip()
                log(f"Read header: {key}={value}")

        content_length_str = headers.get("Content-Length")
        if not content_length_str:
            log("No Content-Length header found")
            return None
            
        content_length = int(content_length_str)
        log(f"Reading content of length: {content_length}")
        
        content = sys.stdin.read(content_length)
        if not content:
             log("Failed to read content")
             return None
             
        log(f"Received request: {content[:200]}...")
        return json.loads(content)
    except Exception as e:
        log(f"Error reading request: {e}")
        return None

THEORY2_BIN = "/home/mikeb/theory2/.venv/bin/theory"

TOOLS = [
    {
        "name": "theory2_symbolic_compute_e7_alpha",
        "description": """Compute the fine-structure constant (α⁻¹ ≈ 137) from E7 Lie algebra structure.

Uses the formula: α⁻¹ = dim(E7) + fundamental_rep/(2 × rank) = 133 + 56/14 = 137

This demonstrates a deep connection between exceptional Lie algebras and fundamental physics constants.

Example output:
- alpha_inverse: 137.0
- components: {dimension: 133, fundamental_rep: 56, rank: 7}
- comparison with CODATA: 137.035999084 (0.026% difference)""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "verify": {
                    "type": "boolean",
                    "description": "Compare result with experimental CODATA value",
                    "default": True
                },
                "precision": {
                    "type": "string",
                    "enum": ["double", "quad"],
                    "description": "Numerical precision for computation",
                    "default": "double"
                }
            }
        }
    },
    {
        "name": "theory2_symbolic_lie_algebra",
        "description": """Query properties of Lie algebras. Supports all exceptional and classical algebras.

Supported algebras: G2, F4, E6, E7, E8, SO10, SO8, SU5, SU3, SU2

Available queries:
- dimension: Total dimension of the algebra
- rank: Rank (number of Cartan generators)
- fundamental_rep: Dimension of fundamental representation
- alpha_inverse: Compute α⁻¹ = dim + fund/(2×rank) for ANY algebra

α⁻¹ values (E7 uniquely gives 137):
- E7: 137.0 (closest to experimental 137.036)
- E6: 80.25, E8: 263.5, G2: 15.75, F4: 55.25
- SO10: 46.6, SU5: 24.625""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "algebra_type": {
                    "type": "string",
                    "description": "Lie algebra type: G2, F4, E6, E7, E8, SO10, SO8, SU5, SU3, SU2",
                    "examples": ["E7", "E8", "SO10", "SU5"]
                },
                "query": {
                    "type": "string",
                    "enum": ["dimension", "rank", "fundamental_rep", "alpha_inverse", "weyl_group_order"],
                    "description": "Property to query"
                }
            },
            "required": ["algebra_type", "query"]
        }
    },
    {
        "name": "theory2_symbolic_compare_alpha",
        "description": """Compare α⁻¹ = dim + fund/(2×rank) across ALL supported Lie algebras.

Verifies that E7 is uniquely the only Lie algebra where this formula yields α⁻¹ ≈ 137.

Returns a ranked list sorted by closeness to experimental value 137.035999084.""",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "theory2_symbolic_eval",
        "description": """Evaluate symbolic mathematical expressions using SymPy.

Supports:
- Algebraic expressions: (x+1)**2, x**3 - 1
- Trigonometric: sin(x), cos(pi/4)
- Calculus: derivatives, integrals (use diff/integrate tools)
- Substitutions: evaluate at specific values

Examples:
- expr="(x+1)**2", substitutions={"x": 2} → 9
- expr="sin(pi/4)" → sqrt(2)/2
- expr="exp(I*pi) + 1" → 0 (Euler's identity)""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "expr": {
                    "type": "string",
                    "description": "Mathematical expression in SymPy syntax"
                },
                "substitutions": {
                    "type": "object",
                    "description": "Variable substitutions as {var: value}",
                    "additionalProperties": {"type": "number"}
                }
            },
            "required": ["expr"]
        }
    },
    {
        "name": "theory2_symbolic_simplify",
        "description": """Simplify mathematical expressions using SymPy's simplification algorithms.

Applies algebraic, trigonometric, and other simplifications.

Examples:
- "(x**2 - 1)/(x - 1)" → x + 1
- "sin(x)**2 + cos(x)**2" → 1
- "exp(log(x))" → x""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "expr": {
                    "type": "string",
                    "description": "Expression to simplify"
                }
            },
            "required": ["expr"]
        }
    },
    {
        "name": "theory2_symbolic_solve",
        "description": """Solve algebraic equations symbolically.

Finds roots/solutions of equations.

Examples:
- expr="x**2 - 1", symbol="x" → [-1, 1]
- expr="x**2 + 1", symbol="x" → [-I, I]
- expr="x**3 - 8", symbol="x" → [2, -1-sqrt(3)*I, -1+sqrt(3)*I]""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "expr": {
                    "type": "string",
                    "description": "Equation to solve (set equal to 0)"
                },
                "symbol": {
                    "type": "string",
                    "description": "Variable to solve for",
                    "default": "x"
                }
            },
            "required": ["expr"]
        }
    },
    {
        "name": "theory2_symbolic_diff",
        "description": """Compute symbolic derivatives.

Examples:
- expr="x**3", symbol="x" → 3*x**2
- expr="sin(x)", symbol="x" → cos(x)
- expr="exp(x**2)", symbol="x" → 2*x*exp(x**2)""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "expr": {
                    "type": "string",
                    "description": "Expression to differentiate"
                },
                "symbol": {
                    "type": "string",
                    "description": "Variable to differentiate with respect to",
                    "default": "x"
                }
            },
            "required": ["expr"]
        }
    },
    {
        "name": "theory2_symbolic_integrate",
        "description": """Compute symbolic integrals (indefinite).

Examples:
- expr="x**2", symbol="x" → x**3/3
- expr="1/x", symbol="x" → log(x)
- expr="exp(-x**2)", symbol="x" → sqrt(pi)*erf(x)/2""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "expr": {
                    "type": "string",
                    "description": "Expression to integrate"
                },
                "symbol": {
                    "type": "string",
                    "description": "Variable of integration",
                    "default": "x"
                }
            },
            "required": ["expr"]
        }
    },
    {
        "name": "theory2_numerical_quantum_chemistry",
        "description": """Perform quantum chemistry calculations (Hartree-Fock, DFT, CCSD).

Compute molecular energies and properties using:
- HF: Hartree-Fock (fastest, least accurate)
- DFT: Density Functional Theory with B3LYP, PBE, etc.
- CCSD: Coupled-Cluster (most accurate, slowest)

Molecule format: "ATOM x y z; ATOM x y z; ..." or shortcuts (H2O, CH4, NH3, CO2)

Examples:
- molecule="H2O", method="dft", xc="b3lyp" → water DFT energy
- molecule="H 0 0 0; H 0 0 0.74", method="hf" → H2 Hartree-Fock
- molecule="CH4", method="ccsd" → methane coupled-cluster""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "molecule": {
                    "type": "string",
                    "description": "Molecular geometry (XYZ format or shortcut)"
                },
                "method": {
                    "type": "string",
                    "enum": ["hf", "dft", "ccsd"],
                    "description": "Calculation method",
                    "default": "dft"
                },
                "basis": {
                    "type": "string",
                    "description": "Basis set",
                    "default": "def2-svp",
                    "examples": ["sto-3g", "6-31G", "cc-pVDZ", "def2-svp"]
                },
                "xc": {
                    "type": "string",
                    "description": "Exchange-correlation functional (for DFT)",
                    "default": "b3lyp",
                    "examples": ["b3lyp", "pbe", "pbe0", "m06-2x"]
                }
            },
            "required": ["molecule"]
        }
    },
    {
        "name": "theory2_numerical_quantum_circuit",
        "description": """Create and simulate quantum circuits.

Build quantum circuits and get measurement results or statevectors.

Available preset circuits:
- bell: 2-qubit Bell state |00⟩ + |11⟩
- ghz3: 3-qubit GHZ state
- ghz4: 4-qubit GHZ state

Examples:
- circuit="bell", shots=1024 → measurement counts {"00": ~512, "11": ~512}
- circuit="ghz3", statevector=true → state amplitudes""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "circuit": {
                    "type": "string",
                    "description": "Circuit type (bell, ghz3, ghz4)",
                    "enum": ["bell", "ghz3", "ghz4"]
                },
                "shots": {
                    "type": "integer",
                    "description": "Number of measurement shots",
                    "default": 1024
                },
                "statevector": {
                    "type": "boolean",
                    "description": "Return statevector instead of measurements",
                    "default": False
                }
            },
            "required": ["circuit"]
        }
    },
    {
        "name": "theory2_numerical_open_quantum_system",
        "description": """Simulate open quantum systems using QuTiP (Lindblad master equation).

Compute time evolution of quantum systems with decoherence and dissipation.

Available systems:
- rabi: Rabi oscillations of a driven qubit with decay
- jaynes-cummings: Atom-cavity coupling (quantum optics)
- spin-chain: Transverse field Ising model

Parameters:
- gamma: Decoherence/decay rate
- t_final: Simulation end time
- n_times: Number of time points

Examples:
- system="rabi", gamma=0.1 → Damped Rabi oscillations
- system="jaynes-cummings", t_final=50 → Cavity QED dynamics
- system="spin-chain" → Many-body quantum dynamics""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "system": {
                    "type": "string",
                    "enum": ["rabi", "jaynes-cummings", "spin-chain"],
                    "description": "Type of quantum system"
                },
                "gamma": {
                    "type": "number",
                    "description": "Decoherence rate",
                    "default": 0.1
                },
                "t_final": {
                    "type": "number",
                    "description": "Final simulation time",
                    "default": 10.0
                },
                "n_times": {
                    "type": "integer",
                    "description": "Number of time points",
                    "default": 100
                }
            },
            "required": ["system"]
        }
    },
    {
        "name": "theory2_numerical_quantum_state_analysis",
        "description": """Analyze quantum states using toqito (quantum information theory).

Compute entanglement measures, separability, and state properties.

Available state types:
- bell: Bell states (|00⟩+|11⟩)/√2 - maximally entangled
- ghz: GHZ states - multi-qubit entanglement
- werner: Werner states - mixed states parameterized by alpha

Computed properties:
- Purity (1 = pure, <1 = mixed)
- Von Neumann entropy
- Negativity, log-negativity
- Concurrence (2-qubit entanglement)
- PPT separability test

Examples:
- state_type="bell" → Analyze Bell state entanglement
- state_type="ghz", n_qubits=3 → 3-qubit GHZ analysis
- state_type="werner", alpha=0.7 → Mixed state with 70% purity""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "state_type": {
                    "type": "string",
                    "enum": ["bell", "ghz", "werner"],
                    "description": "Type of quantum state"
                },
                "n_qubits": {
                    "type": "integer",
                    "description": "Number of qubits (for GHZ)",
                    "default": 2
                },
                "alpha": {
                    "type": "number",
                    "description": "Mixing parameter (for Werner state, 0-1)",
                    "default": 0.5
                }
            },
            "required": ["state_type"]
        }
    },
    {
        "name": "theory2_ml_run_vqe",
        "description": """Run Variational Quantum Eigensolver (VQE) for molecular ground states.

VQE is a hybrid quantum-classical algorithm for finding ground state energies.
Uses parameterized quantum circuits optimized classically.

Parameters:
- molecule: Molecular formula (H2, LiH, etc.)
- bond_length: Interatomic distance in Angstroms
- basis: Basis set (sto-3g, 6-31G)
- n_layers: Ansatz circuit depth

Examples:
- molecule="H2", bond_length=0.74 → H2 ground state (~-1.14 Ha)
- molecule="LiH", bond_length=1.6 → LiH ground state
- n_layers=3 → Deeper ansatz for better accuracy""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "molecule": {
                    "type": "string",
                    "description": "Molecule formula",
                    "default": "H2"
                },
                "bond_length": {
                    "type": "number",
                    "description": "Bond length in Angstroms",
                    "default": 0.74
                },
                "basis": {
                    "type": "string",
                    "description": "Basis set",
                    "default": "sto-3g"
                },
                "n_layers": {
                    "type": "integer",
                    "description": "Number of ansatz layers",
                    "default": 2
                },
                "max_iterations": {
                    "type": "integer",
                    "description": "Max optimization iterations",
                    "default": 100
                }
            }
        }
    },
    {
        "name": "theory2_ml_run_qaoa",
        "description": """Run Quantum Approximate Optimization Algorithm (QAOA).

QAOA solves combinatorial optimization problems using quantum circuits.
Alternates between cost and mixer Hamiltonians.

Problem types:
- maxcut: Maximum cut problem on graphs
- tsp: Traveling salesman (small instances)
- sat: Boolean satisfiability

Parameters:
- problem_type: Type of optimization problem
- n_qubits: Problem size
- depth: Number of QAOA layers (p)

Examples:
- problem_type="maxcut", n_qubits=4 → 4-node MaxCut
- depth=3 → Deeper circuit for better approximation""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "problem_type": {
                    "type": "string",
                    "enum": ["maxcut", "tsp", "sat"],
                    "description": "Type of optimization problem",
                    "default": "maxcut"
                },
                "n_qubits": {
                    "type": "integer",
                    "description": "Number of qubits/problem size",
                    "default": 4
                },
                "depth": {
                    "type": "integer",
                    "description": "QAOA circuit depth (p)",
                    "default": 2
                }
            }
        }
    },
    {
        "name": "theory2_ml_train_fno",
        "description": """Train a Fourier Neural Operator for PDE solving.

FNOs learn mappings between function spaces - ideal for:
- Weather prediction
- Fluid dynamics
- Heat transfer
- Any PDE operator learning

Parameters:
- modes: Fourier modes to keep (higher = more resolution, more memory)
- width: Hidden channel dimension
- layers: Number of Fourier layers
- factorization: Tucker decomposition reduces memory 10x

Examples:
- modes=16, width=64, layers=4 → Standard FNO
- modes=32, width=128, factorization="tucker" → Large efficient FNO""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "modes": {
                    "type": "integer",
                    "description": "Number of Fourier modes",
                    "default": 12
                },
                "width": {
                    "type": "integer",
                    "description": "Hidden dimension width",
                    "default": 64
                },
                "layers": {
                    "type": "integer",
                    "description": "Number of Fourier layers",
                    "default": 4
                },
                "factorization": {
                    "type": "string",
                    "enum": ["dense", "tucker", "cp"],
                    "description": "Tensor factorization for memory efficiency",
                    "default": "tucker"
                }
            }
        }
    },
    {
        "name": "theory2_ml_train_e3nn",
        "description": """Train an E(3)-equivariant neural network for molecular/atomic systems.

E3NN respects 3D rotation/translation symmetry - ideal for:
- Molecular property prediction
- Force field learning
- Crystal structure analysis
- Protein folding

Irreps format: "NxLp" where N=multiplicity, L=angular momentum, p=parity (e/o)
Examples: "16x0e + 16x1o" = 16 scalars + 16 vectors

Examples:
- irreps_hidden="32x0e+16x1o+8x2e" → Rich representation
- use_gates=true → Gated nonlinearities (more expressive)""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "irreps_hidden": {
                    "type": "string",
                    "description": "Hidden layer irreps specification",
                    "default": "16x0e + 16x1o + 16x2e"
                },
                "layers": {
                    "type": "integer",
                    "description": "Number of convolution layers",
                    "default": 3
                },
                "use_gates": {
                    "type": "boolean",
                    "description": "Use gated nonlinearities",
                    "default": True
                }
            }
        }
    },
    {
        "name": "theory2_ml_solve_pde",
        "description": """Solve PDEs using Physics-Informed Neural Networks (PINNs).

PINNs embed physics equations into the loss function - no training data needed!

Available PDE types:
- heat: 1D heat equation ∂u/∂t = α ∂²u/∂x²
- poisson: 2D Poisson equation ∇²u = f

Examples:
- pde_type="heat", alpha=0.01, iterations=10000 → Heat diffusion
- pde_type="poisson", iterations=20000 → Steady-state potential""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pde_type": {
                    "type": "string",
                    "enum": ["heat", "poisson"],
                    "description": "Type of PDE to solve"
                },
                "iterations": {
                    "type": "integer",
                    "description": "Training iterations",
                    "default": 10000
                },
                "alpha": {
                    "type": "number",
                    "description": "Diffusion coefficient (for heat equation)",
                    "default": 0.01
                }
            },
            "required": ["pde_type"]
        }
    },
    {
        "name": "theory2_prove_lean",
        "description": """Prove mathematical statements using Lean 4 with RobustLeanProver.

RobustLeanProver provides intelligent tactic selection, parallel proof search, and caching.

Tactic Tiers (auto mode tries in order with 120s default timeout):
1. fast (parallel): rfl, trivial, decide (~1s)
2. arithmetic (parallel): norm_num, omega, ring, simp (~3s)
3. search (sequential): simp_all, aesop, tauto (~10s)
4. atp (sequential): duper, simp; ring, norm_num; simp (~30s each)
5. hammer (sequential): hammer with neural premise selection (~60s)

Available tactics:
- auto: Full 5-tier fallback including ATP provers (RECOMMENDED, use timeout=120)
- rfl: Reflexivity (fastest for definitional equalities)
- decide: Decidable propositions
- omega: Linear arithmetic
- simp: Simplification
- ring: Ring algebra
- duper: Superposition ATP prover (61% benchmark success, uses lean-hammer REPL)
- hammer: Neural premise selection + Duper + Aesop (uses lean-hammer REPL)

Problem Type Detection:
- Numeric equality (2 + 2 = 4) → rfl, decide
- Linear arithmetic (n + 0 = n) → omega, simp
- Decidable props (True, 1 < 2) → decide
- Complex theorems → duper, hammer

Features:
- Proof caching: Same statement = instant cache hit
- Parallel search: Multiple tactics tried simultaneously
- Problem analysis: Intelligent tactic ordering
- ATP provers: duper/hammer for hard theorems (require lean-hammer REPL)

Examples:
- statement="2 + 2 = 4" → auto proves with rfl in ~400ms
- statement="∀ n : Nat, n + 0 = n" → proves with simp in ~900ms
- statement="∀ a b : Nat, a + b = b + a", tactic="hammer" → proves using Nat.add_comm""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "statement": {
                    "type": "string",
                    "description": "Mathematical statement to prove (Lean 4 syntax)"
                },
                "tactic": {
                    "type": "string",
                    "enum": ["auto", "rfl", "decide", "simp", "omega", "ring", "trivial", "norm_num", "aesop", "tauto", "duper", "hammer"],
                    "description": "Proof tactic (auto = 5-tier fallback including ATP, duper/hammer = direct ATP)",
                    "default": "auto"
                },
                "timeout": {
                    "type": "integer",
                    "description": "Timeout in seconds (use 120+ for auto to reach ATP tiers)",
                    "default": 120
                },
                "no_cache": {
                    "type": "boolean",
                    "description": "Disable proof caching",
                    "default": False
                },
                "save": {
                    "type": "boolean",
                    "description": "Save successful proof to certificate store",
                    "default": False
                }
            },
            "required": ["statement"]
        }
    },
    {
        "name": "theory2_prove_search",
        "description": """Search mathlib4 theorem database (210K+ theorems).

Find existing theorems by name or statement pattern.

Examples:
- query="add_comm" → Find commutativity lemmas
- query="prime", search_in="statement" → Theorems about primes
- query="continuous" → Continuity-related theorems""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query"
                },
                "search_in": {
                    "type": "string",
                    "enum": ["name", "statement", "both"],
                    "description": "Where to search",
                    "default": "both"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "theory2_verify_cross_check",
        "description": """Cross-validate physics claims using multiple independent methods.

Verifies results by comparing:
- Symbolic: Algebraic/analytic computation
- Numerical: High-precision numerical evaluation
- Experimental: Known experimental values (CODATA, etc.)

Examples:
- claim="alpha_inv=137", methods="symbolic,numerical,experimental"
  → Compares E7 formula vs computation vs CODATA

- claim="H2_energy=-1.17", methods="symbolic,numerical"
  → Compares analytic vs quantum chemistry result""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "claim": {
                    "type": "string",
                    "description": "Physics claim to verify (name=value format)"
                },
                "methods": {
                    "type": "string",
                    "description": "Comma-separated verification methods",
                    "default": "symbolic,numerical"
                },
                "tolerance": {
                    "type": "number",
                    "description": "Acceptable relative tolerance",
                    "default": 0.001
                }
            },
            "required": ["claim"]
        }
    },
    {
        "name": "theory2_bioinformatics_analyze_sequence",
        "description": """Analyze DNA, RNA, or protein sequences using Biopython.

Computes sequence properties including:
- Sequence length and composition
- GC content (for nucleotide sequences)
- Molecular weight
- Amino acid frequency (for proteins)

Auto-detects sequence type or you can specify explicitly.

Examples:
- sequence="ATGCGATCGATCG" → DNA analysis with GC content
- sequence="MVLSPADKTNVK", seq_type="protein" → Protein properties
- sequence="AUGCGAUCGAUCG", seq_type="rna" → RNA analysis""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sequence": {
                    "type": "string",
                    "description": "DNA/RNA/Protein sequence string"
                },
                "seq_type": {
                    "type": "string",
                    "enum": ["auto", "dna", "rna", "protein"],
                    "description": "Sequence type (default: auto-detect)",
                    "default": "auto"
                },
                "explain": {
                    "type": "boolean",
                    "description": "Include detailed explanation",
                    "default": False
                }
            },
            "required": ["sequence"]
        }
    },
    {
        "name": "theory2_bioinformatics_translate_dna",
        "description": """Translate DNA sequence to protein using genetic code.

Uses standard codon table by default. Supports alternative tables:
- 1: Standard (default)
- 2: Vertebrate Mitochondrial
- 3: Yeast Mitochondrial
- And more (see NCBI codon tables)

Returns the translated protein sequence in one-letter amino acid codes.

Examples:
- sequence="ATGGCTAGCTAG" → Translates to protein (M-A-S-*)
- sequence="ATGAAATGA", table=1 → Uses standard genetic code
- sequence="ATGAAATAA", table=2 → Uses mitochondrial code""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sequence": {
                    "type": "string",
                    "description": "DNA sequence to translate"
                },
                "table": {
                    "type": "integer",
                    "description": "Codon table (1=Standard, 2=Mitochondrial)",
                    "default": 1
                }
            },
            "required": ["sequence"]
        }
    },
    {
        "name": "theory2_bioinformatics_analyze_protein",
        "description": """Analyze protein sequence properties using Biopython ProteinAnalysis.

Computes comprehensive protein properties:
- Molecular weight (Da)
- Isoelectric point (pI)
- Instability index (>40 = unstable)
- GRAVY score (hydrophobicity: + = hydrophobic, - = hydrophilic)
- Amino acid composition and frequencies
- Aromaticity

Examples:
- sequence="MVLSPADKTNVK" → Basic protein analysis
- sequence="MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH" → Hemoglobin fragment analysis
- explain=true → Include detailed property explanations""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sequence": {
                    "type": "string",
                    "description": "Protein sequence (one-letter amino acid codes)"
                },
                "explain": {
                    "type": "boolean",
                    "description": "Include detailed explanation",
                    "default": False
                }
            },
            "required": ["sequence"]
        }
    },
    {
        "name": "theory2_bioinformatics_load_structure",
        "description": """Load and analyze PDB structure files using Biopython Bio.PDB.

Reads protein structure files in PDB format and extracts:
- Number of models (NMR structures have multiple)
- Chain information
- Residue counts per chain
- Total atom counts
- Structure metadata

Useful for structural bioinformatics and understanding protein 3D structures.

Examples:
- pdb_file="1abc.pdb" → Analyze local PDB file
- pdb_file="/path/to/protein.pdb" → Full path to structure
- Returns: models, chains, residues, atoms""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pdb_file": {
                    "type": "string",
                    "description": "Path to PDB structure file"
                }
            },
            "required": ["pdb_file"]
        }
    },
    {
        "name": "theory2_combinatorics_create_graph",
        "description": """Create graphs from edge lists or use well-known named graphs.

Create custom graphs or use classical graph theory examples:

Named graphs available:
- petersen: Petersen graph (famous counterexample in graph theory)
- complete_5, complete_10: Complete graphs K5, K10
- cube, octahedron, icosahedron, dodecahedron: Platonic solids
- tutte: Tutte graph (counterexample to Tait's conjecture)
- heawood: Heawood graph (cage graph)
- karate: Zachary's karate club (social network)

Or create custom graphs from edge lists.

Examples:
- named_graph="petersen", analyze=true → Create & analyze Petersen graph
- edges="[[0,1],[1,2],[2,0]]" → Create triangle graph
- edges="[[0,1],[1,2]]", graph_type="directed" → Directed graph""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "edges": {
                    "type": "string",
                    "description": "Edge list as JSON: [[0,1],[1,2],[2,0]]"
                },
                "named_graph": {
                    "type": "string",
                    "enum": ["petersen", "complete_5", "complete_10", "cube", "octahedron",
                             "icosahedron", "dodecahedron", "tutte", "heawood", "karate"],
                    "description": "Create a well-known graph"
                },
                "graph_type": {
                    "type": "string",
                    "enum": ["undirected", "directed"],
                    "description": "Graph type",
                    "default": "undirected"
                },
                "analyze": {
                    "type": "boolean",
                    "description": "Include full graph analysis",
                    "default": False
                }
            }
        }
    },
    {
        "name": "theory2_combinatorics_analyze_graph",
        "description": """Comprehensive graph analysis using NetworkX algorithms.

Computes extensive graph properties:
- Connectivity (is_connected, number of components)
- Density (edge density)
- Diameter (longest shortest path)
- Clustering coefficient (local clustering)
- Planarity (can be drawn without edge crossings)
- Bipartiteness (2-colorable check)
- Chromatic number estimate (minimum colors needed)
- Degree statistics (min, max, average degree)

Examples:
- edges="[[0,1],[1,2],[2,0]]" → Analyze triangle (diameter=1, connected)
- edges="[[0,1],[1,2],[2,0],[0,3]]" → Analyze with explanation
- explain=true → Include detailed property explanations""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "edges": {
                    "type": "string",
                    "description": "Edge list as JSON: [[0,1],[1,2],[2,0]]"
                },
                "explain": {
                    "type": "boolean",
                    "description": "Include detailed explanation",
                    "default": False
                }
            },
            "required": ["edges"]
        }
    },
    {
        "name": "theory2_combinatorics_count",
        "description": """Compute combinatorial counting functions.

Available counting types:
- permutations: P(n,k) = n!/(n-k)! - ordered selections
- combinations: C(n,k) = n!/[k!(n-k)!] - unordered selections
- partitions: Integer partitions p(n)
- catalan: Catalan numbers C_n = (2n)!/[(n+1)!n!]
- bell: Bell numbers B_n (number of partitions of a set)
- stirling: Stirling numbers S(n,k) (set partitions into k subsets)
- derangements: D(n) - permutations with no fixed points
- fibonacci: Fibonacci numbers F(n)

Examples:
- type="permutations", n=5, k=3 → P(5,3) = 60
- type="combinations", n=10, k=3 → C(10,3) = 120
- type="catalan", n=5 → C_5 = 42
- type="bell", n=5, explain=true → B_5 = 52 with formula explanation""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["permutations", "combinations", "partitions", "catalan",
                             "bell", "stirling", "derangements", "fibonacci"],
                    "description": "Type of counting"
                },
                "n": {
                    "type": "integer",
                    "description": "Main parameter n"
                },
                "k": {
                    "type": "integer",
                    "description": "Secondary parameter k (for permutations, combinations, stirling)"
                },
                "explain": {
                    "type": "boolean",
                    "description": "Include formula explanation",
                    "default": False
                }
            },
            "required": ["type", "n"]
        }
    },
    {
        "name": "theory2_combinatorics_solve_tsp",
        "description": """Solve the Traveling Salesman Problem using various algorithms.

Finds shortest route visiting all cities exactly once and returning to start.

Available methods:
- greedy: Fast greedy heuristic (good for large instances)
- nearest_neighbor: Classic nearest neighbor heuristic
- christofides: 1.5-approximation algorithm (proven guarantee)
- exact: Brute force optimal (only for small instances, n ≤ 10)

Distance matrix format: Symmetric n×n matrix with 0 on diagonal.

Examples:
- distances="[[0,10,15,20],[10,0,35,25],[15,35,0,30],[20,25,30,0]]", method="greedy"
  → 4-city TSP with greedy solution
- distances="[[0,1,2],[1,0,3],[2,3,0]]", method="exact"
  → 3-city optimal solution
- method="christofides" → Guaranteed ≤ 1.5 × optimal""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "distances": {
                    "type": "string",
                    "description": "Distance matrix as JSON: [[0,1,2],[1,0,3],[2,3,0]]"
                },
                "method": {
                    "type": "string",
                    "enum": ["greedy", "nearest_neighbor", "christofides", "exact"],
                    "description": "TSP solving method",
                    "default": "greedy"
                }
            },
            "required": ["distances"]
        }
    },
    {
        "name": "theory2_combinatorics_solve_knapsack",
        "description": """Solve the 0/1 Knapsack problem (classic dynamic programming problem).

Given items with values and weights, find the maximum value subset that fits in knapsack.

Methods:
- dp: Dynamic programming - optimal solution O(n×capacity)
- greedy: Greedy by value/weight ratio - fast approximation

Returns:
- Maximum total value achievable
- Selected item indices
- Total weight used

Examples:
- values="[60,100,120]", weights="[10,20,30]", capacity=50
  → Items 1,2 selected for value=220
- values="[10,20,30]", weights="[1,2,3]", capacity=4, method="dp"
  → Optimal: items 0,1,2 (if they fit) or best combination
- method="greedy" → Fast approximation for large instances""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "values": {
                    "type": "string",
                    "description": "Item values as JSON: [60, 100, 120]"
                },
                "weights": {
                    "type": "string",
                    "description": "Item weights as JSON: [10, 20, 30]"
                },
                "capacity": {
                    "type": "integer",
                    "description": "Knapsack capacity"
                },
                "method": {
                    "type": "string",
                    "enum": ["dp", "greedy"],
                    "description": "Solving method (dp=optimal, greedy=fast)",
                    "default": "dp"
                }
            },
            "required": ["values", "weights", "capacity"]
        }
    }
]


def run_theory2_command(args: list[str]) -> dict[str, Any]:
    """Execute Theory2 CLI command and return JSON result."""
    cmd = [THEORY2_BIN, "--json"] + args
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            try:
                # Theory2 CLI may output extra messages before JSON
                # Find the first { and parse from there
                json_start = result.stdout.find('{')
                if json_start >= 0:
                    json_str = result.stdout[json_start:]
                    return json.loads(json_str)
                else:
                    return json.loads(result.stdout)
            except json.JSONDecodeError:
                return {"status": "success", "output": result.stdout}
        else:
            return {"status": "error", "error": result.stderr or result.stdout}
    except subprocess.TimeoutExpired:
        return {"status": "error", "error": "Command timed out after 300 seconds"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def handle_tool_call(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Route tool calls to appropriate Theory2 commands."""

    if name == "theory2_symbolic_compute_e7_alpha":
        args = ["symbolic", "compute-e7-alpha"]
        if arguments.get("verify", True):
            args.append("--verify")
        if arguments.get("precision"):
            args.extend(["--precision", arguments["precision"]])
        return run_theory2_command(args)

    elif name == "theory2_symbolic_lie_algebra":
        return run_theory2_command([
            "symbolic", "lie-algebra",
            "--type", arguments["algebra_type"],
            "--query", arguments["query"]
        ])

    elif name == "theory2_symbolic_compare_alpha":
        return run_theory2_command(["symbolic", "compare-alpha"])

    elif name == "theory2_symbolic_eval":
        args = ["symbolic", "eval", "--expr", arguments["expr"]]
        if arguments.get("substitutions"):
            args.extend(["--substitutions", json.dumps(arguments["substitutions"])])
        return run_theory2_command(args)

    elif name == "theory2_symbolic_simplify":
        return run_theory2_command([
            "symbolic", "simplify", "--expr", arguments["expr"]
        ])

    elif name == "theory2_symbolic_solve":
        args = ["symbolic", "solve", "--expr", arguments["expr"]]
        if arguments.get("symbol"):
            args.extend(["--symbol", arguments["symbol"]])
        return run_theory2_command(args)

    elif name == "theory2_symbolic_diff":
        args = ["symbolic", "diff", "--expr", arguments["expr"]]
        if arguments.get("symbol"):
            args.extend(["--symbol", arguments["symbol"]])
        return run_theory2_command(args)

    elif name == "theory2_symbolic_integrate":
        args = ["symbolic", "integrate", "--expr", arguments["expr"]]
        if arguments.get("symbol"):
            args.extend(["--symbol", arguments["symbol"]])
        return run_theory2_command(args)

    elif name == "theory2_numerical_quantum_chemistry":
        args = ["numerical", "quantum-chemistry", "--molecule", arguments["molecule"]]
        if arguments.get("method"):
            args.extend(["--method", arguments["method"]])
        if arguments.get("basis"):
            args.extend(["--basis", arguments["basis"]])
        if arguments.get("xc"):
            args.extend(["--xc", arguments["xc"]])
        return run_theory2_command(args)

    elif name == "theory2_numerical_quantum_circuit":
        args = ["numerical", "quantum-circuit", "--circuit", arguments["circuit"]]
        if arguments.get("shots"):
            args.extend(["--shots", str(arguments["shots"])])
        if arguments.get("statevector"):
            args.append("--statevector")
        return run_theory2_command(args)

    elif name == "theory2_numerical_open_quantum_system":
        args = ["numerical", "open-quantum-system", "--system", arguments["system"]]
        if arguments.get("gamma"):
            args.extend(["--gamma", str(arguments["gamma"])])
        if arguments.get("t_final"):
            args.extend(["--t-final", str(arguments["t_final"])])
        if arguments.get("n_times"):
            args.extend(["--n-times", str(arguments["n_times"])])
        return run_theory2_command(args)

    elif name == "theory2_numerical_quantum_state_analysis":
        args = ["numerical", "quantum-state-analysis", "--state-type", arguments["state_type"]]
        if arguments.get("n_qubits"):
            args.extend(["--n-qubits", str(arguments["n_qubits"])])
        if arguments.get("alpha"):
            args.extend(["--alpha", str(arguments["alpha"])])
        return run_theory2_command(args)

    elif name == "theory2_ml_run_vqe":
        args = ["ml", "run-vqe"]
        if arguments.get("molecule"):
            args.extend(["--molecule", arguments["molecule"]])
        if arguments.get("bond_length"):
            args.extend(["--bond-length", str(arguments["bond_length"])])
        if arguments.get("basis"):
            args.extend(["--basis", arguments["basis"]])
        if arguments.get("n_layers"):
            args.extend(["--n-layers", str(arguments["n_layers"])])
        if arguments.get("max_iterations"):
            args.extend(["--max-iterations", str(arguments["max_iterations"])])
        return run_theory2_command(args)

    elif name == "theory2_ml_run_qaoa":
        args = ["ml", "run-qaoa"]
        if arguments.get("problem_type"):
            args.extend(["--problem-type", arguments["problem_type"]])
        if arguments.get("n_qubits"):
            args.extend(["--n-qubits", str(arguments["n_qubits"])])
        if arguments.get("depth"):
            args.extend(["--depth", str(arguments["depth"])])
        return run_theory2_command(args)

    elif name == "theory2_ml_train_fno":
        args = ["ml", "train-fno"]
        if arguments.get("modes"):
            args.extend(["--modes", str(arguments["modes"])])
        if arguments.get("width"):
            args.extend(["--width", str(arguments["width"])])
        if arguments.get("layers"):
            args.extend(["--layers", str(arguments["layers"])])
        if arguments.get("factorization"):
            args.extend(["--factorization", arguments["factorization"]])
        return run_theory2_command(args)

    elif name == "theory2_ml_train_e3nn":
        args = ["ml", "train-e3nn"]
        if arguments.get("irreps_hidden"):
            args.extend(["--irreps-hidden", arguments["irreps_hidden"]])
        if arguments.get("layers"):
            args.extend(["--layers", str(arguments["layers"])])
        if arguments.get("use_gates"):
            args.append("--use-gates")
        return run_theory2_command(args)

    elif name == "theory2_ml_solve_pde":
        args = ["ml", "solve-pde", "--pde-type", arguments["pde_type"]]
        if arguments.get("iterations"):
            args.extend(["--iterations", str(arguments["iterations"])])
        if arguments.get("alpha"):
            args.extend(["--alpha", str(arguments["alpha"])])
        return run_theory2_command(args)

    elif name == "theory2_prove_lean":
        args = ["prove", "lean", "--statement", arguments["statement"]]
        if arguments.get("tactic"):
            args.extend(["--tactic", arguments["tactic"]])
        if arguments.get("timeout"):
            args.extend(["--timeout", str(arguments["timeout"])])
        if arguments.get("no_cache"):
            args.append("--no-cache")
        if arguments.get("save"):
            args.append("--save")
        return run_theory2_command(args)

    elif name == "theory2_prove_search":
        args = ["prove", "search", "--query", arguments["query"]]
        if arguments.get("search_in"):
            args.extend(["--search-in", arguments["search_in"]])
        return run_theory2_command(args)

    elif name == "theory2_verify_cross_check":
        args = ["verify", "cross-check", "--claim", arguments["claim"]]
        if arguments.get("methods"):
            args.extend(["--methods", arguments["methods"]])
        if arguments.get("tolerance"):
            args.extend(["--tolerance", str(arguments["tolerance"])])
        return run_theory2_command(args)

    elif name == "theory2_bioinformatics_analyze_sequence":
        args = ["bioinformatics", "analyze-sequence", "--sequence", arguments["sequence"]]
        if arguments.get("seq_type"):
            args.extend(["--seq-type", arguments["seq_type"]])
        if arguments.get("explain"):
            args.append("--explain")
        return run_theory2_command(args)

    elif name == "theory2_bioinformatics_translate_dna":
        args = ["bioinformatics", "translate-dna", "--sequence", arguments["sequence"]]
        if arguments.get("table"):
            args.extend(["--table", str(arguments["table"])])
        return run_theory2_command(args)

    elif name == "theory2_bioinformatics_analyze_protein":
        args = ["bioinformatics", "analyze-protein", "--sequence", arguments["sequence"]]
        if arguments.get("explain"):
            args.append("--explain")
        return run_theory2_command(args)

    elif name == "theory2_bioinformatics_load_structure":
        args = ["bioinformatics", "load-structure", "--pdb-file", arguments["pdb_file"]]
        return run_theory2_command(args)

    elif name == "theory2_combinatorics_create_graph":
        args = ["combinatorics", "create-graph"]
        if arguments.get("edges"):
            args.extend(["--edges", arguments["edges"]])
        if arguments.get("named_graph"):
            args.extend(["--named-graph", arguments["named_graph"]])
        if arguments.get("graph_type"):
            args.extend(["--graph-type", arguments["graph_type"]])
        if arguments.get("analyze"):
            args.append("--analyze")
        return run_theory2_command(args)

    elif name == "theory2_combinatorics_analyze_graph":
        args = ["combinatorics", "analyze-graph", "--edges", arguments["edges"]]
        if arguments.get("explain"):
            args.append("--explain")
        return run_theory2_command(args)

    elif name == "theory2_combinatorics_count":
        args = ["combinatorics", "count", "--type", arguments["type"], "--n", str(arguments["n"])]
        if arguments.get("k"):
            args.extend(["--k", str(arguments["k"])])
        if arguments.get("explain"):
            args.append("--explain")
        return run_theory2_command(args)

    elif name == "theory2_combinatorics_solve_tsp":
        args = ["combinatorics", "tsp", "--distances", arguments["distances"]]
        if arguments.get("method"):
            args.extend(["--method", arguments["method"]])
        return run_theory2_command(args)

    elif name == "theory2_combinatorics_solve_knapsack":
        args = ["combinatorics", "knapsack",
                "--values", arguments["values"],
                "--weights", arguments["weights"],
                "--capacity", str(arguments["capacity"])]
        if arguments.get("method"):
            args.extend(["--method", arguments["method"]])
        return run_theory2_command(args)

    else:
        return {"status": "error", "error": f"Unknown tool: {name}"}


def main():
    """Main MCP server loop."""
    log("Server starting...")
    try:
        while True:
            request = read_request()
            if request is None:
                break

            method = request.get("method", "")
            req_id = request.get("id")
            params = request.get("params", {})
            
            log(f"Handling method: {method}")

            if method == "initialize":
                send_response({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {"listChanged": False}
                        },
                        "serverInfo": {
                            "name": "theory2-physics",
                            "version": "1.0.0"
                        }
                    }
                })

            elif method == "notifications/initialized":
                pass  # No response needed

            elif method == "ping":
                send_response({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {}
                })

            elif method == "tools/list":
                send_response({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"tools": TOOLS}
                })

            elif method == "tools/call":
                tool_name = params.get("name", "")
                tool_args = params.get("arguments", {})
                log(f"Calling tool: {tool_name}")
                result = handle_tool_call(tool_name, tool_args)
                send_response({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }]
                    }
                })

            else:
                log(f"Method not found: {method}")
                send_response({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                })
    except Exception as e:
        log(f"Server crashed: {e}")
        raise


if __name__ == "__main__":
    main()
