import os
import matplotlib.pyplot as plt
import csv
from typing import Dict, List

years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
counts = [266, 352, 506, 645, 803, 1010, 1350, 1540]

plt.figure(figsize=(7.0, 4.0), dpi=360)
ax = plt.gca()
ax.plot(years, counts, marker='o', linewidth=2.0, color='#1f77b4', label='Total (all sources)')

# Add headroom so annotations don't get clipped
y_min, y_max = min(counts), max(counts)
y_range = max(1, y_max - y_min)
ax.set_ylim(y_min - 0.05 * y_range, y_max + 0.12 * y_range)

# Place labels for primary series
for x, y in zip(years, counts):
    dy, va = ( -10, 'top') if y >= y_max - 0.03 * y_range else (8, 'bottom')
    ax.annotate(f'{y}', (x, y), textcoords='offset points', xytext=(0, dy),
                ha='center', va=va, fontsize=10, clip_on=True)

# Try to overlay safety/RL counts extracted from reference.bib
data_csv = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "publication_counts.csv")
safety_series: List[int] = []
rl_series: List[int] = []
if os.path.isfile(data_csv):
    by_year: Dict[int, Dict[str, int]] = {}
    with open(data_csv, newline='', encoding='utf-8') as f:
        r = csv.DictReader(f)
        for row in r:
            y = int(row['year'])
            by_year[y] = {
                "safety": int(row.get('safety_bib', 0)),
                "rl": int(row.get('rl_bib', 0)),
            }
    safety_series = [by_year.get(y, {}).get("safety", 0) for y in years]
    rl_series = [by_year.get(y, {}).get("rl", 0) for y in years]

    ax2 = ax.twinx()
    # Compute reasonable limits for secondary axis
    s_max = max(safety_series + rl_series) if (safety_series or rl_series) else 0
    s_max = max(1, s_max)
    ax2.set_ylim(0, s_max * 1.25)

    l1, = ax2.plot(years, safety_series, marker='s', linestyle='--', color='#d62728', label='Safety (from reference.bib)')
    l2, = ax2.plot(years, rl_series, marker='^', linestyle='-.', color='#2ca02c', label='RL (from reference.bib)')

    ax2.set_ylabel('Count (from reference.bib)')
    # Optionally annotate the secondary series
    for x, y in zip(years, safety_series):
        if y > 0:
            ax2.annotate(f'{y}', (x, y), textcoords='offset points', xytext=(0, 6),
                         ha='center', va='bottom', fontsize=9, color='#d62728', clip_on=True)
    for x, y in zip(years, rl_series):
        if y > 0:
            ax2.annotate(f'{y}', (x, y), textcoords='offset points', xytext=(0, -10),
                         ha='center', va='top', fontsize=9, color='#2ca02c', clip_on=True)

# Titles, labels, legend
ax.set_title('Publications per Year (2018–2025)')
ax.set_xlabel('Year')
ax.set_ylabel('Number of Publications')
ax.grid(True, linestyle='--', alpha=0.4)
ax.set_xticks(years)

# Merge legends
handles1, labels1 = ax.get_legend_handles_labels()
handles2, labels2 = ([], [])
if 'ax2' in locals():
    handles2, labels2 = ax2.get_legend_handles_labels()
ax.legend(handles1 + handles2, labels1 + labels2, loc='upper left', frameon=True)

plt.tight_layout()

out_dir = os.path.join('docs', 'images')
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, 'publications_trend_new.png')
plt.savefig(out_path, dpi=330, bbox_inches='tight')
print(f'Saved figure to {out_path}')