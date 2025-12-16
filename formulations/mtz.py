from pulp import *
from .common import create_base_prob
import time


def solve_mtz(n, dist_matrix, relax=False):

    prob, x = create_base_prob(n, dist_matrix, relax)

    # u[i] = position of city i in the tour (1 to n)
    u = LpVariable.dicts("rank",
                         range(n),
                         lowBound=1,
                         upBound=n,
                         cat='Integer')

    # Fix u[0] = 1
    prob += u[0] == 1

    # Miller-Tucker-Zemlin subtour elimination constraints
    # If we go from i to j, then u[j] must be greater than u[i]
    for i in range(0, n):
        for j in range(1, n):  # Skip city 0
            if i != j:
                prob += u[j] >= u[i] + 1 - n * (1 - x[i, j])

    # 4. Solve and Time
    start_time = time.time()
    prob.solve()
    end_time = time.time()

    return value(prob.objective), x, (end_time - start_time)