"""Grader for medium 5-step tasks."""

from __future__ import annotations


def grade_medium(total_reward: float) -> float:
    """Normalize medium-task reward to a [0, 1] score using a divisor of 5."""
    score = total_reward / 5.0
    return max(0.0, min(1.0, score))
