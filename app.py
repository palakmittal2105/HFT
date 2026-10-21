
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from market_events import generate_market_events
from task_generator import events_to_tasks
from cpu_simulator import simulate
from metrics import summarize
from adaptive_selector import select_scheduler

import fcfs
import round_robin
import priority
import rate_monotonic
import edf
import market_aware


st.set_page_config(
    page_title="HFT Scheduler Dashboard",
    page_icon="📈",
    layout="wide"
)

# ---------- PAGE HEADER ----------

st.title("Market-Event-Aware Adaptive Real-Time Scheduler")





# ---------- SIDEBAR SETTINGS ----------

st.sidebar.title("Simulation Settings")

event_count = st.sidebar.slider(
    "Number of market events",
    min_value=5,
    max_value=30,
    value=10
)

seed = st.sidebar.number_input(
    "Random seed",
    min_value=0,
    max_value=99999,
    value=42
)

workload_mode = st.sidebar.selectbox(
    "Market workload",
    ["Bursty", "Normal"]
)

quantum = st.sidebar.slider(
    "Round Robin time quantum",
    min_value=1,
    max_value=5,
    value=2
)

run_button = st.sidebar.button(
    "Run Simulation",
    type="primary",
    use_container_width=True
)



# ---------- RUN SIMULATION ----------

if run_button or "outputs" not in st.session_state:

    events = generate_market_events(
        count=int(event_count),
        seed=int(seed),
        bursty=(workload_mode == "Bursty")
    )

    tasks = events_to_tasks(events)

    # Select one algorithm automatically for this workload.
    selected_name, selected_chooser, selected_preemptive = (
        select_scheduler(
            tasks,
            bursty=(workload_mode == "Bursty")
        )
    )

    # Run the selected adaptive policy.
    adaptive_result = simulate(
        tasks=tasks,
        policy_name=selected_name,
        choose_task=selected_chooser,
        preemptive=selected_preemptive,
        quantum=int(quantum)
    )

    # Run all six algorithms for comparison.
    algorithms = [
        ("FCFS", fcfs.choose_task, False),
        ("Round Robin", round_robin.choose_task, True),
        ("Priority", priority.choose_task, True),
        ("Rate Monotonic", rate_monotonic.choose_task, True),
        ("EDF", edf.choose_task, True),
        ("Market-Aware", market_aware.choose_task, True)
    ]

    outputs = {}
    summaries = []

    for name, chooser, preemptive in algorithms:
        result = simulate(
            tasks=tasks,
            policy_name=name,
            choose_task=chooser,
            preemptive=preemptive,
            quantum=int(quantum)
        )

        outputs[name] = result
        summaries.append(summarize(result))

    # Store the adaptive result separately from the baselines.
    st.session_state["outputs"] = outputs
    st.session_state["summaries"] = summaries
    st.session_state["events"] = events
    st.session_state["tasks"] = tasks
    st.session_state["adaptive_name"] = selected_name
    st.session_state["adaptive_result"] = adaptive_result


# ---------- LOAD RESULTS ----------

outputs = st.session_state["outputs"]
summaries = st.session_state["summaries"]
events = st.session_state["events"]
tasks = st.session_state["tasks"]

summary_df = pd.DataFrame(summaries)


# ---------- ADAPTIVE SELECTION RESULT ----------

st.subheader("Adaptive Scheduler Selection")

st.success(
    f"Automatically selected algorithm: "
    f"{st.session_state['adaptive_name']}"
)

st.caption(
    "The selector chooses a scheduling policy for the current "
    "workload. The table and charts below compare all six "
    "baseline policies."
)

adaptive_summary = summarize(
    st.session_state["adaptive_result"]
)

st.dataframe(
    pd.DataFrame([adaptive_summary]),
    width="stretch",
    hide_index=True
)



# ---------- OVERVIEW METRICS ----------

st.subheader("Simulation Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Market Events", len(events))
col2.metric("CPU Tasks", len(tasks))
col3.metric("Schedulers Compared", len(outputs))
col4.metric("Workload", workload_mode)

st.divider()


# ---------- COMPARISON TABLE ----------

st.subheader("Scheduler Performance Comparison")

st.dataframe(
    summary_df,
    use_container_width=True,
    hide_index=True
)


# ---------- RESPONSE TIME CHART ----------

st.subheader("Performance Analysis")

left, right = st.columns(2)

with left:
    st.markdown("#### Average Response Time")

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.bar(
        summary_df["Scheduler"],
        summary_df["Avg Response Time"]
    )

    ax.set_ylabel("Simulated time units")
    ax.tick_params(axis="x", rotation=35)
    fig.tight_layout()

    st.pyplot(fig)
    plt.close(fig)


# ---------- DEADLINE MISSES CHART ----------

with right:
    st.markdown("#### Deadline Misses")

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.bar(
        summary_df["Scheduler"],
        summary_df["Deadline Misses"]
    )

    ax.set_ylabel("Number of missed deadlines")
    ax.tick_params(axis="x", rotation=35)
    fig.tight_layout()

    st.pyplot(fig)
    plt.close(fig)


# ---------- CPU UTILIZATION CHART ----------

left, right = st.columns(2)

with left:
    st.markdown("#### CPU Utilization")

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.bar(
        summary_df["Scheduler"],
        summary_df["CPU Utilization (%)"]
    )

    ax.set_ylabel("Utilization (%)")
    ax.set_ylim(0, 100)
    ax.tick_params(axis="x", rotation=35)
    fig.tight_layout()

    st.pyplot(fig)
    plt.close(fig)


# ---------- CONTEXT SWITCHES CHART ----------

with right:
    st.markdown("#### Context Switches")

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.bar(
        summary_df["Scheduler"],
        summary_df["Context Switches"]
    )

    ax.set_ylabel("Number of switches")
    ax.tick_params(axis="x", rotation=35)
    fig.tight_layout()

    st.pyplot(fig)
    plt.close(fig)


st.divider()


# ---------- GANTT CHART ----------

st.subheader("CPU Execution Timeline — Gantt Chart")

selected_scheduler = st.selectbox(
    "Select a scheduler",
    list(outputs.keys()),
    index=list(outputs.keys()).index("Market-Aware")
)

gantt = outputs[selected_scheduler]["gantt"]

# Assign a row to each task in order of appearance.
task_ids = []

for segment in gantt:
    task_id = segment["task_id"]

    if task_id != "IDLE" and task_id not in task_ids:
        task_ids.append(task_id)

y_positions = {
    task_id: index
    for index, task_id in enumerate(task_ids)
}

idle_position = len(task_ids)

fig, ax = plt.subplots(figsize=(14, 6))

for segment in gantt:

    start = segment["start"]
    duration = segment["end"] - start
    task_id = segment["task_id"]

    if task_id == "IDLE":
        y = idle_position
    else:
        y = y_positions[task_id]

    ax.barh(
        y,
        duration,
        left=start,
        height=0.65
    )

ax.set_yticks(
    list(range(len(task_ids))) + [idle_position]
)

ax.set_yticklabels(
    task_ids + ["IDLE"]
)

ax.set_xlabel("Simulated Time")
ax.set_ylabel("CPU Task")
ax.set_title(
    selected_scheduler + " — CPU Execution Timeline"
)

ax.invert_yaxis()
ax.grid(axis="x", linestyle="--", alpha=0.35)

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)


# ---------- TASK-LEVEL RESULTS ----------

with st.expander("View Individual Task Results"):

    task_scheduler = st.selectbox(
        "Select scheduler results",
        list(outputs.keys()),
        key="task_results_scheduler"
    )

    task_df = pd.DataFrame(
        outputs[task_scheduler]["task_results"]
    )

    st.dataframe(
        task_df,
        use_container_width=True,
        hide_index=True
    )


# ---------- DOWNLOAD RESULTS ----------

st.subheader("Export Results")

st.download_button(
    label="Download Scheduler Comparison CSV",
    data=summary_df.to_csv(index=False),
    file_name="scheduler_comparison.csv",
    mime="text/csv"
)

st.caption(
    "All results are simulation outputs. Validate the simulator "
    "and test multiple workload scenarios before reporting "
    "experimental conclusions."
)
