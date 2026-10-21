
from task import Task
from market_aware import choose_task, calculate_priority


def make_task(task_id, deadline, frequency, criticality):
    task = Task(
        task_id=task_id,
        task_type="Test Task",
        arrival_time=0,
        burst_time=2,
        deadline=deadline,
        event_frequency=frequency,
        criticality=criticality,
        period=10
    )

    return {
        "task_id": task.task_id,
        "task_type": task.task_type,
        "arrival_time": task.arrival_time,
        "burst_time": task.burst_time,
        "remaining": task.burst_time,
        "deadline": task.deadline,
        "event_frequency": task.event_frequency,
        "criticality": task.criticality,
        "period": task.period
    }


def test_selection_changes_over_time():
   
    task_a = make_task(
        "A", deadline=20, frequency=0.6, criticality=0.6
    )
    task_b = make_task(
        "B", deadline=5, frequency=0.0, criticality=0.0
    )


    ready = [task_a, task_b]

    early_choice = choose_task(ready, now=0)
    late_choice = choose_task(ready, now=4)

    print("At time 0:", early_choice["task_id"])
    print("At time 4:", late_choice["task_id"])

    assert early_choice["task_id"] == "A"

    # Verify the actual scores before asserting the late choice.
    score_a = calculate_priority(task_a, now=4)
    score_b = calculate_priority(task_b, now=4)

    print("Task A score at time 4:", score_a)
    print("Task B score at time 4:", score_b)

    assert score_b > score_a
    assert late_choice["task_id"] == "B"

    print("PASS: Task selection changes as urgency changes.")


if __name__ == "__main__":
    test_selection_changes_over_time()
