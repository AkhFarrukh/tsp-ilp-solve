# Traveling Salesman Problem (TSP) - Integer Linear Programming Solver

An implementation and comparative benchmark of Integer Linear Programming (ILP) formulations for the Traveling Salesman Problem (TSP) using Python and PuLP.

## Formulations Implemented

1. **Miller-Tucker-Zemlin (MTZ):** Formulates subtour elimination using auxiliary continuous variables, resulting in O(n^2) constraints.
2. **Dantzig-Fulkerson-Johnson (DFJ) - Enumerative:** Formulates subtour elimination by generating all O(2^n) subset constraints a priori.
3. **Dantzig-Fulkerson-Johnson (DFJ) - Iterative:** Solves the problem iteratively by detecting subtours and dynamically adding subtour elimination constraints only when violated.
4. **Continuous Relaxations:** Evaluates linear programming (LP) relaxations to compare bounds and relative integrality gaps.

## Repository Structure

- `tsp_solver.py`: Main CLI tool to execute individual solver runs.
- `formulations/`: Core implementations of MTZ and DFJ models.
- `utils/`: Graph processing, cycle detection, and file parsing utilities.
- `benchmark.py`: Automation script to benchmark models across test instances.
- `results.csv`: Benchmark output containing execution times, objective values, and integrality gaps.
- `*.png`: Generated performance and integrality gap plots.
- `instance_*.txt`: Benchmark problem instances of various topologies (Euclidean, Circle, Line, Random).

## Requirements

Install dependencies using pip:

```bash
pip install pulp matplotlib pandas
```

## Usage

Run `tsp_solver.py` with an instance file and a formulation code:

```bash
python3 tsp_solver.py <instance_file> <formulation_code>
```

### Formulation Codes

- `0`: Solve MTZ (Integer)
- `1`: Solve MTZ Continuous Relaxation
- `2`: Solve DFJ Enumerative (Integer)
- `3`: Solve DFJ Enumerative Continuous Relaxation
- `4`: Solve DFJ Iterative (Integer)

### Example

```bash
python3 tsp_solver.py instance_10_random_sym_1.txt 4
```

### Running Benchmarks

To reproduce full benchmark results and regenerate plots:

```bash
python3 benchmark.py
python3 time_int_graph.py
python3 integ_gap_graph.py
```
