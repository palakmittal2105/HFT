# Market-Event-Aware Adaptive Real-Time Scheduling for High-Frequency Trading Workloads

A Python-based CPU scheduling simulator that studies how different real-time scheduling algorithms perform under normal and bursty market-event workloads.

## Overview

High-frequency trading (HFT) systems process time-sensitive tasks such as market-data ingestion, preprocessing, signal generation, risk calculation, and order generation. When multiple tasks compete for CPU time, scheduling decisions can affect response time, deadline misses, and overall system performance.

This project simulates these workloads and compares conventional scheduling algorithms with a proposed **Market-Event-Aware Dynamic Priority Scheduling** approach. It also includes an adaptive policy selector and an interactive Streamlit dashboard for visualizing experimental results.

**Note:** This is an educational simulation using synthetic workloads. It does not connect to live financial markets or execute real trades.

## Key Features

- Synthetic normal and bursty market-event generation
- Stage-based CPU task generation
- Implementation of six scheduling policies
- Dynamic priority calculation using deadline urgency, event frequency, and task criticality
- Adaptive scheduling-policy selection based on workload characteristics
- CPU execution simulation and Gantt timeline generation
- Performance evaluation using scheduling metrics
- Multi-scenario and multi-seed experiments
- CSV result generation
- Interactive dashboard with charts and comparisons
- Automated tests for simulator and scheduling behaviour

## Scheduling Algorithms

| Algorithm | Description |
|---|---|
| First Come, First Served (FCFS) | Executes ready tasks in arrival order. |
| Round Robin (RR) | Shares CPU time using a fixed time quantum. |
| Priority Scheduling | Selects tasks using their assigned static priority or criticality. |
| Rate Monotonic (RM) | Gives higher priority to tasks with shorter periods. |
| Earliest Deadline First (EDF) | Selects the ready task with the earliest deadline. |
| Market-Aware Dynamic Priority | Dynamically scores ready tasks using deadline urgency, event frequency, and criticality. |

### Market-Aware Priority Model

The proposed scheduler calculates a task priority score using:

**Priority = 0.5 × Deadline Urgency + 0.3 × Event Frequency + 0.2 × Criticality**

The weights represent the current experimental configuration. The scheduler uses the score to choose among ready tasks. The urgency component can change during simulated execution.

The separate adaptive selector chooses a scheduling policy for a workload. This is distinct from the market-aware scheduler, which chooses individual tasks.

## Simulated Workload Pipeline

Each market event can generate tasks for the following stages:

1. Market-data ingestion
2. Data preprocessing
3. Signal generation
4. Risk calculation
5. Order generation

The simulator models CPU execution and records task-level results. Task execution requirements and workload patterns are illustrative rather than measurements from a real HFT platform.

## Performance Metrics

The scheduling policies are evaluated using:

- **Response Time:** Time between task arrival and completion.
- **Waiting Time:** Time a task spends waiting for CPU execution.
- **Deadline Misses:** Number of tasks that finish after their deadlines.
- **Deadline Miss Rate:** Proportion of tasks that miss their deadlines.
- **CPU Utilization:** Proportion of simulated time during which the CPU is executing tasks.
- **Context Switches:** Number of task transitions counted by the simulator.
- **Response-Time Jitter:** Standard deviation of task response times within a simulation run.

Metric values depend on the workload, scheduling implementation, and simulation configuration.

## Technology Stack

- **Language:** Python
- **Dashboard:** Streamlit
- **Data Handling:** Pandas
- **Visualization:** Matplotlib
- **Result Storage:** CSV files
- **Testing:** Python test scripts

## Project Structure

```text
HFT_Scheduler_Phase1/
├── task.py
├── market_events.py
├── task_generator.py
├── cpu_simulator.py
├── metrics.py
├── fcfs.py
├── round_robin.py
├── priority.py
├── rate_monotonic.py
├── edf.py
├── market_aware.py
├── adaptive_selector.py
├── main.py
├── app.py
├── compare_experiments.py
├── run_multiple_seeds.py
├── plot_results.py
├── plot_all_experiments.py
├── plot_multi_seed.py
├── run_all_tests.py
├── test_simulator.py
├── test_all_schedulers.py
├── test_market_aware.py
├── test_dynamic_urgency.py
├── test_dynamic_selection.py
└── README.md
```

Experiment-generated CSV files and plot images may also be present in the repository.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/palakmittal2105/HFT.git
cd HFT
```

### 2. Check Python

Python 3.9 or later is recommended.

```bash
python3 --version
```

### 3. Install dependencies

```bash
python3 -m pip install streamlit pandas matplotlib
```

If the project includes a `requirements.txt` file, install the listed dependencies instead:

```bash
python3 -m pip install -r requirements.txt
```

## Running the Project

### Run a scheduling experiment

```bash
python3 main.py
```

This runs the configured workload scenario and generates experiment results according to the implementation.

### Launch the interactive dashboard

```bash
python3 -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually `http://localhost:8501`.

### Run the test suite

```bash
python3 run_all_tests.py
```

### Run multi-seed experiments

```bash
python3 run_multiple_seeds.py
```

### Generate experiment comparisons and plots

```bash
python3 compare_experiments.py
python3 plot_results.py
python3 plot_all_experiments.py
python3 plot_multi_seed.py
```

Run these scripts after checking their configuration and required input files. Some scripts may depend on CSV results generated by earlier experiments.

## Experimental Scenarios

The project supports workload scenarios such as:

- **Normal workload:** Simulates a comparatively regular flow of market events.
- **Bursty workload:** Simulates periods of increased event arrivals.
- **Larger bursty workload:** Increases the number of generated events to study scheduler behaviour under a heavier workload.
- **Multi-seed experiments:** Repeats experiments with different random seeds to examine variability.

The scenarios help compare scheduling behaviour under different synthetic workload conditions.

## Testing and Validation

The project includes tests for:

- Basic CPU simulator behaviour
- Scheduling algorithm execution
- Market-aware priority selection
- Dynamic urgency and priority-score changes
- Task selection when scores change

Run the test suite using:

```bash
python3 run_all_tests.py
```

A successful test run indicates that the included tests passed for that run. It does not establish correctness for every possible workload or prove performance on real HFT systems.

## Limitations

- Workloads and task execution times are synthetic.
- The simulator does not model a complete production trading system.
- Real exchange latency, network delays, hardware behaviour, and market microstructure are not fully represented.
- The adaptive selector's behaviour depends on its implemented selection rules.
- Results from simulation should not be interpreted as proof that a scheduling policy will outperform others in a live trading environment.

## Future Improvements

- Add more realistic workload distributions and configurable task parameters.
- Expand deadline and overload analysis.
- Improve adaptive policy selection using clearly defined performance objectives.
- Evaluate the effect of different priority weights.
- Add more extensive repeated experiments and statistical comparisons.
- Explore hardware-aware and multicore scheduling models.



## License

No license has been specified yet. Add an appropriate open-source license if you want others to reuse, modify, and distribute this project.
