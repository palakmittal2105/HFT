# HFT Scheduler — Phase 1

This phase implements only the Review 1 workload foundation: synthetic market
events, the five HFT-like task stages, and task attributes. Scheduling algorithms
will be added in later phases.

## Setup on macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

## Files
- `task.py`: task data model and validation
- `market_events.py`: reproducible synthetic events
- `task_generator.py`: converts events into five pipeline task types
- `main.py`: prints a preview
- `schedulers/`: reserved for FCFS, RR, Priority, RM, EDF, and proposed scheduler
- `results/`: reserved for experiment outputs

Times are simulated units. Burst times, deadlines, and criticality values are
initial experimental parameters, not measurements of a real HFT system.
