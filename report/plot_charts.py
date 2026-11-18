import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

os.makedirs('report/figures', exist_ok=True)

# Su dung Times New Roman dong bo voi bao cao va ho tro day du tieng Viet co dau
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'font.size': 10,
    'axes.labelsize': 10,
    'figure.dpi': 150,
})

# --- Doc du lieu ---
cutoff_df = pd.read_csv('results/cutoff_results.csv')
summary_df = pd.read_csv('results/summary.csv')

# ==============================================
# Hinh 1: CUTOFF vs Thoi gian (n=100000, random)
# ==============================================
fig, ax = plt.subplots(figsize=(7.8, 4.0))
ax.plot(cutoff_df['cutoff'], cutoff_df['time_ms'], 'o-', color='black', linewidth=1.5, markersize=5)
best_idx = cutoff_df['time_ms'].idxmin()
best_c = int(cutoff_df.loc[best_idx, 'cutoff'])
best_t = cutoff_df.loc[best_idx, 'time_ms']
ax.axvline(x=best_c, color='gray', linestyle='--', linewidth=1)
ax.annotate(f'CUTOFF = {best_c}\n({best_t:.1f} ms)', xy=(best_c, best_t),
            xytext=(best_c + 3, best_t + 1.2), fontsize=9)
ax.set_xlabel('Giá trị CUTOFF')
ax.set_ylabel('Thời gian trung bình (ms)')
ax.grid(True, linestyle=':', alpha=0.6)
fig.tight_layout()
fig.savefig('report/figures/fig1_cutoff_vs_time.png')
plt.close()

# ==============================================
# Hinh 2: Thoi gian vs Kich thuoc mang (random)
# ==============================================
rand_df = summary_df[summary_df['type'] == 'random'].copy().sort_values('size')

fig, ax = plt.subplots(figsize=(7.8, 4.0))
ax.plot(rand_df['size'], rand_df['merge_ms'], 's--', color='black', linewidth=1.5, markersize=5, label='MergeSort')
ax.plot(rand_df['size'], rand_df['optimized_ms'], 'o-', color='dimgray', linewidth=1.5, markersize=5, label='OptimizedMergeSort (CUTOFF = 16)')
ax.set_xlabel('Kích thước mảng (n)')
ax.set_ylabel('Thời gian trung bình (ms)')
ax.legend()
ax.grid(True, linestyle=':', alpha=0.6)
fig.tight_layout()
fig.savefig('report/figures/fig2_size_vs_time.png')
plt.close()

# ==============================================
# Hinh 3: So sanh MergeSort vs Optimized (all sizes, random)
# ==============================================
fig, ax = plt.subplots(figsize=(7.8, 4.0))
x = np.arange(len(rand_df))
w = 0.35
ax.bar(x - w/2, rand_df['merge_ms'], w, label='MergeSort', color='white', edgecolor='black', linewidth=1)
ax.bar(x + w/2, rand_df['optimized_ms'], w, label='OptimizedMergeSort (CUTOFF = 16)', color='lightgray', edgecolor='black', linewidth=1)
ax.set_xticks(x)
ax.set_xticklabels([f'{int(s):,}' for s in rand_df['size']], fontsize=9)
ax.set_xlabel('Kích thước mảng (n)')
ax.set_ylabel('Thời gian trung bình (ms)')
ax.legend()
ax.grid(True, axis='y', linestyle=':', alpha=0.6)
fig.tight_layout()
fig.savefig('report/figures/fig3_comparison.png')
plt.close()

# ==============================================
# Hinh 4: Hieu nang tren 7 kieu du lieu (n=1.000.000)
# ==============================================
large_df = summary_df[summary_df['size'] == 1000000].copy()
type_names = {
    'random': 'Ngẫu nhiên',
    'sorted': 'Đã sắp xếp',
    'reversed': 'Ngược chiều',
    'duplicates': 'Nhiều trùng lặp',
    'partially_sorted_1pct': 'Gần sắp xếp (1%)',
    'partially_sorted_5pct': 'Gần sắp xếp (5%)',
    'partially_sorted_10pct': 'Gần sắp xếp (10%)'
}
large_df['type_vi'] = large_df['type'].map(type_names).fillna(large_df['type'])

fig, ax = plt.subplots(figsize=(9.2, 4.2))
x = np.arange(len(large_df))
w = 0.35
ax.bar(x - w/2, large_df['merge_ms'], w, label='MergeSort', color='white', edgecolor='black', linewidth=1)
ax.bar(x + w/2, large_df['optimized_ms'], w, label='OptimizedMergeSort (CUTOFF = 16)', color='lightgray', edgecolor='black', linewidth=1)
ax.set_xticks(x)
ax.set_xticklabels(large_df['type_vi'], fontsize=9, rotation=10)
ax.set_xlabel('Kiểu phân bố dữ liệu')
ax.set_ylabel('Thời gian trung bình (ms)')
ax.legend()
ax.grid(True, axis='y', linestyle=':', alpha=0.6)
fig.tight_layout()
fig.savefig('report/figures/fig4_distribution.png')
plt.close()

print("Đã cập nhật script vẽ biểu đồ với CUTOFF = 16.")
