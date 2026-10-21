
import csv

from market_events import generate_market_events
from task_generator import events_to_tasks
from cpu_simulator import simulate
from metrics import summarize

import fcfs
import round_robin
import priority
import rate_monotonic
import edf
import market_aware


SCENARIOS = [
    ("Normal 10", 10, False),
    ("Bursty 10", 10, True),
    ("Bursty 20", 20, True),
]

ALGORITHMS = [
    ("FCFS", fcfs.choose_task, False),
    ("Round Robin", round_robin.choose_task, True),
    ("Priority", priority.choose_task, True),
    ("Rate Monotonic", rate_monotonic.choose_task, True),
    ("EDF", edf.choose_task, True),
    ("Market-Aware", market_aware.choose_task, True),
]

SEEDS = [42, 43, 44, 45, 46]

rows = []

for scenario, count, bursty in SCENARIOS:
    for seed in SEEDS:
        events = generate_market_events(
            count=count,
            seed=seed,
            bursty=bursty
        )

        tasks = events_to_tasks(events)

        for name, chooser, preemptive in ALGORITHMS:
            result = simulate(
                tasks=tasks,
                policy_name=name,
                choose_task=chooser,
                preemptive=preemptive,
                quantum=2
            )

            summary = summarize(result)
            summary["Scenario"] = scenario
            summary["Seed"] = seed
            rows.append(summary)

with open(
    "multi_seed_results.csv",
    "w",
    newline=""
) as file:
    writer = csv.DictWriter(
        file,
        fieldnames=rows[0].keys()
    )
    writer.writeheader()
    writer.writerows(rows)

print("Multi-seed experiments completed.")
print("Scenarios:", len(SCENARIOS))
print("Seeds per scenario:", len(SEEDS))
print("Algorithms:", len(ALGORITHMS))
print("Total runs:", len(rows))
print("Saved: multi_seed_results.csv")
