"""Baseline inference loop for the Ethical Twin API."""

from __future__ import annotations

import random

import requests
from requests import RequestException

BASE_URL = "http://127.0.0.1:8000"


def choose_action(observation: dict) -> str:
    """Pick an action using simple rule-based logic."""
    side_effect_risk = observation.get("side_effect_risk")
    genetic_risk = observation.get("genetic_risk")

    if side_effect_risk is None or genetic_risk is None:
        # Fallback keeps script robust if response shape changes.
        return random.choice(["low_dose", "medium_dose", "high_dose", "stop_drug"])

    if side_effect_risk > 0.25:
        return "stop_drug"
    if genetic_risk > 0.6:
        return "low_dose"
    return "medium_dose"


def main() -> None:
    try:
        reset_response = requests.post(f"{BASE_URL}/reset", timeout=10)
        reset_response.raise_for_status()
        state = reset_response.json()
    except RequestException as exc:
        print("Could not connect to the API at http://127.0.0.1:8000.")
        print("Start the server first: uvicorn server.app:app --reload")
        print(f"Details: {exc}")
        return

    done = bool(state.get("done", False))
    observation = state.get("observation", {})

    while not done:
        action = choose_action(observation)

        try:
            step_response = requests.post(
                f"{BASE_URL}/step",
                json={"action": action},
                timeout=10,
            )
            step_response.raise_for_status()
            step_result = step_response.json()
        except RequestException as exc:
            print("Request to /step failed.")
            print(f"Details: {exc}")
            return

        observation = step_result.get("observation", {})
        reward = step_result.get("reward", 0.0)
        done = bool(step_result.get("done", False))

        print(f"Observation: {observation}")
        print(f"Action: {action}")
        print(f"Reward: {reward}")
        print()


if __name__ == "__main__":
    main()
