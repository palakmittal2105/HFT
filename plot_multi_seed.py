
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("multi_seed_results.csv")

metrics = [
    ("Avg Response Time", "Average Response Time"),
    ("Avg Waiting Time", "Average Waiting Time"),
    ("Deadline Misses", "Deadline Misses"),
    ("CPU Utilization (%)", "CPU Utilization"),
    ("Context Switches", "Context Switches"),
    ("Response-Time Jitter (SD)", "Response-Time Jitter")
]

for scenario in df["Scenario"].unique():
    subset = df[df["Scenario"] == scenario]

    for metric, title in metrics:
        stats = (
            subset.groupby("Scheduler")[metric]
            .agg(["mean", "std"])
            .fillna(0)
        )

        ax = stats["mean"].plot(
            kind="bar",
            yerr=stats["std"],
            capsize=4,
            figsize=(11, 6),
            legend=False
        )

        ax.set_title(f"{title} — {scenario} (5 seeds)")
        ax.set_xlabel("Scheduling Algorithm")
        ax.set_ylabel(metric)
        ax.tick_params(axis="x", rotation=25)
        ax.grid(axis="y", alpha=0.25)

        plt.tight_layout()

        filename = (
            f"{scenario.lower().replace(' ', '_')}_"
            f"{title.lower().replace(' ', '_')}.png"
        )

        plt.savefig(filename, dpi=200, bbox_inches="tight")
        plt.close()

        print("Saved:", filename)

print("\nAll multi-seed graphs generated!")
