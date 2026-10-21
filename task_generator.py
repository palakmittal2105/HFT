from task import Task

TASK_STAGES = [
    ("Market Data Ingestion", 1, 0.70, 5, 7),
    ("Preprocessing", 3, 0.50, 8, 9),
    ("Signal Generation", 4, 0.60, 10, 8),
    ("Risk Calculation", 1, 1.00, 6, 5),
    ("Order Generation", 2, 0.90, 7, 6),
]


def events_to_tasks(events):
    tasks = []

    for event in events:
        for index, stage in enumerate(TASK_STAGES):
            name, burst, criticality, period, relative_deadline = stage

            arrival = event.arrival_time + index

            task = Task(
                task_id="E{:03d}-T{}".format(
                    event.event_id, index + 1
                ),
                task_type=name,
                arrival_time=arrival,
                burst_time=burst,
                deadline=arrival + relative_deadline,
                event_frequency=event.event_frequency,
                criticality=criticality,
                period=period
            )

            tasks.append(task)

    return sorted(
        tasks,
        key=lambda task: (task.arrival_time, task.task_id)
    )