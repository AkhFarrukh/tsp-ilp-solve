import os
import csv
import time
from utils.data_loader import read_instance
from formulations.dfj import solve_dfj_iter, solve_dfj_iter_bonus

# Configuration
INSTANCES_DIR = "."  # Or "instances" if in a subfolder
OUTPUT_FILE = "bonus.csv"


def run_bonus_benchmark():
    # Prepare CSV file with headers
    headers = [
        "instance",
        "time_standard", "iters_standard",
        "time_bonus", "iters_bonus",
        "time_diff", "iters_diff"
    ]

    # Get list of all instance files
    files = [f for f in os.listdir(INSTANCES_DIR) if f.endswith(".txt")]
    files.sort()

    if not files:
        print(f"No .txt files found in {os.path.abspath(INSTANCES_DIR)}")
        return

    print(f"Starting Bonus Benchmark on {len(files)} instances...")

    with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

        for filename in files:
            print(f"Processing {filename}...")
            filepath = os.path.join(INSTANCES_DIR, filename)

            # Load Data
            n, coords, dist_matrix = read_instance(filepath)

            try:
                # 1. Run Standard DFJ Iterative
                _, _, _, time_std, iters_std = solve_dfj_iter(n, dist_matrix)

                # 2. Run Bonus DFJ Iterative (One constraint for 2 subtours)
                _, _, _, time_bonus, iters_bonus = solve_dfj_iter_bonus(n, dist_matrix)

                # Calculate differences
                time_diff = time_bonus - time_std
                iters_diff = iters_bonus - iters_std

                # Write results
                writer.writerow([
                    filename,
                    f"{time_std:.4f}", iters_std,
                    f"{time_bonus:.4f}", iters_bonus,
                    f"{time_diff:.4f}", iters_diff
                ])

                print(f"  > Done. Standard: {iters_std} iters, Bonus: {iters_bonus} iters")

            except Exception as e:
                print(f"  ! Error processing {filename}: {e}")

            # Flush to disk to save progress
            csvfile.flush()

    print(f"\nBonus benchmark finished. Results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    run_bonus_benchmark()