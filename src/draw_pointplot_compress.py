import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import numpy as np

# ─── Data ──────────────────────────────────────────────────────────────────────
# labels          = ["FD-Full", "PLOI", "Flax (Ours)"]
# success_rates   = np.array([0.000, 0.477, 0.586])
# planning_times  = np.array([100.00, 61.88, 54.86])

success_rates_avg   = np.array([0.00+0.35, 0.477, 0.680])
planning_times_avg  = np.array([100.00-20, 61.88, 54.86])

success_rates_10   = np.array([0.00+0.35, 0.449, 0.672])
planning_times_10  = np.array([100.00-20, 67.40, 60.60])

success_rates_12   = np.array([0.00+0.35, 0.481, 0.660])
planning_times_12  = np.array([100.00-20, 59.00, 50.45])

success_rates_15   = np.array([0.00+0.35, 0.502, 0.707])
planning_times_15  = np.array([100.00-20, 59.25, 53.53])


# ─── Figure & colours ──────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 5), dpi=120)
# fig.suptitle("Flax vs Baselines in Hard Mode", fontsize=24, weight="bold", y=0.95)
fig.suptitle("Flax vs Baselines in Expert Mode", fontsize=24, weight="bold", y=0.95)

palette = ["#4e79a7", "#f28e2b", "#76b7b2"]
marker_size = 250                            # area of the markers (points)

# ─── Scatter plot ──────────────────────────────────────────────────────────────
sc = ax.scatter(planning_times_avg, success_rates_avg, s=1.7*marker_size, c=palette,
                edgecolor="black", linewidth=0.6, zorder=3, marker='o')
sc = ax.scatter(planning_times_10, success_rates_10, s=0.7*marker_size, c=palette,
                edgecolor="black", linewidth=0.6, zorder=3, marker='D')
sc = ax.scatter(planning_times_12, success_rates_12, s=marker_size, c=palette,
                edgecolor="black", linewidth=0.6, zorder=3, marker='p')
sc = ax.scatter(planning_times_15, success_rates_15, s=marker_size, c=palette,
                edgecolor="black", linewidth=0.6, zorder=3, marker='h')

# ─── Axes styling ──────────────────────────────────────────────────────────────
ax.set_xlabel("Planning Time Spent (% of Time Budget)", fontsize=18, weight="bold")
ax.set_ylabel("Success rate", fontsize=18, weight="bold")
ax.set_xlim(45.0, 85.0)
ax.set_ylim(0.33, 0.75)

# ax.grid(axis="both", linestyle="--", alpha=0.4, zorder=0)
ax.set_xticks([50, 55, 60, 65, 70, 75, 80])
ax.set_xticklabels(["50", "55", "60", "65", "70", r"$\dots$", "100"], fontsize=14)
ax.set_yticks([0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7])
ax.set_yticklabels(["0.0", r"$\dots$", "0.45", "0.5", "0.55", "0.6", "0.65", "0.7"], fontsize=14)


# Remove spines for a cleaner look
for spine in ("right", "top"):
    ax.spines[spine].set_visible(False)

legend = [
    mlines.Line2D([], [], color='black', marker='D', linestyle='None', markersize=7, label="10×10 Maze"),
    mlines.Line2D([], [], color='black', marker='p', linestyle='None', markersize=10, label="12×12 Maze"),
    mlines.Line2D([], [], color='black', marker='h', linestyle='None', markersize=10, label="15×15 Maze"),
    mlines.Line2D([], [], color='black', marker='o', linestyle='None', markersize=10, label="Average"),
]
legend1 = ax.legend(handles=legend, loc='upper right', fontsize=12, title_fontsize=13)
ax.add_artist(legend1)


plt.tight_layout(rect=[0, 0, 1, 0.95])      # leave room for suptitle
plt.savefig("assets/pointplot.png", dpi=300, bbox_inches="tight")
# plt.show()
