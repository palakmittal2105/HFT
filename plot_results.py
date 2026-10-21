
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("scheduler_comparison.csv")

metrics = [
    ("Avg Response Time", "Average Response Time"),
    ("Avg Waiting Time", "Average Waiting Time"),
    ("Deadline Misses", "Deadline Misses"),
    ("CPU Utilization (%)", "CPU Utilization"),
    ("Context Switches", "Context Switches"),
    ("Response-Time Jitter (SD)", "Response-Time Jitter")
]

for column, title in metrics:

    plt.figure(figsize=(11, 6))

    bars = plt.bar(
        df["Scheduler"],
        df[column]
    )

    plt.title(title + " Comparison", fontsize=15)
    plt.xlabel("Scheduling Algorithm")
    plt.ylabel(column)

    plt.xticks(rotation=25, ha="right")

    plt.bar_label(
        bars,
        fmt="%.2f",
        padding=3
    )

    plt.grid(axis="y", alpha=0.25)
    plt.tight_layout()

    filename = (
        title.lower().replace(" ", "_") + ".png"
    )

    plt.savefig(filename, dpi=200)
    plt.close()

    print("Saved:", filename)

print("\nAll six comparison graphs generated!")
