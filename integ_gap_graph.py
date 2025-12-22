import pandas as pd
import matplotlib.pyplot as plt
import os

# Configuration
CSV_FILE = "results.csv"
OUTPUT_IMAGE = "gap_mtz_analysis.png"

# Color mapping for instance types
TYPE_COLORS = {
    'circle': '#2ca02c',  # Green
    'line': '#d62728',  # Red
    'eucl': '#1f77b4',  # Blue
    'rand': '#ff7f0e'  # Orange
}


def get_instance_type(name):
    """Extracts 'circle', 'line', etc. from the short name."""
    for key in TYPE_COLORS:
        if key in name:
            return key
    return 'other'


def clean_instance_name(name):
    name = name.replace("instance_", "").replace(".txt", "")
    name = name.replace("euclidean", "eucl").replace("random", "rand")
    return name


def generate_chart():
    if not os.path.exists(CSV_FILE):
        print(f"Error: {CSV_FILE} not found.")
        return

    # 1. Load Data
    try:
        df = pd.read_csv(CSV_FILE)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    # 2. Filter for MTZ ONLY
    df = df[df['formulation'] == 'MTZ'].copy()

    # Process numeric gap
    df['gap'] = pd.to_numeric(df['gap'], errors='coerce')
    df = df.dropna(subset=['gap'])
    df['gap_percent'] = df['gap'] * 100

    # Process Names and Types
    df['short_name'] = df['instance'].apply(clean_instance_name)
    df['type'] = df['short_name'].apply(get_instance_type)

    # Assign colors based on type
    df['color'] = df['type'].map(TYPE_COLORS)

    # Sort by gap to make the chart readable (Highest gap first)
    # Or sort by name if you prefer consistent ordering
    df = df.sort_values(by='short_name')

    # 3. Plotting
    plt.figure(figsize=(14, 7))

    bars = plt.bar(df['short_name'], df['gap_percent'], color=df['color'])

    # 4. Styling
    plt.title('MTZ Formulation Weakness: Integrality Gap by Instance Type', fontsize=16)
    plt.ylabel('Integrality Gap (%)', fontsize=14)
    plt.xlabel('Instance', fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    # 5. Add Legend for Colors
    # Create dummy handles for the legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=TYPE_COLORS[t], label=t) for t in TYPE_COLORS]
    plt.legend(handles=legend_elements, title="Topology", fontsize=12)

    # 6. Add value labels on top
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height + 0.5,
                 f'{height:.1f}%',
                 ha='center', va='bottom', fontsize=9, rotation=0)

    plt.tight_layout()
    plt.savefig(OUTPUT_IMAGE, dpi=300)
    print(f"Chart saved to {OUTPUT_IMAGE}")
    plt.show()


if __name__ == "__main__":
    generate_chart()