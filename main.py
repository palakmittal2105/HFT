import csv

from market_events import generate_market_events
from task_generator import events_to_tasks
from cpu_simulator import simulate
from metrics import summarize
import market_aware 

import fcfs
import round_robin
import priority
import rate_monotonic
import edf


def save_csv(filename, rows):
    if not rows:
        return

    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=rows[0].keys()
        )
        writer.writeheader()
        writer.writerows(rows)


def main():
    
    scenario = "bursty_20"

    if scenario == "normal_10":
        count = 10
        bursty = False
    elif scenario == "bursty_20":
        count = 20
        bursty = True
    else:
        count = 10
        bursty = True

    events = generate_market_events(
        count=count,
        seed=42,
        bursty=bursty
    )


    tasks = events_to_tasks(events)

    algorithms = [
    ("FCFS", fcfs.choose_task, False),
    ("Round Robin", round_robin.choose_task, True),
    ("Priority", priority.choose_task, True),
    ("Rate Monotonic", rate_monotonic.choose_task, True),
    ("EDF", edf.choose_task, True),
    ("Market-Aware", market_aware.choose_task, True),
]

    summaries = []

    for name, chooser, preemptive in algorithms:
        result = simulate(
            tasks=tasks,
            policy_name=name,
            choose_task=chooser,
            preemptive=preemptive,
            quantum=2
        )


        assert len(result["task_results"]) == len(tasks), (
            f"{name}: Incorrect number of task results"
        )

        assert all(
            row["completion"] is not None
            for row in result["task_results"]
        ), f"{name}: Some tasks did not complete"

        executed_ticks = sum(
            segment["end"] - segment["start"]
            for segment in result["gantt"]
            if segment["task_id"] != "IDLE"
        )

        expected_ticks = sum(task.burst_time for task in tasks)

        assert executed_ticks == expected_ticks, (
            f"{name}: CPU execution time mismatch"
        )


        summaries.append(summarize(result))

        safe_name = name.lower().replace(" ", "_")

        save_csv(
            safe_name + "_task_results.csv",
            result["task_results"]
        )

        save_csv(
            safe_name + "_gantt.csv",
            result["gantt"]
        )

    save_csv(
    f"scheduler_comparison_{scenario}.csv",
    summaries
)

    print("\nHFT-LIKE WORKLOAD SCHEDULER COMPARISON")
    print("=" * 105)
    print("Market events:", len(events))
    print("CPU tasks:", len(tasks))
    print("Round Robin quantum: 2 simulated units\n")

    headers = [
        "Scheduler",
        "Avg Response Time",
        "Avg Waiting Time",
        "Deadline Misses",
        "CPU Utilization (%)",
        "Context Switches",
        "Response-Time Jitter (SD)"
    ]

    print(" | ".join(headers))
    print("-" * 145)

    for row in summaries:
        print(
            "{} | {} | {} | {} | {} | {} | {}".format(
                row["Scheduler"],
                row["Avg Response Time"],
                row["Avg Waiting Time"],
                row["Deadline Misses"],
                row["CPU Utilization (%)"],
                row["Context Switches"],
                row["Response-Time Jitter (SD)"]
            )
        )

    #print("\nCSV files saved in the current project folder.")
    #print("The proposed scheduler will be added next.")


if __name__ == "__main__":
    main()