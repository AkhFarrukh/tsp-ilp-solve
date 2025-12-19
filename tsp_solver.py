import sys
import time
from utils.data_loader import read_instance
from utils.results import get_tour_string
from formulations.mtz import solve_mtz
from formulations.dfj import solve_dfj_enum, solve_dfj_iter

#TODO Utilisez des structures de données efficaces (dictionnaires Python) pour représenter les graphes

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 tsp_solver.py <instance_file> <method_flag>")
        return

    filename = sys.argv[1]
    method_flag = int(sys.argv[2])

    n, coords, dist_matrix = read_instance(filename)

    # Select Method
    # f=0: MTZ, f=1: MTZ Relax, f=2: DFJ Enum, f=3: DFJ Enum Relax, f=4: DFJ Iter
    if method_flag == 0:
        val, x, time_taken = solve_mtz(n, dist_matrix, relax=False)
        print(f"Cycle: {get_tour_string(n, x)}")
    elif method_flag == 1:
        val, x, time_taken = solve_mtz(n, dist_matrix, relax=True)
        #print(f"Cycle: {get_tour_string(n, x)}")
    elif method_flag == 2:
        val, x, time_taken = solve_dfj_enum(n, dist_matrix, relax=False)
        print(f"Cycle: {get_tour_string(n, x)}")
    elif method_flag == 3:
        val, x, time_taken = solve_dfj_enum(n, dist_matrix, relax=True)
        #print(f"Cycle: {get_tour_string(n, x)}")
    elif method_flag == 4:
        val, x, time_taken, iterations = solve_dfj_iter(n, dist_matrix)
        print(f"Cycle: {get_tour_string(n, x)}")
        print(f"Iterations: {iterations}")


    print(f"Objective: {val}")
    print(f"Time: {time_taken}")


if __name__ == "__main__":
    main()