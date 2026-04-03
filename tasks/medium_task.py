"""Medium task for a short 5-step simulation."""

from __future__ import annotations


def get_medium_task() -> dict:
    """Return a 5-step policy-evaluation style task."""
    return {
        "description": (
            "Run a 5-step treatment simulation and maximize total reward while "
            "avoiding unsafe high-risk dosing."
        ),
        "steps": 5,
        "goal": "Keep patient risk controlled and collect positive step rewards.",
        "allowed_actions": ["low_dose", "medium_dose", "high_dose", "stop_drug"],
        "grading_hint": "Total reward will be normalized by the medium grader.",
    }
