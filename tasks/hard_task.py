"""Hard task for a full 10-step optimization run."""

from __future__ import annotations


def get_hard_task() -> dict:
    """Return a 10-step optimization task."""
    return {
        "name": "hard",
        "description": (
            "Run a full 10-step virtual trial and optimize long-term reward by "
            "balancing dosage effectiveness and side-effect risk."
        ),
        "grader": "graders.hard_grader",
        "grader_fn": "grade",
        "score_min": 0.01,
        "score_max": 0.99,
        "steps": 10,
        "goal": "Find a robust action strategy across an entire episode.",
        "allowed_actions": ["low_dose", "medium_dose", "high_dose", "stop_drug"],
        "grading_hint": "Total reward will be normalized by the hard grader.",
    }


def get_task() -> dict:
    """Compatibility alias used by validators that expect get_task()."""
    return get_hard_task()
