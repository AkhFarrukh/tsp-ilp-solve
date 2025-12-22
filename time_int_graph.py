import pandas as pd
import matplotlib.pyplot as plt


def plot_tsp_times_optimized(csv_file):
    # 1. Load the data
    df = pd.read_csv(csv_file)
    df['instance'] = df['instance'].str.replace('.txt', '', regex=False)

    # 2. Pivot
    pivot_df = df.pivot(index='instance', columns='formulation', values='time_int')

    # 3. Create the plot
    # Ordering columns for consistency
    cols = [c for c in ['DFJ_enum', 'DFJ_iter', 'MTZ'] if c in pivot_df.columns]
    pivot_df = pivot_df[cols]

    # INCREASED HEIGHT: (width=14, height=10)
    ax = pivot_df.plot(kind='bar', figsize=(14, 10), width=0.8, color=['#1f77b4', '#ff7f0e', '#2ca02c'])

    # --- Y-AXIS LIMIT ---
    Y_LIMIT = 5.3
    plt.ylim(0, Y_LIMIT)

    # 4. Customize the chart
    plt.title('Integer Resolution Time Comparison', fontsize=16, fontweight='bold')
    plt.xlabel('Instance Name', fontsize=13)
    plt.ylabel('Time (seconds)', fontsize=13)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='Method', loc='upper left')

    for p in ax.patches:
        real_val = p.get_height()
        if real_val > 0:
            if real_val > Y_LIMIT:
                # MOVE DOWN: Position slightly below the top edge
                label_y = Y_LIMIT - 0.1
                display_text = f'[{real_val:.2f}s]'
                color = 'white'
                weight = 'bold'
                v_align = 'top'  # Hang the text DOWN from the point
                offset_y = -10  # Push it further down away from the line
            else:
                label_y = real_val
                display_text = f'{real_val:.2f}s'
                color = 'black'
                weight = 'normal'
                v_align = 'bottom'  # Normal text grows UP from the bar
                offset_y = 5  # Standard space above the bar

            ax.annotate(display_text,
                        (p.get_x() + p.get_width() / 2., label_y),
                        ha='center', va=v_align,
                        xytext=(0, offset_y),
                        textcoords='offset points',
                        fontsize=9,
                        color=color,
                        fontweight=weight,
                        rotation=90)

    plt.tight_layout()
    plt.savefig('solving_times.png', dpi=300)
    print("Chart saved as 'solving_times.png'")
    plt.show()


if __name__ == "__main__":
    plot_tsp_times_optimized('results.csv')