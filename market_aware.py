def calculate_priority(task, now, w1=0.5, w2=0.3, w3=0.2):
    """
    Market-Event-Aware Dynamic Priority Scheduling.

    D = deadline urgency
    F = market-event frequency
    C = task criticality
    """

    remaining_time = max(task["deadline"] - now, 0)

    # Normalize urgency to the range [0, 1].
    relative_deadline = max(
        task["deadline"] - task["arrival_time"], 1
    )

    urgency = 1 - min(
        remaining_time / relative_deadline, 1
    )

    # Frequency and criticality are already in [0, 1]
    # in our current workload generator.
    frequency = max(0, min(task["event_frequency"], 1))
    criticality = max(0, min(task["criticality"], 1))

    return (
        w1 * urgency
        + w2 * frequency
        + w3 * criticality
    )


def choose_task(ready, now):
    """Select the ready task with the highest dynamic priority."""

    return max(
        ready,
        key=lambda task: (
            calculate_priority(task, now),
            -task["deadline"],
            task["task_id"]
        )
    )