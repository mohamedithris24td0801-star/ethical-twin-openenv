"""Easy task for a single-step action decision."""

from __future__ import annotations


def get_easy_task() -> dict:
    """Return a fixed single-step task with a known correct action."""
    return {
        "description": "Choose the safest effective dose for one synthetic patient.",
        "patient_state": {
            "bp": 126,
            "heart_rate": 82.0,
            "genetic_risk": 0.46,
            "side_effect_risk": 0.11,
        },
        "correct_action": "medium_dose",
    }
