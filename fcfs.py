def choose_task(ready, now):
    return min(
        ready,
        key=lambda task: (
            task["arrival_time"],
            task["task_id"]
        )
    )