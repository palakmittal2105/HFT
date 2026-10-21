
import pandas as pd

files = {
    "Normal 10": "scheduler_comparison_normal_10.csv",
    "Bursty 10": "scheduler_comparison_bursty_10.csv",
    "Bursty 20": "scheduler_comparison_bursty_20.csv"
}

frames = []

for scenario, filename in files.items():
    try:
        df = pd.read_csv(filename)
        df.insert(0, "Scenario", scenario)
        frames.append(df)
        print(f"Loaded: {filename}")

    except FileNotFoundError:
        print(f"Missing file: {filename}")

if len(frames) != len(files):
    print("\nRun and save all three experiments first.")
else:
    combined = pd.concat(frames, ignore_index=True)

    combined.to_csv(
        "all_experiments_comparison.csv",
        index=False
    )

    print("\nCombined experiment results:")
    print(
        combined[
            [
                "Scenario",
                "Scheduler",
                "Avg Response Time",
                "Avg Waiting Time",
                "Deadline Misses",
                "CPU Utilization (%)",
                "Context Switches",
                "Response-Time Jitter (SD)"
            ]
        ].to_string(index=False)
    )

    print("\nSaved: all_experiments_comparison.csv")
