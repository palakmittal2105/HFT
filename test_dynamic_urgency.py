
from task import Task
from market_aware import calculate_priority


def make_task(deadline, frequency=0.5, criticality=0.5):
    task = Task(
        task_id="TEST",
        task_type="Risk Calculation",
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


def test_urgency_increases():
    task = make_task(deadline=10)

    early = calculate_priority(task, now=0)
    late = calculate_priority(task, now=8)

    assert late > early, (
        f"Urgency should increase as the deadline approaches: "
        f"early={early}, late={late}"
    )

    print("PASS: Priority increases as the deadline approaches.")


def test_frequency_affects_priority():
    low_frequency = make_task(deadline=10, frequency=0.1)
    high_frequency = make_task(deadline=10, frequency=0.9)

    low_score = calculate_priority(low_frequency, now=5)
    high_score = calculate_priority(high_frequency, now=5)

    assert high_score > low_score

    print("PASS: Higher event frequency increases priority.")


def test_criticality_affects_priority():
    low_criticality = make_task(deadline=10, criticality=0.1)
    high_criticality = make_task(deadline=10, criticality=0.9)

    low_score = calculate_priority(low_criticality, now=5)
    high_score = calculate_priority(high_criticality, now=5)

    assert high_score > low_score

    print("PASS: Higher criticality increases priority.")


if __name__ == "__main__":
    test_urgency_increases()
    test_frequency_affects_priority()
    test_criticality_affects_priority()

    print("\nAll dynamic-priority component tests passed!")
