import matplotlib.pyplot as plt
import numpy as np

# ─── Data ──────────────────────────────────────────────────────────────────────
labels          = ["FD-Full", "PLOI", "Flax (Ours)"]
success_rates   = np.array([0.480, 0.537, 0.809])
planning_times  = np.array([18.848, 10.663, 7.690])   # seconds

# ─── Figure & colours ──────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 5), dpi=120)
fig.suptitle("Flax vs Baselines on 12×12 Hard Map",
             fontsize=24, weight="bold", y=0.95)

palette = ["#4e79a7", "#f28e2b", "#76b7b2"]
marker_size = 250                            # area of the markers (points)

# ─── Scatter plot ──────────────────────────────────────────────────────────────
sc = ax.scatter(planning_times, success_rates, s=marker_size, c=palette,
                edgecolor="black", linewidth=0.6, zorder=3)

# Annotate each point with its label (“Ours” for Flax)
for x, y, lbl in zip(planning_times, success_rates, labels):
    display_lbl = lbl
    ax.annotate(display_lbl,
                xy=(x, y),
                xytext=(0, 8), textcoords="offset points",
                ha="center", va="bottom",
                fontsize=14,
                weight="bold" if "Flax" in lbl else None)

# ─── Axes styling ──────────────────────────────────────────────────────────────
ax.set_xlabel("Weighted planning time (s)", fontsize=18, weight="bold")
ax.set_ylabel("Success rate", fontsize=18, weight="bold")
ax.set_xlim(4.0, planning_times.max() * 1.15)
ax.set_ylim(0.4, 1.0)
ax.set_yticks(np.arange(0.4, 1.1, 0.2))
ax.grid(axis="both", linestyle="--", alpha=0.4, zorder=0)

# Remove spines for a cleaner look
for spine in ("right", "top"):
    ax.spines[spine].set_visible(False)

plt.tight_layout(rect=[0, 0, 1, 0.95])      # leave room for suptitle
plt.savefig("assets/pointplot.png", dpi=300, bbox_inches="tight")
# plt.show()
