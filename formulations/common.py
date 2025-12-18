from pulp import *


def create_base_prob(n, dist_matrix, relax=False):
    """Creates variables, objective, and degree constraints."""
    #TODO add relax later

    # Create the model
    prob = LpProblem("Traveling_Salesman_Problem", LpMinimize)

    if relax:
        var_type = 'Continuous'
    else:
        var_type = 'Binary'


    # Create variables
    # x[i,j] = 1 if we go from city i to city j, 0 otherwise
    x = LpVariable.dicts("edge",
                         ((i, j) for i in range(n) for j in range(n) if i != j),
                         lowBound=0,
                         upBound=1,
                         cat=var_type)



    # Objective: minimize total distance
    prob += lpSum(dist_matrix[i][j] * x[i, j]
                  for i in range(n)
                  for j in range(n)
                  if i != j)

    # Constraint: each city must be visited exactly once (outgoing)
    for i in range(n):
        prob += lpSum(x[i, j] for j in range(n) if i != j) == 1

    # Constraint: each city must be visited exactly once (incoming)
    for j in range(n):
        prob += lpSum(x[i, j] for i in range(n) if i != j) == 1

    return prob, x
