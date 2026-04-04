"""Module 5 training simulation for the Ethical Twin Environment."""

from __future__ import annotations

from typing import Any, Dict

import requests


BASE_URL = "https://mohamedithris-ethical-twin-env.hf.space"
ACTIONS = ["low_dose", "medium_dose", "high_dose", "stop_drug"]


def choose_action(observation: Dict[str, Any]) -> str:
    """Simple policy for selecting an action from the current observation."""
    side_effect_risk = float(observation.get("side_effect_risk", 0.0))
    genetic_risk = float(observation.get("genetic_risk", 0.0))

    if side_effect_risk > 0.25:
        return "stop_drug"
    if genetic_risk > 0.6:
        return "low_dose"
    return "medium_dose"


def run_episode(session: requests.Session | None = None) -> float:
    """Run one episode against the deployed API and return the total reward."""
    owns_session = session is None
    http = session or requests.Session()
    total_reward = 0.0

    try:
        # API interaction: reset the remote environment before starting a new episode.
        response = http.post(f"{BASE_URL}/reset", timeout=30)
        response.raise_for_status()
        state = response.json()
        observation = state["observation"]
        done = bool(state.get("done", False))

        while not done:
            # Policy decision logic: pick an action using simple risk-based rules.
            action = choose_action(observation)

            step_response = http.post(
                f"{BASE_URL}/step",
                json={"action": action},
                timeout=30,
            )
            step_response.raise_for_status()
            result = step_response.json()

            observation = result["observation"]
            reward = float(result["reward"])
            done = bool(result["done"])

            # Reward accumulation: keep a running sum across the full episode.
            total_reward += reward

            print("Observation:", observation)
            print("Chosen action:", action)
            print("Reward:", reward)
            print()

        print("Final episode reward:", total_reward)
        return total_reward
    finally:
        if owns_session:
            http.close()


def main() -> None:
    episodes = 5
    rewards = []

    with requests.Session() as session:
        for episode_number in range(1, episodes + 1):
            print(f"Episode {episode_number}")
            print("-" * 20)
            episode_reward = run_episode(session=session)
            rewards.append(episode_reward)
            print()

    average_reward = sum(rewards) / len(rewards) if rewards else 0.0
    print("Episode rewards:", rewards)
    print("Average reward:", average_reward)


if __name__ == "__main__":
    main()