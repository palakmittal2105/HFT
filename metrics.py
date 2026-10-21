from statistics import mean, pstdev


def summarize(result):
    rows = result["task_results"]

    response_times = [
        row["response_time"] for row in rows
    ]

    waiting_times = [
        row["waiting_time"] for row in rows
    ]

    deadline_misses = sum(
        row["deadline_missed"] for row in rows
    )

    total_tasks = len(rows)

    return {
        "Scheduler": result["policy"],
        "Tasks": total_tasks,

        "Avg Response Time": round(
            mean(response_times), 3
        ),

        "Avg Waiting Time": round(
            mean(waiting_times), 3
        ),

        "Deadline Misses": deadline_misses,

        "Deadline Miss Rate (%)": round(
            deadline_misses / total_tasks * 100, 2
        ) if total_tasks else 0,

        "CPU Utilization (%)": round(
            result["cpu_utilization"], 2
        ),

        "Context Switches": result["context_switches"],

        # Defined here as population standard deviation
        # of task response times.
        "Response-Time Jitter (SD)": round(
            pstdev(response_times), 3
        ) if len(response_times) > 1 else 0
    }