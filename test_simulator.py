
from task import Task
from cpu_simulator import simulate
import fcfs
import round_robin
import edf


def make_task(task_id, arrival, burst, deadline):
    return Task(
        task_id=task_id,
        task_type="Test Task",
        arrival_time=arrival,
        burst_time=burst,
        deadline=deadline,
        event_frequency=0.5,
        criticality=0.5,
        period=5
    )


def test_fcfs():
    print("\nTEST 1: FCFS")

    tasks = [
        make_task("A", 0, 3, 10),
        make_task("B", 0, 2, 10)
    ]

    result = simulate(
        tasks, "FCFS", fcfs.choose_task,
        preemptive=False
    )

    rows = {
        row["task_id"]: row
        for row in result["task_results"]
    }

    assert rows["A"]["completion"] == 3
    assert rows["B"]["completion"] == 5
    assert rows["B"]["response_time"] == 3
    assert rows["B"]["waiting_time"] == 3
    assert result["context_switches"] == 1

    print("PASS: Completion times, response time,")
    print("waiting time and context switches are correct.")


def test_round_robin():
    print("\nTEST 2: Round Robin")

    tasks = [
        make_task("A", 0, 3, 10),
        make_task("B", 0, 2, 10)
    ]

    result = simulate(
        tasks, "Round Robin", round_robin.choose_task,
        preemptive=True, quantum=2
    )

    rows = {
        row["task_id"]: row
        for row in result["task_results"]
    }

    assert rows["A"]["completion"] == 5
    assert rows["B"]["completion"] == 4
    assert rows["A"]["response_time"] == 0
    assert rows["B"]["response_time"] == 2
    assert result["context_switches"] == 2

    print("PASS: Quantum rotation and task timing are correct.")


def test_edf_preemption():
    print("\nTEST 3: EDF preemption")

    tasks = [
        make_task("A", 0, 4, 10),
        make_task("B", 1, 1, 3)
    ]

    result = simulate(
        tasks, "EDF", edf.choose_task,
        preemptive=True
    )

    rows = {
        row["task_id"]: row
        for row in result["task_results"]
    }

    assert rows["A"]["completion"] == 5
    assert rows["B"]["completion"] == 2
    assert rows["B"]["response_time"] == 0
    assert result["context_switches"] == 2

    print("PASS: EDF preempts A when the more urgent")
    print("task B arrives.")


if __name__ == "__main__":
    test_fcfs()
    test_round_robin()
    test_edf_preemption()

    print("\nAll three simulator tests passed!")
