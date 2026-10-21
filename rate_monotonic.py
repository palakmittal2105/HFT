def choose_task(ready, now):
    return min(
        ready,
        key=lambda task: (
            task["period"]
            if task["period"] is not None
            else float("inf"),
            task["arrival_time"],
            task["task_id"]
        )
    )