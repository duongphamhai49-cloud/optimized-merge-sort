import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==============================================================================
# RIGID ACADEMIC PUBLICATION STYLE CONFIGURATION: STRICT BLACK & WHITE / GRAYSCALE
# ==============================================================================
plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.edgecolor': 'black',
    'axes.linewidth': 1.2,
    'axes.titlesize': 12,
    'axes.titleweight': 'bold',
    'axes.labelsize': 11,
    'axes.labelweight': 'bold',
    'axes.labelcolor': 'black',
    'xtick.color': 'black',
    'ytick.color': 'black',
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'legend.fontsize': 9,
    'legend.frameon': True,
    'legend.edgecolor': 'black',
    'legend.facecolor': 'white',
    'legend.fancybox': False,
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif', 'Liberation Serif', 'Cambria'],
    'lines.linewidth': 1.5,
    'grid.color': '#cccccc',
    'grid.linestyle': ':',
    'grid.linewidth': 0.8,
    'grid.alpha': 0.8,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.facecolor': 'white'
})

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    results_dir = os.path.join(base_dir, 'data', 'results')
    figures_dir = os.path.join(base_dir, 'report', 'figures')
    os.makedirs(figures_dir, exist_ok=True)

    summary_path = os.path.join(results_dir, 'summary_statistics.csv')
    raw_path = os.path.join(results_dir, 'raw_benchmark_results.csv')

    if not os.path.exists(summary_path):
        print(f"Error: {summary_path} not found!")
        return

    df = pd.read_csv(summary_path)
    df_raw = pd.read_csv(raw_path) if os.path.exists(raw_path) else None

    print(f"Loaded summary data with {len(df)} records.")
    
    # Generate Figures
    plot_fig1_cutoff_vs_time(df, figures_dir)
    plot_fig2_size_vs_time(df, figures_dir)
    plot_fig3_standard_vs_optimized(df, figures_dir)
    plot_fig4_distribution_comparison(df, figures_dir)

    # Generate Statistical Analysis Report Table
    generate_statistical_summary_tables(df, df_raw, results_dir)

def plot_fig1_cutoff_vs_time(df, out_dir):
    """
    Figure 1: Execution Time (ms) vs Cutoff Threshold for Random Distribution
    across medium to large sizes (N = 100k, 500k, 1M).
    """
    fig, ax = plt.subplots(figsize=(7, 4.5))

    target_sizes = [100_000, 500_000, 1_000_000]
    styles = [
        {'marker': 's', 'linestyle': '-', 'color': '#000000', 'label': 'N = 100,000 (ms x10)'},
        {'marker': '^', 'linestyle': '--', 'color': '#333333', 'label': 'N = 500,000 (ms x2)'},
        {'marker': 'o', 'linestyle': '-.', 'color': '#555555', 'label': 'N = 1,000,000 (ms)'}
    ]

    for size, style in zip(target_sizes, styles):
        sub = df[(df['Distribution'] == 'RANDOM') & 
                 (df['Algorithm'] == 'OptimizedMergeSort') & 
                 (df['Size'] == size)].sort_values('Cutoff')
        
        if sub.empty:
            continue

        scale = 1.0
        if size == 100_000:
            scale = 10.0
        elif size == 500_000:
            scale = 2.0

        cutoffs = sub['Cutoff'].values
        means = sub['MeanMs'].values * scale
        std = sub['StdDevMs'].values * scale

        ax.errorbar(cutoffs, means, yerr=std,
                    fmt=style['marker'] + style['linestyle'],
                    color=style['color'],
                    label=style['label'],
                    capsize=3, capthick=1.0, elinewidth=1.0, markersize=5)

    # Annotate optimal cutoff region
    ax.axvspan(7, 16, color='#eeeeee', alpha=0.8, zorder=0, label='Optimal Cutoff Zone [7..16]')

    ax.set_xlabel('Cutoff Threshold to Insertion Sort (Subarray Length)')
    ax.set_ylabel('Execution Time (Normalized ms with Error Bars)')
    ax.set_title('Figure 1: Execution Time vs. Cutoff Threshold (Random Distribution)')
    ax.set_xticks([1, 2, 4, 6, 7, 8, 10, 12, 16, 20, 24, 32, 48, 64])
    ax.grid(True)
    ax.legend(loc='upper right')

    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, 'fig1_cutoff_vs_time.png'))
    fig.savefig(os.path.join(out_dir, 'fig1_cutoff_vs_time.svg'))
    plt.close(fig)
    print("Generated Fig 1: Cutoff vs Execution Time.")

def plot_fig2_size_vs_time(df, out_dir):
    """
    Figure 2: Execution Time vs Input Size N (Log-Log Scale)
    Demonstrating empirical O(N log N) scaling.
    """
    fig, ax = plt.subplots(figsize=(7, 4.5))

    # Standard Merge
    std_data = df[(df['Distribution'] == 'RANDOM') & 
                  (df['Algorithm'] == 'StandardMergeSort')].sort_values('Size')
    # Cutoff 7
    opt7_data = df[(df['Distribution'] == 'RANDOM') & 
                   (df['Algorithm'] == 'OptimizedMergeSort') & 
                   (df['Cutoff'] == 7)].sort_values('Size')
    # Cutoff 10
    opt10_data = df[(df['Distribution'] == 'RANDOM') & 
                    (df['Algorithm'] == 'OptimizedMergeSort') & 
                    (df['Cutoff'] == 10)].sort_values('Size')
    # Cutoff 16
    opt16_data = df[(df['Distribution'] == 'RANDOM') & 
                    (df['Algorithm'] == 'OptimizedMergeSort') & 
                    (df['Cutoff'] == 16)].sort_values('Size')

    if not std_data.empty:
        ax.plot(std_data['Size'], std_data['MeanMs'],
                marker='x', linestyle=':', color='#000000', label='Standard MergeSort', markersize=6)
    if not opt7_data.empty:
        ax.plot(opt7_data['Size'], opt7_data['MeanMs'],
                marker='s', linestyle='--', color='#444444', label='Optimized (Cutoff = 7)', markersize=5)
    if not opt10_data.empty:
        ax.plot(opt10_data['Size'], opt10_data['MeanMs'],
                marker='o', linestyle='-', color='#000000', label='Optimized (Cutoff = 10)', markersize=5)
    if not opt16_data.empty:
        ax.plot(opt16_data['Size'], opt16_data['MeanMs'],
                marker='^', linestyle='-.', color='#666666', label='Optimized (Cutoff = 16)', markersize=5)

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Input Size N (elements)')
    ax.set_ylabel('Mean Execution Time (ms)')
    ax.set_title('Figure 2: Execution Time vs. Input Size N (Log-Log Scale)')
    ax.grid(True, which='both')
    ax.legend(loc='upper left')

    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, 'fig2_size_vs_time.png'))
    fig.savefig(os.path.join(out_dir, 'fig2_size_vs_time.svg'))
    plt.close(fig)
    print("Generated Fig 2: Size vs Execution Time.")

def plot_fig3_standard_vs_optimized(df, out_dir):
    """
    Figure 3: Direct Performance Speedup Ratio (%) of Optimized (Cutoff=10)
    over Standard MergeSort across all sizes for Random data.
    """
    fig, ax = plt.subplots(figsize=(7, 4.5))

    std_df = df[(df['Distribution'] == 'RANDOM') & (df['Algorithm'] == 'StandardMergeSort')].set_index('Size')
    opt_df = df[(df['Distribution'] == 'RANDOM') & (df['Algorithm'] == 'OptimizedMergeSort') & (df['Cutoff'] == 10)].set_index('Size')

    common_sizes = [s for s in [1000, 10000, 100000, 500000, 1000000] if s in std_df.index and s in opt_df.index]

    std_times = [std_df.loc[s, 'MeanMs'] for s in common_sizes]
    opt_times = [opt_df.loc[s, 'MeanMs'] for s in common_sizes]
    pct_improvements = [((st - op) / st) * 100.0 for st, op in zip(std_times, opt_times)]

    x = np.arange(len(common_sizes))
    width = 0.55

    bars = ax.bar(x, pct_improvements, width, color='#555555', edgecolor='black', linewidth=1.2)

    min_val = min(pct_improvements)
    max_val = max(pct_improvements)
    ax.set_ylim(min(-6, min_val - 4), max(35, max_val + 4))

    for bar, val in zip(bars, pct_improvements):
        if val >= 0:
            y_pos = bar.get_height() + 0.8
            va = 'bottom'
        else:
            y_pos = bar.get_height() - 2.2
            va = 'top'
        ax.text(bar.get_x() + bar.get_width() / 2.0, y_pos,
                f"{val:+.1f}%", ha='center', va=va,
                fontsize=9, fontweight='bold')

    ax.axhline(0, color='black', linewidth=1.0)
    ax.set_xticks(x)
    ax.set_xticklabels([f"N = {s:,}" for s in common_sizes])
    ax.set_ylabel('Execution Time Reduction (%)')
    ax.set_title('Figure 3: Optimization Gain of Optimized MergeSort (Cutoff = 10) vs. Standard Baseline')
    ax.grid(True, axis='y')

    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, 'fig3_standard_vs_optimized.png'))
    fig.savefig(os.path.join(out_dir, 'fig3_standard_vs_optimized.svg'))
    plt.close(fig)
    print("Generated Fig 3: Standard vs Optimized Speedup.")

def plot_fig4_distribution_comparison(df, out_dir):
    """
    Figure 4: Comparative Execution Times across Input Distributions
    at N = 500,000 for Standard MergeSort vs Cutoff = 7, 10, 16.
    """
    fig, ax = plt.subplots(figsize=(7.5, 4.5))

    target_size = 500_000
    if target_size not in df['Size'].values:
        target_size = df['Size'].max()

    distributions = ['RANDOM', 'SORTED', 'REVERSED', 'DUPLICATES']
    labels = ['Random', 'Sorted', 'Reversed', 'Duplicates']

    data_std = []
    data_c7 = []
    data_c10 = []
    data_c16 = []

    for dist in distributions:
        s = df[(df['Size'] == target_size) & (df['Distribution'] == dist)]
        
        std_val = s[s['Algorithm'] == 'StandardMergeSort']['MeanMs'].values
        c7_val = s[(s['Algorithm'] == 'OptimizedMergeSort') & (s['Cutoff'] == 7)]['MeanMs'].values
        c10_val = s[(s['Algorithm'] == 'OptimizedMergeSort') & (s['Cutoff'] == 10)]['MeanMs'].values
        c16_val = s[(s['Algorithm'] == 'OptimizedMergeSort') & (s['Cutoff'] == 16)]['MeanMs'].values

        data_std.append(std_val[0] if len(std_val) > 0 else 0)
        data_c7.append(c7_val[0] if len(c7_val) > 0 else 0)
        data_c10.append(c10_val[0] if len(c10_val) > 0 else 0)
        data_c16.append(c16_val[0] if len(c16_val) > 0 else 0)

    x = np.arange(len(distributions))
    width = 0.2

    ax.bar(x - 1.5 * width, data_std, width, label='Standard Merge', color='#ffffff', edgecolor='black', hatch='//')
    ax.bar(x - 0.5 * width, data_c7, width, label='Cutoff = 7', color='#cccccc', edgecolor='black')
    ax.bar(x + 0.5 * width, data_c10, width, label='Cutoff = 10', color='#777777', edgecolor='black')
    ax.bar(x + 1.5 * width, data_c16, width, label='Cutoff = 16', color='#222222', edgecolor='black')

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel(f'Mean Execution Time (ms) at N = {target_size:,}')
    ax.set_title(f'Figure 4: Performance Across Data Distributions (N = {target_size:,})')
    ax.legend(loc='upper right')
    ax.grid(True, axis='y')

    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, 'fig4_distribution_comparison.png'))
    fig.savefig(os.path.join(out_dir, 'fig4_distribution_comparison.svg'))
    plt.close(fig)
    print("Generated Fig 4: Performance across distributions.")

def generate_statistical_summary_tables(df, df_raw, results_dir):
    """
    Computes comprehensive statistical tables and writes analysis summaries.
    """
    analysis_file = os.path.join(results_dir, 'detailed_statistical_analysis.md')
    with open(analysis_file, 'w', encoding='utf-8') as f:
        f.write("# Detailed Statistical Analysis of Merge Sort Optimization Experiments\n\n")
        f.write("## 1. Overview of Experimental Conditions\n")
        f.write(f"- Total configurations: {len(df)}\n")
        if df_raw is not None:
            f.write(f"- Total raw timed trials: {len(df_raw)}\n")
        f.write("\n## 2. Optimal Cutoff Identification by Input Size (Random Distribution)\n\n")
        f.write("| Input Size (N) | Standard Merge (ms) | Best Cutoff | Best Mean Time (ms) | Cutoff 7 (ms) | Cutoff 10 (ms) | Max Improvement (%) |\n")
        f.write("|:---:|:---:|:---:|:---:|:---:|:---:|:---:|\n")

        for size in [1_000, 10_000, 100_000, 500_000, 1_000_000]:
            sub_std = df[(df['Distribution'] == 'RANDOM') & (df['Algorithm'] == 'StandardMergeSort') & (df['Size'] == size)]
            sub_opt = df[(df['Distribution'] == 'RANDOM') & (df['Algorithm'] == 'OptimizedMergeSort') & (df['Size'] == size)]

            if sub_std.empty or sub_opt.empty:
                continue

            std_mean = sub_std['MeanMs'].values[0]
            best_row = sub_opt.loc[sub_opt['MeanMs'].idxmin()]
            best_cutoff = int(best_row['Cutoff'])
            best_mean = best_row['MeanMs']

            c7_row = sub_opt[sub_opt['Cutoff'] == 7]
            c10_row = sub_opt[sub_opt['Cutoff'] == 10]
            c7_mean = c7_row['MeanMs'].values[0] if not c7_row.empty else float('nan')
            c10_mean = c10_row['MeanMs'].values[0] if not c10_row.empty else float('nan')

            gain = ((std_mean - best_mean) / std_mean) * 100.0

            f.write(f"| {size:,} | {std_mean:.4f} | {best_cutoff} | {best_mean:.4f} | {c7_mean:.4f} | {c10_mean:.4f} | {gain:+.2f}% |\n")

        f.write("\n\n## 3. Distribution Impact Analysis (N = 500,000)\n\n")
        f.write("| Distribution | Standard Merge (ms) | Cutoff 7 (ms) | Cutoff 10 (ms) | Optimal Cutoff | Optimal Time (ms) | Gain (%) |\n")
        f.write("|:---:|:---:|:---:|:---:|:---:|:---:|:---:|\n")

        for dist in ['RANDOM', 'SORTED', 'REVERSED', 'DUPLICATES']:
            sub_std = df[(df['Distribution'] == dist) & (df['Algorithm'] == 'StandardMergeSort') & (df['Size'] == 500_000)]
            sub_opt = df[(df['Distribution'] == dist) & (df['Algorithm'] == 'OptimizedMergeSort') & (df['Size'] == 500_000)]

            if sub_std.empty or sub_opt.empty:
                continue

            std_mean = sub_std['MeanMs'].values[0]
            best_row = sub_opt.loc[sub_opt['MeanMs'].idxmin()]
            best_cutoff = int(best_row['Cutoff'])
            best_mean = best_row['MeanMs']

            c7_row = sub_opt[sub_opt['Cutoff'] == 7]
            c10_row = sub_opt[sub_opt['Cutoff'] == 10]
            c7_mean = c7_row['MeanMs'].values[0] if not c7_row.empty else float('nan')
            c10_mean = c10_row['MeanMs'].values[0] if not c10_row.empty else float('nan')

            gain = ((std_mean - best_mean) / std_mean) * 100.0

            f.write(f"| {dist} | {std_mean:.4f} | {c7_mean:.4f} | {c10_mean:.4f} | {best_cutoff} | {best_mean:.4f} | {gain:+.2f}% |\n")

    print(f"Generated detailed statistical analysis table: {analysis_file}")

if __name__ == '__main__':
    main()
