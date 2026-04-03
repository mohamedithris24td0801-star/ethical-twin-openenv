"""Hard task for a full 10-step optimization run."""

from __future__ import annotations


def get_hard_task() -> dict:
    """Return a 10-step optimization task."""
    return {
        "description": (
            "Run a full 10-step virtual trial and optimize long-term reward by "
            "balancing dosage effectiveness and side-effect risk."
        ),
        "steps": 10,
        "goal": "Find a robust action strategy across an entire episode.",
        "allowed_actions": ["low_dose", "medium_dose", "high_dose", "stop_drug"],
        "grading_hint": "Total reward will be normalized by the hard grader.",
    }
