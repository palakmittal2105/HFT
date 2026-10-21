def choose_task(ready, now):
    return min(
        ready,
        key=lambda task: (
            task["ready_order"],
            task["arrival_time"],
            task["task_id"]
        )
    )