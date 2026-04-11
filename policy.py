"""Simple action policies for the Ethical Twin environment."""

from __future__ import annotations

import random
from typing import Dict

ACTIONS = ["low_dose", "medium_dose", "high_dose", "stop_drug"]


def random_policy() -> str:
    """Return a random valid action."""
    return random.choice(ACTIONS)


def smart_policy(observation: Dict[str, float]) -> str:
    """Return a rule-based action based on patient risk values."""
    if observation["side_effect_risk"] > 0.25:
        return "stop_drug"
    if observation["genetic_risk"] > 0.6:
        return "low_dose"
    return "medium_dose"
