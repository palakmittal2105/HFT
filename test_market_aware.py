
from task import Task
from cpu_simulator import simulate
import market_aware


def test_market_aware_priority():
    print("\nTEST 1: Market-Aware Priority Selection")

    tasks = [
        Task(
            task_id="A",
            task_type="Preprocessing",
            arrival_time=0,
            burst_time=2,
            deadline=10,
            event_frequency=0.1,
            criticality=0.1,
            period=10
        ),
        Task(
            task_id="B",
            task_type="Risk Calculation",
            arrival_time=0,
            burst_time=1,
            deadline=10,
            event_frequency=1.0,
            criticality=1.0,
            period=10
        )
    ]

    result = simulate(
        tasks,
        "Market-Aware",
        market_aware.choose_task,
        preemptive=True
    )

    first_segment = result["gantt"][0]

    assert first_segment["task_id"] == "B", (
        f"Expected task B to run first, "
        f"but got {first_segment['task_id']}"
    )

    print("PASS: The higher-scoring task runs first.")


if __name__ == "__main__":
    test_market_aware_priority()
    print("\nMarket-Aware scheduler test passed!")
