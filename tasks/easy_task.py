"""Easy task for a single-step action decision."""

from __future__ import annotations


def get_easy_task() -> dict:
    """Return a fixed single-step task with a known correct action."""
    return {
        "name": "easy",
        "description": "Choose the safest effective dose for one synthetic patient.",
        "grader": "graders.easy_grader",
        "grader_fn": "grade",
        "score_min": 0.01,
        "score_max": 0.99,
        "patient_state": {
            "bp": 126,
            "heart_rate": 82.0,
            "genetic_risk": 0.46,
            "side_effect_risk": 0.11,
        },
        "correct_action": "medium_dose",
    }


def get_task() -> dict:
    """Compatibility alias used by validators that expect get_task()."""
    return get_easy_task()
