import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

os.makedirs('report/figures', exist_ok=True)

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'axes.titlesize': 11,
    'axes.labelsize': 10,
    'figure.dpi': 150,
})

# --- Doc du lieu ---
cutoff_df = pd.read_csv('results/cutoff_results.csv')
summary_df = pd.read_csv('results/summary.csv')

# ==============================================
# Hinh 1: Cutoff vs Thoi gian (n=100000, random)
# ==============================================
fig, ax = plt.subplots(figsize=(8, 4.8))
ax.plot(cutoff_df['cutoff'], cutoff_df['time_ms'], 'o-', color='black', linewidth=1.5, markersize=5)
best_idx = cutoff_df['time_ms'].idxmin()
best_c = cutoff_df.loc[best_idx, 'cutoff']
best_t = cutoff_df.loc[best_idx, 'time_ms']
ax.axvline(x=best_c, color='gray', linestyle='--', linewidth=1)
ax.annotate(f'cutoff={best_c}\n({best_t:.1f} ms)', xy=(best_c, best_t),
            xytext=(best_c + 3, best_t + 1), fontsize=9)
ax.set_xlabel('Gia tri cutoff')
ax.set_ylabel('Thoi gian trung binh (ms)')
ax.set_title('Hinh 1. Anh huong cua cutoff den thoi gian sap xep\n(n = 100.000, du lieu ngau nhien, 5 lan lap)')
ax.grid(True, linestyle=':', alpha=0.6)
fig.tight_layout()
fig.savefig('report/figures/fig1_cutoff_vs_time.png')
plt.close()

# ==============================================
# Hinh 2: Thoi gian vs Kich thuoc mang (random)
# ==============================================
rand_df = summary_df[summary_df['type'] == 'random'].copy().sort_values('size')

fig, ax = plt.subplots(figsize=(8, 4.8))
ax.plot(rand_df['size'], rand_df['merge_ms'], 's--', color='black', linewidth=1.5, markersize=5, label='MergeSort')
ax.plot(rand_df['size'], rand_df['optimized_ms'], 'o-', color='dimgray', linewidth=1.5, markersize=5, label='OptimizedMergeSort (cutoff=8)')
ax.set_xlabel('Kich thuoc mang (n)')
ax.set_ylabel('Thoi gian trung binh (ms)')
ax.set_title('Hinh 2. Thoi gian sap xep theo kich thuoc mang\n(du lieu ngau nhien, 5 lan lap)')
ax.legend()
ax.grid(True, linestyle=':', alpha=0.6)
fig.tight_layout()
fig.savefig('report/figures/fig2_size_vs_time.png')
plt.close()

# ==============================================
# Hinh 3: So sanh MergeSort vs Optimized (all sizes, random)
# ==============================================
fig, ax = plt.subplots(figsize=(8, 4.8))
x = np.arange(len(rand_df))
w = 0.35
ax.bar(x - w/2, rand_df['merge_ms'], w, label='MergeSort', color='white', edgecolor='black', linewidth=1)
ax.bar(x + w/2, rand_df['optimized_ms'], w, label='OptimizedMergeSort', color='lightgray', edgecolor='black', linewidth=1)
ax.set_xticks(x)
ax.set_xticklabels([f'{int(s):,}' for s in rand_df['size']], fontsize=9)
ax.set_xlabel('Kich thuoc mang (n)')
ax.set_ylabel('Thoi gian trung binh (ms)')
ax.set_title('Hinh 3. So sanh MergeSort va OptimizedMergeSort\n(du lieu ngau nhien)')
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
    'random': 'Ngau nhien',
    'sorted': 'Da sap xep',
    'reversed': 'Nguoc chieu',
    'duplicates': 'Trung lap',
    'partially_sorted_1pct': 'Gan xep (1%)',
    'partially_sorted_5pct': 'Gan xep (5%)',
    'partially_sorted_10pct': 'Gan xep (10%)'
}
large_df['type_vi'] = large_df['type'].map(type_names).fillna(large_df['type'])

fig, ax = plt.subplots(figsize=(10, 5))
x = np.arange(len(large_df))
w = 0.35
ax.bar(x - w/2, large_df['merge_ms'], w, label='MergeSort', color='white', edgecolor='black', linewidth=1)
ax.bar(x + w/2, large_df['optimized_ms'], w, label='OptimizedMergeSort (cutoff=8)', color='lightgray', edgecolor='black', linewidth=1)
ax.set_xticks(x)
ax.set_xticklabels(large_df['type_vi'], fontsize=8.5, rotation=10)
ax.set_xlabel('Kieu phan bo du lieu')
ax.set_ylabel('Thoi gian trung binh (ms)')
ax.set_title('Hinh 4. Hieu nang tren 7 kieu du lieu dau vao\n(n = 1.000.000, 5 lan lap)')
ax.legend()
ax.grid(True, axis='y', linestyle=':', alpha=0.6)
fig.tight_layout()
fig.savefig('report/figures/fig4_distribution.png')
plt.close()

print("Da tao xong 4 bieu do moi cho 7 bo du lieu.")
