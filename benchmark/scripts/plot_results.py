import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==============================================================================
# ĐỊNH DẠNG ĐỒ HỌA HỌC THUẬT: ĐƠN SẮC / THANG ĐỘ XÁM (STRICT BLACK & WHITE)
# HỖ TRỢ TIẾNG VIỆT UNICODE (TIMES NEW ROMAN)
# ==============================================================================
plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.edgecolor': 'black',
    'axes.linewidth': 1.2,
    'axes.titlesize': 11.5,
    'axes.titleweight': 'bold',
    'axes.labelsize': 10.5,
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
    'font.family': 'Times New Roman',
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
        print(f"Lỗi: Không tìm thấy {summary_path}!")
        return

    df = pd.read_csv(summary_path)
    df_raw = pd.read_csv(raw_path) if os.path.exists(raw_path) else None

    print(f"Đã tải dữ liệu thống kê với {len(df)} cấu hình.")
    
    # Xuất các biểu đồ tiếng Việt
    plot_fig1_cutoff_vs_time(df, figures_dir)
    plot_fig2_size_vs_time(df, figures_dir)
    plot_fig3_standard_vs_optimized(df, figures_dir)
    plot_fig4_distribution_comparison(df, figures_dir)

    # Xuất bảng phân tích thống kê tiếng Việt
    generate_statistical_summary_tables(df, df_raw, results_dir)

def plot_fig1_cutoff_vs_time(df, out_dir):
    """
    Hình 1: Tương quan giữa Ngưỡng Cutoff và Thời gian Thực thi (Dữ liệu ngẫu nhiên)
    """
    fig, ax = plt.subplots(figsize=(7, 4.5))

    target_sizes = [100_000, 500_000, 1_000_000]
    styles = [
        {'marker': 's', 'linestyle': '-', 'color': '#000000', 'label': 'N = 100.000 (ms x10)'},
        {'marker': '^', 'linestyle': '--', 'color': '#333333', 'label': 'N = 500.000 (ms x2)'},
        {'marker': 'o', 'linestyle': '-.', 'color': '#555555', 'label': 'N = 1.000.000 (ms)'}
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

    ax.axvspan(7, 16, color='#eeeeee', alpha=0.8, zorder=0, label='Vùng Cutoff tối ưu [7..16]')

    ax.set_xlabel('Ngưỡng Cutoff chuyển sang Insertion Sort (Độ dài đoạn con)')
    ax.set_ylabel('Thời gian thực thi (ms chuẩn hóa có thanh sai số)')
    ax.set_title('Hình 1: Tương Quan Giữa Ngưỡng Cutoff và Thời Gian Thực Thi (Dữ Liệu Ngẫu Nhiên)')
    ax.set_xticks([1, 2, 4, 6, 7, 8, 10, 12, 16, 20, 24, 32, 48, 64])
    ax.grid(True)
    ax.legend(loc='upper right')

    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, 'fig1_cutoff_vs_time.png'))
    fig.savefig(os.path.join(out_dir, 'fig1_cutoff_vs_time.svg'))
    plt.close(fig)
    print("Đã tạo Hình 1: Cutoff vs Thời gian thực thi.")

def plot_fig2_size_vs_time(df, out_dir):
    """
    Hình 2: Quy luật mở rộng thời gian theo kích thước mảng N (Log-Log Scale)
    """
    fig, ax = plt.subplots(figsize=(7, 4.5))

    std_data = df[(df['Distribution'] == 'RANDOM') & 
                  (df['Algorithm'] == 'StandardMergeSort')].sort_values('Size')
    opt7_data = df[(df['Distribution'] == 'RANDOM') & 
                   (df['Algorithm'] == 'OptimizedMergeSort') & 
                   (df['Cutoff'] == 7)].sort_values('Size')
    opt10_data = df[(df['Distribution'] == 'RANDOM') & 
                    (df['Algorithm'] == 'OptimizedMergeSort') & 
                    (df['Cutoff'] == 10)].sort_values('Size')
    opt16_data = df[(df['Distribution'] == 'RANDOM') & 
                    (df['Algorithm'] == 'OptimizedMergeSort') & 
                    (df['Cutoff'] == 16)].sort_values('Size')

    if not std_data.empty:
        ax.plot(std_data['Size'], std_data['MeanMs'],
                marker='x', linestyle=':', color='#000000', label='MergeSort chuẩn', markersize=6)
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
    ax.set_xlabel('Kích thước mảng N (phần tử)')
    ax.set_ylabel('Thời gian thực thi trung bình (ms)')
    ax.set_title('Hình 2: Quy Luật Mở Rộng Thời Gian Theo Kích Thước N (Thang Log-Log)')
    ax.grid(True, which='both')
    ax.legend(loc='upper left')

    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, 'fig2_size_vs_time.png'))
    fig.savefig(os.path.join(out_dir, 'fig2_size_vs_time.svg'))
    plt.close(fig)
    print("Đã tạo Hình 2: Kích thước N vs Thời gian.")

def plot_fig3_standard_vs_optimized(df, out_dir):
    """
    Hình 3: Tỷ lệ giảm thời gian thực thi của Optimized MergeSort (Cutoff = 10) so với bản chuẩn
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
    ax.set_ylim(min(-6, min_val - 4), max(36, max_val + 4))

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
    ax.set_ylabel('Tỷ lệ giảm thời gian thực thi (%)')
    ax.set_title('Hình 3: Mức Cải Thiện của Optimized MergeSort (Cutoff = 10) So Với Bản Chuẩn')
    ax.grid(True, axis='y')

    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, 'fig3_standard_vs_optimized.png'))
    fig.savefig(os.path.join(out_dir, 'fig3_standard_vs_optimized.svg'))
    plt.close(fig)
    print("Đã tạo Hình 3: Mức tăng tốc so với chuẩn.")

def plot_fig4_distribution_comparison(df, out_dir):
    """
    Hình 4: Hiệu năng theo các dạng phân bố dữ liệu tại N = 500.000
    """
    fig, ax = plt.subplots(figsize=(7.5, 4.5))

    target_size = 500_000
    if target_size not in df['Size'].values:
        target_size = df['Size'].max()

    distributions = ['RANDOM', 'SORTED', 'REVERSED', 'DUPLICATES']
    labels = ['Ngẫu nhiên', 'Đã sắp xếp', 'Nghịch đảo', 'Trùng lặp']

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

    ax.bar(x - 1.5 * width, data_std, width, label='MergeSort chuẩn', color='#ffffff', edgecolor='black', hatch='//')
    ax.bar(x - 0.5 * width, data_c7, width, label='Cutoff = 7', color='#cccccc', edgecolor='black')
    ax.bar(x + 0.5 * width, data_c10, width, label='Cutoff = 10', color='#777777', edgecolor='black')
    ax.bar(x + 1.5 * width, data_c16, width, label='Cutoff = 16', color='#222222', edgecolor='black')

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel(f'Thời gian thực thi trung bình (ms) tại N = {target_size:,}')
    ax.set_title(f'Hình 4: Hiệu Năng Theo Các Dạng Phân Bố Dữ Liệu (N = {target_size:,})')
    ax.legend(loc='upper right')
    ax.grid(True, axis='y')

    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, 'fig4_distribution_comparison.png'))
    fig.savefig(os.path.join(out_dir, 'fig4_distribution_comparison.svg'))
    plt.close(fig)
    print("Đã tạo Hình 4: So sánh phân bố dữ liệu.")

def generate_statistical_summary_tables(df, df_raw, results_dir):
    """
    Xuất bảng tổng hợp phân tích thống kê chi tiết bằng tiếng Việt.
    """
    analysis_file = os.path.join(results_dir, 'detailed_statistical_analysis.md')
    with open(analysis_file, 'w', encoding='utf-8') as f:
        f.write("# Báo Cáo Phân Tích Thống Kê Chi Tiết Thực Nghiệm MergeSort Cutoff\n\n")
        f.write("## 1. Tổng Quan Điều Kiện Thực Nghiệm\n")
        f.write(f"- Tổng số cấu hình đo lường: {len(df)}\n")
        if df_raw is not None:
            f.write(f"- Tổng số lượt chạy đo đạc thời gian thực tế: {len(df_raw)}\n")
        f.write("\n## 2. Xác Định Ngưỡng Cutoff Tối Ưu Theo Quy Mô Mảng (Dữ Liệu Ngẫu Nhiên)\n\n")
        f.write("| Kích thước mảng (N) | MergeSort chuẩn (ms) | Cutoff Tối ưu | Thời gian tối ưu (ms) | Cutoff = 7 (ms) | Cutoff = 10 (ms) | Mức cải thiện (%) |\n")
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

        f.write("\n\n## 3. Đánh Giá Ảnh Hưởng Của Phân Bố Dữ Liệu (N = 500.000)\n\n")
        f.write("| Phân bố dữ liệu | MergeSort chuẩn (ms) | Cutoff = 7 (ms) | Cutoff = 10 (ms) | Cutoff Tối ưu | Thời gian tối ưu (ms) | Tỷ lệ cải thiện (%) |\n")
        f.write("|:---:|:---:|:---:|:---:|:---:|:---:|:---:|\n")

        for dist, name in [('RANDOM', 'Ngẫu nhiên (Random)'), ('SORTED', 'Đã sắp xếp (Sorted)'), ('REVERSED', 'Nghịch đảo (Reversed)'), ('DUPLICATES', 'Trùng lặp (Duplicates)')]:
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

            f.write(f"| {name} | {std_mean:.4f} | {c7_mean:.4f} | {c10_mean:.4f} | {best_cutoff} | {best_mean:.4f} | {gain:+.2f}% |\n")

    print(f"Đã cập nhật bảng phân tích chi tiết tiếng Việt: {analysis_file}")

if __name__ == '__main__':
    main()
