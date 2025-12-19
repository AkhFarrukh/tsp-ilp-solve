import os
import csv
from utils.data_loader import read_instance
from formulations.mtz import solve_mtz
from formulations.dfj import solve_dfj_enum, solve_dfj_iter
#todo do not return this file

# Configuration
# "." means the current directory where this script is located
INSTANCES_DIR = "."
OUTPUT_FILE = "results.csv"

def calculate_gap(obj_int, obj_relax):
    if obj_relax is None:
        return ""
    try:
        return (obj_int - obj_relax) / obj_int
    except ZeroDivisionError:
        return 0.0

def run_benchmark():
    # Prepare CSV file with headers
    headers = [
        "instance", "formulation", "obj_int", "time_int",
        "obj_relax", "time_relax", "gap", "vars", "constr"
    ]

    # Get list of all instance files
    files = [f for f in os.listdir(INSTANCES_DIR) if f.endswith(".txt")]
    files.sort()

    if not files:
        print(f"No .txt files found in {os.path.abspath(INSTANCES_DIR)}")
        return

    with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

        for filename in files:
            print(f"Processing {filename}...")
            filepath = os.path.join(INSTANCES_DIR, filename)

            # Load Data
            n, coords, dist_matrix = read_instance(filepath)

            # ==========================================
            # 1. MTZ Formulation
            # ==========================================
            try:
                # Integer Run
                obj_int, _, prob_int, time_int = solve_mtz(n, dist_matrix, relax=False)

                # Relaxed Run
                obj_rel, _, _, time_rel = solve_mtz(n, dist_matrix, relax=True)

                # Stats
                gap = calculate_gap(obj_int, obj_rel)
                num_vars = prob_int.numVariables()
                num_constrs = prob_int.numConstraints()

                writer.writerow([
                    filename, "MTZ",
                    f"{obj_int:.2f}", f"{time_int:.4f}",
                    f"{obj_rel:.2f}", f"{time_rel:.4f}",
                    f"{gap:.4f}", num_vars, num_constrs
                ])
                print(f"  > MTZ Done (Time: {time_int:.2f}s)")

            except Exception as e:
                print(f"  ! Error in MTZ for {filename}: {e}")

            # ==========================================
            # 2. DFJ Enumerative (Only if n <= 15)
            # ==========================================
            if n <= 15:
                try:
                    # Integer Run
                    obj_int, _, prob_int, time_int = solve_dfj_enum(n, dist_matrix, relax=False)

                    # Relaxed Run
                    obj_rel, _, _, time_rel = solve_dfj_enum(n, dist_matrix, relax=True)

                    # Stats
                    gap = calculate_gap(obj_int, obj_rel)
                    num_vars = prob_int.numVariables()
                    num_constrs = prob_int.numConstraints()

                    writer.writerow([
                        filename, "DFJ_enum",
                        f"{obj_int:.2f}", f"{time_int:.4f}",
                        f"{obj_rel:.2f}", f"{time_rel:.4f}",
                        f"{gap:.4f}", num_vars, num_constrs
                    ])
                    print(f"  > DFJ Enum Done (Time: {time_int:.2f}s)")
                except Exception as e:
                    print(f"  ! Error in DFJ Enum for {filename}: {e}")
            else:
                print(f"  > Skipping DFJ Enum (n={n} > 15)")

            # ==========================================
            # 3. DFJ Iterative (Always Run)
            # ==========================================
            try:
                # Integer Run Only (Relaxation not required/possible for Iterative)
                obj_int, _, prob_int, time_int, iters = solve_dfj_iter(n, dist_matrix)

                # Stats
                num_vars = prob_int.numVariables()
                num_constrs = prob_int.numConstraints()

                writer.writerow([
                    filename, "DFJ_iter",
                    f"{obj_int:.2f}", f"{time_int:.4f}",
                    "", "",  # No relaxation for iterative
                    "",  # No gap
                    num_vars, num_constrs
                ])
                print(f"  > DFJ Iter Done (Time: {time_int:.2f}s, Iters: {iters})")
            except Exception as e:
                print(f"  ! Error in DFJ Iter for {filename}: {e}")

            # Flush to disk immediately in case of crash
            csvfile.flush()

    print(f"\nBenchmark finished. Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    run_benchmark()