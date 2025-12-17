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
    """Pour n<=10 seulement."""

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

    return value(prob.objective), x, (end_time - start_time)

