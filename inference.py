"""OpenEnv inference script for the Ethical Twin Environment."""

from __future__ import annotations

from typing import Any, Dict

import requests


BASE_URL = "https://mohamedithris-ethical-twin-env.hf.space"


def run_inference(num_episodes: int = 1) -> Dict[str, Any]:
    """Run inference on the deployed Ethical Twin Environment API.
    
    Args:
        num_episodes: Number of episodes to run for inference.
        
    Returns:
        Dictionary containing episode results and statistics.
    """
    results = {
        "episodes": [],
        "total_reward": 0.0,
        "average_reward": 0.0,
    }

    with requests.Session() as session:
        for episode_num in range(num_episodes):
            episode_data = {
                "episode": episode_num + 1,
                "steps": [],
                "total_reward": 0.0,
            }

            try:
                # Reset environment for a new episode
                response = session.post(f"{BASE_URL}/reset", timeout=30)
                response.raise_for_status()
                state = response.json()
                observation = state["observation"]
                done = bool(state.get("done", False))

                step_count = 0
                while not done and step_count < 10:
                    # Simple heuristic policy for inference
                    side_effect_risk = float(observation.get("side_effect_risk", 0.0))
                    genetic_risk = float(observation.get("genetic_risk", 0.0))

                    if side_effect_risk > 0.25:
                        action = "stop_drug"
                    elif genetic_risk > 0.6:
                        action = "low_dose"
                    else:
                        action = "medium_dose"

                    # Take a step in the environment
                    step_response = session.post(
                        f"{BASE_URL}/step",
                        json={"action": action},
                        timeout=30,
                    )
                    step_response.raise_for_status()
                    result = step_response.json()

                    observation = result["observation"]
                    reward = float(result["reward"])
                    done = bool(result["done"])

                    episode_data["steps"].append({
                        "action": action,
                        "reward": reward,
                        "observation": observation,
                    })

                    episode_data["total_reward"] += reward
                    step_count += 1

                results["episodes"].append(episode_data)
                results["total_reward"] += episode_data["total_reward"]

            except Exception as e:
                print(f"Error during episode {episode_num + 1}: {e}")
                continue

    if results["episodes"]:
        results["average_reward"] = results["total_reward"] / len(results["episodes"])

    return results


def main() -> None:
    """Main entry point for OpenEnv inference."""
    print("Starting Ethical Twin Environment inference...")
    results = run_inference(num_episodes=3)

    print("\nInference Results:")
    print(f"Total episodes: {len(results['episodes'])}")
    print(f"Average reward: {results['average_reward']:.2f}")

    for episode in results["episodes"]:
        print(f"\nEpisode {episode['episode']}: Total reward = {episode['total_reward']:.2f}")


if __name__ == "__main__":
    main()
