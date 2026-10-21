from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    task_id: str
    task_type: str
    arrival_time: int
    burst_time: int
    deadline: int
    event_frequency: float
    criticality: float
    period: Optional[int] = None

    def __post_init__(self):
        if self.arrival_time < 0:
            raise ValueError("Arrival time cannot be negative")
        if self.burst_time <= 0:
            raise ValueError("Burst time must be positive")
        if self.deadline <= self.arrival_time:
            raise ValueError("Deadline must be after arrival time")
        if self.event_frequency < 0:
            raise ValueError("Event frequency cannot be negative")
        if not 0 <= self.criticality <= 1:
            raise ValueError("Criticality must be between 0 and 1")
        if self.period is not None and self.period <= 0:
            raise ValueError("Period must be positive")