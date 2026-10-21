
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("all_experiments_comparison.csv")

metrics = [
    ("Avg Response Time", "Average Response Time"),
    ("Avg Waiting Time", "Average Waiting Time"),
    ("Deadline Misses", "Deadline Misses"),
    ("CPU Utilization (%)", "CPU Utilization"),
    ("Context Switches", "Context Switches"),
    ("Response-Time Jitter (SD)", "Response-Time Jitter")
]

for column, title in metrics:
    pivot = df.pivot(
        index="Scheduler",
        columns="Scenario",
        values=column
    )

    # Keep the scenario order consistent in every chart.
    scenario_order = [
        "Normal 10",
        "Bursty 10",
        "Bursty 20"
    ]
    pivot = pivot.reindex(columns=scenario_order)

    ax = pivot.plot(
        kind="bar",
        figsize=(12, 6),
        width=0.8
    )

    ax.set_title(title + " Across Workload Scenarios")
    ax.set_xlabel("Scheduling Algorithm")
    ax.set_ylabel(column)
    ax.tick_params(axis="x", rotation=25)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(title="Scenario")

    plt.tight_layout()

    filename = (
        title.lower().replace(" ", "_") + "_all_scenarios.png"
    )

    plt.savefig(filename, dpi=200, bbox_inches="tight")
    plt.close()

    print("Saved:", filename)

