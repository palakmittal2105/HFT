
from task import Task
from cpu_simulator import simulate
from metrics import summarize

import priority
import rate_monotonic


def make_task(task_id, arrival, burst, deadline,
              criticality=0.5, period=5):
    return Task(
        task_id=task_id,
        task_type="Test Task",
        arrival_time=arrival,
        burst_time=burst,
        deadline=deadline,
        event_frequency=0.5,
        criticality=criticality,
        period=period
    )


def test_priority():
    print("\nTEST 1: Priority Scheduling")

    tasks = [
        make_task("A", 0, 2, 10, criticality=0.2),
        make_task("B", 0, 1, 10, criticality=0.9)
    ]

    result = simulate(
        tasks, "Priority", priority.choose_task,
        preemptive=True
    )

    rows = {r["task_id"]: r for r in result["task_results"]}

    assert rows["B"]["completion"] == 1
    assert rows["A"]["completion"] == 3

    print("PASS: The higher-priority task runs first.")


def test_rate_monotonic():
    print("\nTEST 2: Rate Monotonic")

    tasks = [
        make_task("A", 0, 2, 10, period=10),
        make_task("B", 0, 1, 10, period=3)
    ]

    result = simulate(
        tasks, "Rate Monotonic",
        rate_monotonic.choose_task,
        preemptive=True
    )

    rows = {r["task_id"]: r for r in result["task_results"]}

    assert rows["B"]["completion"] == 1
    assert rows["A"]["completion"] == 3

    print("PASS: The shorter-period task runs first.")


def test_idle_time():
    print("\nTEST 3: CPU Idle Time")

    tasks = [make_task("A", 3, 1, 10)]

    result = simulate(
        tasks, "Priority", priority.choose_task,
        preemptive=True
    )

    idle_segments = [
        segment for segment in result["gantt"]
        if segment["task_id"] == "IDLE"
    ]

    assert idle_segments[0]["start"] == 0
    assert idle_segments[0]["end"] == 3
    assert result["cpu_utilization"] == 25.0

    print("PASS: Idle time and CPU utilization are correct.")


def test_deadline_miss():
    print("\nTEST 4: Deadline Miss")

    tasks = [make_task("A", 0, 3, 2)]

    result = simulate(
        tasks, "Priority", priority.choose_task,
        preemptive=True
    )

    row = result["task_results"][0]

    assert row["completion"] == 3
    assert row["deadline_missed"] is True

    print("PASS: A task finishing after its deadline is detected.")



def test_metrics():
    print("\nTEST 5: Metric Calculation")

    tasks = [
        make_task("A", 0, 2, 10, criticality=0.9),
        make_task("B", 0, 1, 10, criticality=0.2)
    ]

    result = simulate(
        tasks,
        "Priority",
        priority.choose_task,
        preemptive=True
    )

    metrics = summarize(result)

    assert metrics["Tasks"] == 2
    assert metrics["Avg Response Time"] == 1.0
    assert metrics["Avg Waiting Time"] == 1.0
    assert metrics["Deadline Misses"] == 0

    print("PASS: Response time, waiting time and deadline metrics are correct.")



if __name__ == "__main__":
    test_priority()
    test_rate_monotonic()
    test_idle_time()
    test_deadline_miss()
    test_metrics()

    print("\nAll five additional tests passed!")
