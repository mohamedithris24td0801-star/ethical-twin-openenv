"""Grader for easy single-step tasks."""

from __future__ import annotations


def grade_easy(predicted: str, correct: str) -> float:
    """Return a strict-open score in (0, 1)."""
    return 0.99 if predicted == correct else 0.01
