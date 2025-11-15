import os
import matplotlib.pyplot as plt

years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
counts = [266, 352, 506, 645, 803, 1010, 1350, 1540]

plt.figure(figsize=(7.0, 4.0), dpi=360)
plt.plot(years, counts, marker='o', linewidth=2.0, color='#1f77b4')

# Add headroom so annotations don't get clipped
y_min, y_max = min(counts), max(counts)
y_range = max(1, y_max - y_min)
plt.ylim(y_min - 0.05 * y_range, y_max + 0.12 * y_range)

# Place labels; put labels below points that are near the top to keep them in-frame
for x, y in zip(years, counts):
    if y >= y_max - 0.03 * y_range:
        dy, va = -10, 'top'      # near top: annotate below
    else:
        dy, va = 8, 'bottom'     # otherwise: annotate above
    plt.annotate(f'{y}', (x, y), textcoords='offset points', xytext=(0, dy),
                 ha='center', va=va, fontsize=12, clip_on=True)

plt.title('Publications per Year (2018–2025)')
plt.xlabel('Year')
plt.ylabel('Number of Publications')
plt.grid(True, linestyle='--', alpha=0.4)
plt.xticks(years)
plt.tight_layout()

out_dir = os.path.join('docs', 'images')
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, 'publications_trend.png')
plt.savefig(out_path, dpi=330, bbox_inches='tight')
print(f'Saved figure to {out_path}')