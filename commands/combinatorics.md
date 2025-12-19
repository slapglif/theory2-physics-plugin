---
name: combinatorics
description: Combinatorics and graph theory (NetworkX) - graph algorithms, enumeration, optimization
argument-hint: <operation> [options]
allowed-tools:
  - Bash
  - Read
---

# Theory2 Combinatorics

Execute graph theory, combinatorial counting, and optimization algorithms using NetworkX and custom implementations.

## Graph Theory Operations

### Create Graph

```bash
# Create from edge list
/home/mikeb/theory2/.venv/bin/theory --json combinatorics create-graph \
  --edges="[[0,1],[1,2],[2,0]]"

# Create well-known graphs
/home/mikeb/theory2/.venv/bin/theory --json combinatorics create-graph \
  --named-graph=petersen --analyze

# Available named graphs:
# petersen, complete_5, complete_10, cube, octahedron,
# icosahedron, dodecahedron, tutte, heawood, karate

# Directed graph
/home/mikeb/theory2/.venv/bin/theory --json combinatorics create-graph \
  --edges="[[0,1],[1,2]]" --graph-type=directed
```

**Output**:
```json
{
  "status": "success",
  "result": {
    "num_nodes": 3,
    "num_edges": 3,
    "is_directed": false,
    "analysis": {
      "is_connected": true,
      "density": 1.0,
      "diameter": 1,
      "is_tree": false,
      "is_bipartite": false,
      "is_planar": true,
      "chromatic_number": 3
    }
  }
}
```

### Analyze Graph

Comprehensive graph analysis including connectivity, density, diameter, clustering coefficient, planarity, bipartiteness, and chromatic number estimates.

```bash
/home/mikeb/theory2/.venv/bin/theory --json combinatorics analyze-graph \
  --edges="[[0,1],[1,2],[2,0],[0,3]]" --explain
```

**Output**:
```json
{
  "status": "success",
  "result": {
    "num_nodes": 4,
    "num_edges": 4,
    "density": 0.6667,
    "average_degree": 2.0,
    "is_connected": true,
    "is_tree": false,
    "is_bipartite": false,
    "is_planar": true,
    "diameter": 2,
    "clustering_coefficient": 0.5,
    "chromatic_number": 3
  }
}
```

### Find Paths

Find shortest or all paths between nodes.

```bash
# Find shortest path
/home/mikeb/theory2/.venv/bin/theory --json combinatorics find-paths \
  --edges="[[0,1],[1,2],[2,3]]" --source=0 --target=3 --algorithm=shortest

# Find all shortest paths
/home/mikeb/theory2/.venv/bin/theory --json combinatorics find-paths \
  --edges="[[0,1],[1,2],[2,3],[0,2]]" --source=0 --target=3 --algorithm=all_shortest

# Find all simple paths
/home/mikeb/theory2/.venv/bin/theory --json combinatorics find-paths \
  --edges="[[0,1],[1,2],[2,3],[0,2]]" --source=0 --target=3 --algorithm=all_simple
```

**Output**:
```json
{
  "status": "success",
  "result": {
    "path": [0, 1, 2, 3],
    "length": 3
  }
}
```

### Graph Coloring

Color graph vertices with minimum colors (greedy approximation).

```bash
/home/mikeb/theory2/.venv/bin/theory --json combinatorics graph-coloring \
  --edges="[[0,1],[1,2],[2,0]]" --strategy=largest_first

# Strategies: largest_first, smallest_last, saturation_largest_first
```

**Output**:
```json
{
  "status": "success",
  "result": {
    "coloring": {"0": 0, "1": 1, "2": 2},
    "num_colors": 3
  }
}
```

## Combinatorial Counting

### Count Operations

```bash
# Permutations: P(n,k) = n!/(n-k)!
/home/mikeb/theory2/.venv/bin/theory --json combinatorics count \
  --type=permutations --n=5 --k=3 --explain

# Combinations: C(n,k) = n!/(k!(n-k)!)
/home/mikeb/theory2/.venv/bin/theory --json combinatorics count \
  --type=combinations --n=10 --k=4 --explain

# Catalan numbers: C_n = (2n)!/((n+1)!×n!)
/home/mikeb/theory2/.venv/bin/theory --json combinatorics count \
  --type=catalan --n=10 --explain

# Bell numbers: number of ways to partition a set
/home/mikeb/theory2/.venv/bin/theory --json combinatorics count \
  --type=bell --n=10 --explain

# Integer partitions
/home/mikeb/theory2/.venv/bin/theory --json combinatorics count \
  --type=partitions --n=10

# Stirling numbers (1st and 2nd kind)
/home/mikeb/theory2/.venv/bin/theory --json combinatorics count \
  --type=stirling --n=10 --k=4 --explain

# Derangements: permutations with no fixed points
/home/mikeb/theory2/.venv/bin/theory --json combinatorics count \
  --type=derangements --n=10 --explain

# Fibonacci numbers
/home/mikeb/theory2/.venv/bin/theory --json combinatorics count \
  --type=fibonacci --n=20 --explain
```

**Output (Permutations)**:
```json
{
  "status": "success",
  "result": {
    "type": "permutations",
    "n": 5,
    "k": 3,
    "count": 60
  },
  "explanation": "P(n,k) = n!/(n-k)! = 5!/(5-3)! = 60"
}
```

**Output (Catalan)**:
```json
{
  "status": "success",
  "result": {
    "type": "catalan",
    "n": 10,
    "count": 16796
  },
  "explanation": "C_n = (2n)!/((n+1)!×n!) = 16796\nCounts: valid parentheses, binary trees, lattice paths"
}
```

**Output (Stirling)**:
```json
{
  "status": "success",
  "result": {
    "type": "stirling",
    "n": 10,
    "k": 4,
    "count_first_kind": 269325,
    "count_second_kind": 34105
  },
  "explanation": "S1(10,4) = 269325 (permutations with 4 cycles)\nS2(10,4) = 34105 (partitions into 4 subsets)"
}
```

## Combinatorial Optimization

### Traveling Salesman Problem (TSP)

Find shortest tour visiting all cities.

```bash
/home/mikeb/theory2/.venv/bin/theory --json combinatorics tsp \
  --distances="[[0,10,15,20],[10,0,35,25],[15,35,0,30],[20,25,30,0]]" \
  --method=greedy

# Methods: greedy, nearest_neighbor, christofides, exact
```

**Output**:
```json
{
  "status": "success",
  "result": {
    "tour": [0, 1, 3, 2, 0],
    "total_distance": 80,
    "method": "greedy"
  }
}
```

### Knapsack Problem

0/1 Knapsack: select items to maximize value within capacity constraint.

```bash
# Dynamic programming (optimal)
/home/mikeb/theory2/.venv/bin/theory --json combinatorics knapsack \
  --values="[60,100,120]" --weights="[10,20,30]" --capacity=50 --method=dp

# Greedy approximation (faster)
/home/mikeb/theory2/.venv/bin/theory --json combinatorics knapsack \
  --values="[60,100,120]" --weights="[10,20,30]" --capacity=50 --method=greedy
```

**Output**:
```json
{
  "status": "success",
  "result": {
    "max_value": 220,
    "selected_items": [1, 2],
    "total_weight": 50,
    "method": "dp"
  }
}
```

### Vertex Cover

Find minimum set of vertices covering all edges.

```bash
/home/mikeb/theory2/.venv/bin/theory --json combinatorics vertex-cover \
  --edges="[[0,1],[1,2],[2,3],[3,0]]" --method=approx

# Methods: approx (2-approximation), greedy, exact
```

**Output**:
```json
{
  "status": "success",
  "result": {
    "cover": [0, 2],
    "cover_size": 2,
    "method": "approx"
  }
}
```

### Independent Set

Find maximum set of non-adjacent vertices.

```bash
/home/mikeb/theory2/.venv/bin/theory --json combinatorics independent-set \
  --edges="[[0,1],[1,2],[2,3]]" --method=approx

# Methods: approx, greedy, exact
```

**Output**:
```json
{
  "status": "success",
  "result": {
    "independent_set": [0, 2],
    "set_size": 2,
    "method": "approx"
  }
}
```

### Graph Matching

Find maximum matching (largest set of non-adjacent edges).

```bash
/home/mikeb/theory2/.venv/bin/theory --json combinatorics graph-matching \
  --edges="[[0,1],[1,2],[2,3],[3,4]]" --maximal

# Use --no-maximal for minimal matching
```

**Output**:
```json
{
  "status": "success",
  "result": {
    "matching_edges": [[0, 1], [2, 3]],
    "matching_size": 2
  }
}
```

## Argument Parsing

Parse user arguments to determine the operation:

1. **create-graph** or **graph create**: Create graph from edges or named graph
2. **analyze-graph** or **graph analyze**: Comprehensive graph analysis
3. **find-paths** or **paths**: Find paths between nodes
4. **graph-coloring** or **coloring**: Color graph vertices
5. **count**: Combinatorial counting (permutations, combinations, catalan, bell, stirling, etc.)
6. **tsp**: Traveling Salesman Problem
7. **knapsack**: 0/1 Knapsack optimization
8. **vertex-cover**: Minimum vertex cover
9. **independent-set**: Maximum independent set
10. **graph-matching** or **matching**: Maximum graph matching

Always use `--json` flag for structured output.

## Common Patterns

### Graph Analysis Workflow
```bash
# 1. Create and analyze
theory --json combinatorics create-graph --named-graph=petersen --analyze

# 2. Find shortest paths
theory --json combinatorics find-paths --edges="..." --source=0 --target=5

# 3. Color the graph
theory --json combinatorics graph-coloring --edges="..."
```

### Optimization Workflow
```bash
# 1. Solve TSP
theory --json combinatorics tsp --distances="[[...]]" --method=greedy

# 2. Compare with other methods
theory --json combinatorics tsp --distances="[[...]]" --method=christofides

# 3. Find vertex cover
theory --json combinatorics vertex-cover --edges="[[...]]" --method=approx
```

### Counting Workflow
```bash
# 1. Count permutations
theory --json combinatorics count --type=permutations --n=10 --k=3

# 2. Count combinations
theory --json combinatorics count --type=combinations --n=10 --k=3

# 3. Count special numbers
theory --json combinatorics count --type=catalan --n=10 --explain
theory --json combinatorics count --type=bell --n=10 --explain
```

## Error Handling

All errors return structured JSON:
```json
{
  "status": "error",
  "error": {
    "type": "ImportError",
    "message": "No module named 'networkx'",
    "suggestions": [
      "Install NetworkX: uv pip install networkx"
    ]
  }
}
```

## Dependencies

- **NetworkX**: Graph algorithms and data structures
- **theory2.combinatorics**: Custom enumeration and optimization
- **Standard library**: math, itertools for counting operations
