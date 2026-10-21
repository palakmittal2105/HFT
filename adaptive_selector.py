
import fcfs
import round_robin
import priority
import rate_monotonic
import edf
import market_aware


def select_scheduler(tasks, bursty):
    """
    Select a scheduling policy using workload characteristics.
    Returns the policy name, chooser function, and preemption mode.
    """

    if not tasks:
        raise ValueError("Cannot select a scheduler for an empty workload.")

    avg_criticality = sum(
        task.criticality for task in tasks
    ) / len(tasks)

    avg_event_frequency = sum(
        task.event_frequency for task in tasks
    ) / len(tasks)

    tight_deadlines = sum(
        task.deadline - task.arrival_time <= task.burst_time * 2
        for task in tasks
    )

    tight_deadline_ratio = tight_deadlines / len(tasks)

    # Rule 1: Tight deadlines require deadline-aware scheduling.
    if tight_deadline_ratio >= 0.30:
        return "EDF", edf.choose_task, True

    # Rule 2: Highly critical workloads use criticality-based priority.
    if avg_criticality >= 0.75:
        return "Priority", priority.choose_task, True

    # Rule 3: Bursty, frequent market activity uses market-aware priority.
    if bursty and avg_event_frequency >= 0.50:
        return "Market-Aware", market_aware.choose_task, True

    # Rule 4: Other bursty workloads use time-sharing.
    if bursty:
        return "Round Robin", round_robin.choose_task, True

    # Rule 5: Periodic workloads can use Rate Monotonic.
    if all(task.period is not None for task in tasks):
        return "Rate Monotonic", rate_monotonic.choose_task, True

    # Default for ordinary workloads.
    return "FCFS", fcfs.choose_task, False
