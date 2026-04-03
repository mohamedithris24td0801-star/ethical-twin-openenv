"""Grader for easy single-step tasks."""

from __future__ import annotations


def grade_easy(predicted: str, correct: str) -> float:
    """Return 1.0 for an exact match and 0.0 otherwise."""
    return 1.0 if predicted == correct else 0.0
