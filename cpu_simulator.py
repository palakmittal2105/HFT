def simulate(tasks, policy_name, choose_task,
             preemptive=True, quantum=2):

    states = []

    for task in tasks:
        states.append({
            "task_id": task.task_id,
            "task_type": task.task_type,
            "arrival_time": task.arrival_time,
            "burst_time": task.burst_time,
            "remaining": task.burst_time,
            "deadline": task.deadline,
            "event_frequency": task.event_frequency,
            "criticality": task.criticality,
            "period": task.period,
            "first_start": None,
            "completion": None,
            "ready_order": 0
        })

    now = 0
    running_id = None
    previous_running_id = None
    quantum_left = quantum
    ready_counter = 0
    busy_ticks = 0
    context_switches = 0
    gantt = []

    while any(t["remaining"] > 0 for t in states):

        ready = [
            t for t in states
            if t["arrival_time"] <= now
            and t["remaining"] > 0
        ]

        if not ready:
            next_arrival = min(
                t["arrival_time"] for t in states
                if t["remaining"] > 0
                and t["arrival_time"] > now
            )

            gantt.append({
                "task_id": "IDLE",
                "start": now,
                "end": next_arrival
            })

            now = next_arrival
            running_id = None
            previous_running_id = None
            quantum_left = quantum
            continue

        for task in ready:
            if task["ready_order"] == 0:
                ready_counter += 1
                task["ready_order"] = ready_counter

        current = None

        # Non-preemptive FCFS continues the current task.
        if not preemptive and running_id is not None:
            current = next(
                (t for t in ready
                 if t["task_id"] == running_id),
                None
            )

        # Round Robin continues until its quantum expires.
        elif (
            policy_name == "Round Robin"
            and running_id is not None
            and quantum_left > 0
        ):
            current = next(
                (t for t in ready
                 if t["task_id"] == running_id),
                None
            )

        if current is None:
            current = choose_task(ready, now)

        chosen_id = current["task_id"]

        if (
            previous_running_id is not None
            and chosen_id != previous_running_id
        ):
            context_switches += 1

        if current["first_start"] is None:
            current["first_start"] = now

        # Record execution intervals for the Gantt chart.
        if (
            gantt
            and gantt[-1]["task_id"] == chosen_id
            and gantt[-1]["end"] == now
        ):
            gantt[-1]["end"] += 1
        else:
            gantt.append({
                "task_id": chosen_id,
                "start": now,
                "end": now + 1
            })

        current["remaining"] -= 1
        busy_ticks += 1
        now += 1

        if policy_name == "Round Robin":
            quantum_left -= 1

            if current["remaining"] == 0:
                running_id = None
                quantum_left = quantum

            elif quantum_left == 0:
                ready_counter += 1
                current["ready_order"] = ready_counter
                running_id = None
                quantum_left = quantum

            else:
                running_id = chosen_id

        elif not preemptive:
            running_id = (
                chosen_id
                if current["remaining"] > 0
                else None
            )

        else:
            running_id = None

        if current["remaining"] == 0:
            current["completion"] = now

        previous_running_id = chosen_id

    total_time = max(
        (segment["end"] for segment in gantt),
        default=0
    )

    task_results = []

    for task in states:
        turnaround = (
            task["completion"] - task["arrival_time"]
        )

        waiting = turnaround - task["burst_time"]

        response = (
            task["first_start"] - task["arrival_time"]
        )

        task_results.append({
            "task_id": task["task_id"],
            "task_type": task["task_type"],
            "arrival_time": task["arrival_time"],
            "burst_time": task["burst_time"],
            "deadline": task["deadline"],
            "first_start": task["first_start"],
            "completion": task["completion"],
            "response_time": response,
            "waiting_time": waiting,
            "turnaround_time": turnaround,
            "deadline_missed": (
                task["completion"] > task["deadline"]
            )
        })

    return {
        "policy": policy_name,
        "task_results": task_results,
        "gantt": gantt,
        "context_switches": context_switches,
        "cpu_utilization": (
            busy_ticks / total_time * 100
            if total_time else 0
        ),
        "total_time": total_time
    }