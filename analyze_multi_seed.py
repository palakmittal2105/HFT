
import pandas as pd

# Load results from all 90 scheduler runs.
df = pd.read_csv("multi_seed_results.csv")

metrics = [
    "Avg Response Time",
    "Avg Waiting Time",
    "Deadline Misses",
    "CPU Utilization (%)",
    "Context Switches",
    "Response-Time Jitter (SD)"
]

# Calculate the mean and standard deviation across seeds.
summary = (
    df.groupby(["Scenario", "Scheduler"])[metrics]
    .agg(["mean", "std"])
    .round(3)
)

print("\nMULTI-SEED EXPERIMENT ANALYSIS")
print("=" * 90)
print(summary.to_string())

# Flatten the column names for a convenient CSV.
summary.columns = [
    f"{metric}_{stat}"
    for metric, stat in summary.columns
]

summary = summary.reset_index()

summary.to_csv(
    "multi_seed_summary.csv",
    index=False
)

print("\nSaved: multi_seed_summary.csv")

# Rank schedulers within each scenario.
print("\nBEST SCHEDULER PER SCENARIO")
print("=" * 90)

for scenario, group in df.groupby("Scenario"):
    print(f"\n{scenario}")

    for metric in [
        "Avg Response Time",
        "Deadline Misses",
        "Avg Waiting Time"
    ]:
        best = group.groupby("Scheduler")[metric].mean().idxmin()
        value = group.groupby("Scheduler")[metric].mean().min()

        print(f"  Lowest {metric}: {best} ({value:.3f})")
