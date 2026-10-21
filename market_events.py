from dataclasses import dataclass
import random


@dataclass
class MarketEvent:
    event_id: int
    arrival_time: int
    event_frequency: float
    event_kind: str


def generate_market_events(count=10, seed=42, bursty=True):
    rng = random.Random(seed)
    events = []
    current_time = 0

    if count <= 0:
        raise ValueError("Count must be positive")

    for i in range(count):
        in_burst = bursty and count // 3 <= i < (2 * count) // 3

        if in_burst:
            gap = rng.choice([0, 0, 1])
            frequency = rng.uniform(0.7, 1.0)
        else:
            gap = rng.randint(1, 3)
            frequency = rng.uniform(0.1, 0.6)

        current_time += gap

        events.append(
            MarketEvent(
                event_id=i + 1,
                arrival_time=current_time,
                event_frequency=round(frequency, 3),
                event_kind=rng.choice([
                    "price_update",
                    "volume_change",
                    "order_book_update"
                ])
            )
        )

    return events