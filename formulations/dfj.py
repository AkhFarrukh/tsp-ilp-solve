from pulp import *
from .common import create_base_prob
import time


def generate_subsets(n):
    # todo if lagse, use bitmasking
    subsets = [[]]

    for city in range(n):
        new_subsets = []

        for s in subsets:
            new_subsets.append(s + [city])
        subsets.extend(new_subsets)

    return subsets


def solve_dfj_enum(n, dist_matrix, relax=False):

    prob, x = create_base_prob(n, dist_matrix, relax)
    subsets = generate_subsets(n)

    # Contraints
    for S in subsets:
        # Subset must have at least 2 cities, but strictly less than n
        if 2 <= len(S) < n:
            # Add constraint: sum of edges inside S <= |S| - 1
            prob += lpSum(x[i, j]
                          for i in S
                          for j in S
                          if i != j) <= len(S) - 1

    start_time = time.time()
    prob.solve()
    end_time = time.time()

    return value(prob.objective), x, prob, (end_time - start_time)


def find_subtours(n, active_edges):
    """
    Given a list of active edges [(i, j), ...], returns a list of cycles.
    Example:
    Input: [(0,1), (1,2), (2,0), (3,4), (4,3)]
    Output: [[0, 1, 2], [3, 4]]
    """
    # Build adjacency list (dict)
    adj = {i: [] for i in range(n)}
    for u, v in active_edges:
        adj[u].append(v)

    visited = set()
    subtours = []

    #  Find connected components (cycles)
    for i in range(n):
        if i not in visited:
            cycle = []
            current = i
            while current not in visited:
                visited.add(current)
                cycle.append(current)
                neighbors = adj[current]
                if not neighbors:
                    break # No outgoing edges
                current = neighbors[0]  # Follow the path
            subtours.append(cycle)

    return subtours


def solve_dfj_iter(n, dist_matrix):
    prob, x = create_base_prob(n, dist_matrix, relax=False)

    total_solve_time = 0
    iterations = 0

    while True:

        # Solve
        t0 = time.time()
        # Suppress output to keep console clean during loop
        prob.solve(PULP_CBC_CMD(msg=0))
        total_solve_time += (time.time() - t0)

        # Extract Solution
        solution = []
        for i in range(n):
            for j in range(n):
                if i != j and value(x[i, j]) > 0.9: # Using 0.9 to avoid floating point issues
                    solution.append((i, j))

        # Detect Cycles
        subtours = find_subtours(n, solution)

        # If a unique subtour covering all cities exists
        if len(subtours) == 1 and len(subtours[0]) == n:
            break

        # For every subtour found, add the constraint: sum(x_ij) <= |S| - 1
        for S in subtours:
            if len(S) < n:
                prob += lpSum(x[i, j]
                              for i in S
                              for j in S
                              if i != j) <= len(S) - 1

        iterations += 1

    return value(prob.objective), x, prob, total_solve_time, iterations
