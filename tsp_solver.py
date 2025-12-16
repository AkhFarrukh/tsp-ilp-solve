import sys
import time
from utils.data_loader import read_instance
from utils.results import get_tour_string
from formulations.mtz import solve_mtz


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
        pass
        #val, tour, time_taken, x = solve_mtz(n, dist_matrix, relax=True)
    elif method_flag == 2:
        pass
        #val, tour, time_taken, x = solve_dfj_enum(n, dist_matrix, relax=False)
    elif method_flag == 3:
        pass
        #val, tour, time_taken, x = solve_dfj_enum(n, dist_matrix, relax=True)
    elif method_flag == 4:
        pass
        #val, tour, time_taken, iterations = solve_dfj_iter(n, dist_matrix)


    print(f"Objective: {val}")
    print(f"Time: {time_taken}")


if __name__ == "__main__":
    main()