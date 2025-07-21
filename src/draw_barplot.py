import matplotlib.pyplot as plt
import numpy as np

# ─── Data ──────────────────────────────────────────────────────────────────────
labels          = ["FD-Full", "PLOI", "Flax"]
success_rates   = np.array([0.480, 0.537, 0.809])
planning_times  = np.array([18.848, 10.663, 7.690])   # seconds

# succ_improve_vs = 100 * (success_rates[-1] / success_rates[:-1] - 1)             # +%
# time_reduce_vs  = 100 * (planning_times[:-1] - planning_times[-1]) / planning_times[:-1]  # −%

# ─── Figure & colours ──────────────────────────────────────────────────────────
fig, (ax_succ, ax_time) = plt.subplots(1, 2, figsize=(11, 5), dpi=120)
fig.suptitle("Flax vs Baselines on 12×12 Hard Map", fontsize=28, weight="bold", y=0.95)

bar_width = 0.65
palette   = ["#4e79a7", "#f28e2b", "#76b7b2"]

# ─── Success-rate bars ─────────────────────────────────────────────────────────
ax_succ.tick_params(axis='x', labelsize=20)
bars_succ = ax_succ.bar(labels, success_rates, width=bar_width,
                        color=palette, edgecolor="black", linewidth=0.6)


ax_succ.set_title("Success Rate", fontsize=24, weight="bold")
ax_succ.set_ylabel("Success rate", fontsize=24)
ax_succ.set_ylim(0, 1.0)
ax_succ.set_yticks(np.arange(0, 1.1, 0.2))

# numeric value on every bar
# for bar, val in zip(bars_succ, success_rates):
#     ax_succ.annotate(f"{val:.3f}", xy=(bar.get_x() + bar.get_width()/2, val),
#                      xytext=(0, 4), textcoords="offset points",
#                      ha="center", va="bottom", fontsize=10, color="black")

bar = bars_succ[-1]
ax_succ.annotate("Ours", xy=(bar.get_x() + bar.get_width()/2, success_rates[-1]),
                    xytext=(0, 4), textcoords="offset points",
                    ha="center", va="bottom", fontsize=20, color="black")


# improvement annotations (vs baselines)
# for i, pct in enumerate(succ_improve_vs):
#     ax_succ.annotate(f"+{pct:0.1f}%", xy=(i+1, success_rates[-1]), xytext=(0, 18),
#                      textcoords="offset points", ha="center",
#                      color="green", fontsize=10, weight="bold")

# ─── Planning-time bars ────────────────────────────────────────────────────────
ax_time.tick_params(axis='x', labelsize=20)
bars_time = ax_time.bar(labels, planning_times, width=bar_width,
                        color=palette, edgecolor="black", linewidth=0.6)

ax_time.set_title("Weighted Planning Time", fontsize=24, weight="bold")
ax_time.set_ylabel("Time (s)", fontsize=24)
ax_time.set_ylim(0, max(planning_times)*1.12)

# for bar, val in zip(bars_time, planning_times):
#     ax_time.annotate(f"{val:.2f} s", xy=(bar.get_x() + bar.get_width()/2, val),
#                      xytext=(0, 4), textcoords="offset points",
#                      ha="center", va="bottom", fontsize=10, color="black")

bar = bars_time[-1]
ax_time.annotate("Ours", xy=(bar.get_x() + bar.get_width()/2, planning_times[-1]),
                    xytext=(0, 4), textcoords="offset points",
                    ha="center", va="bottom", fontsize=20, color="black")

# reduction annotations
# for i, pct in enumerate(time_reduce_vs):
#     ax_time.annotate(f"–{pct:0.1f}%", xy=(i+1, planning_times[-1]), xytext=(0, -25),
#                      textcoords="offset points", ha="center",
#                      color="crimson", fontsize=10, weight="bold")

# ─── Extras ────────────────────────────────────────────────────────────────────
for ax in (ax_succ, ax_time):
    ax.spines[['right', 'top']].set_visible(False)
    # ax.tick_params(axis='x', labelrotation=15)
    ax.tick_params(axis='x', labelrotation=0)
    ax.grid(axis='y', linestyle="--", alpha=0.4)

plt.tight_layout(rect=[0, 0, 1, 0.95])  # leave room for suptitle
plt.savefig("assets/barplot.png", dpi=300, bbox_inches='tight')
# plt.show()