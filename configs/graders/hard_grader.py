"""Grader for hard 10-step tasks."""

from __future__ import annotations


def grade_hard(total_reward: float) -> float:
    """Normalize hard-task reward to a [0, 1] score using a divisor of 10."""
    score = total_reward / 10.0
    return max(0.0, min(1.0, score))
