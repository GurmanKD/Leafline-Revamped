"""
Fake ML pipeline simulator.

This is where real ML inference would live:
- tree segmentation
- NDVI analysis
- AQI prediction

For now: deterministic demo values.
"""

import random


def run_fake_tree_model():
    return {
        "tree_count": random.randint(80, 300),
        "tree_density": round(random.uniform(0.3, 0.9), 2),
    }


def run_fake_ndvi_model():
    return round(random.uniform(0.5, 0.85), 2)


def run_fake_aqi_model():
    return random.randint(70, 220)


def compute_green_credits(tree_count: int, ndvi: float, aqi: int) -> int:
    """
    Core credit engine logic.
    This is a simplified scoring formula.

    Higher AQI = higher credit value for same plantation (polluted area = more impact)
    """
    base = tree_count * ndvi
    pollution_weight = 1 + (aqi / 300)  # AQI scaling factor

    credits = int(base * pollution_weight)
    return max(credits, 1)
