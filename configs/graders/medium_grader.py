"""Grader for medium 5-step tasks."""

from __future__ import annotations


def grade_medium(total_reward: float) -> float:
    """Normalize medium-task reward to a strict-open (0, 1) score."""
    score = total_reward / 5.0
    if score <= 0:
        score = 0.01
    if score >= 1:
        score = 0.99
    return score
