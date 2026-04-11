from __future__ import annotations

import argparse
import json
from typing import Any

import requests


def _reset(url: str) -> dict[str, Any]:
    response = requests.post(f"{url.rstrip('/')}/reset", timeout=20)
    response.raise_for_status()
    return response.json()


def _grade(url: str, task_id: str, action: str, reasoning: str) -> float:
    response = requests.post(
        f"{url.rstrip('/')}/grader",
        json={"task_id": task_id, "action": action, "reasoning": reasoning},
        timeout=20,
    )
    response.raise_for_status()
    payload = response.json()
    return float(payload["score"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Baseline agent for ethical-twin-env")
    parser.add_argument("--url", default="http://127.0.0.1:7860", help="Base URL of the Space or local server")
    args = parser.parse_args()

    state = _reset(args.url)
    print(json.dumps({"reset_state": state}, indent=2))

    tasks = [
        ("task_1", "medium_dose", "The patient profile suggests a balanced intervention with attention to safety."),
        ("task_2", "low_dose", "The medium-horizon scenario prioritizes risk reduction and conservative dosing."),
        ("task_3", "stop_drug", "The long-horizon scenario favors stopping treatment when uncertainty and harm dominate."),
    ]

    for task_id, action, reasoning in tasks:
        score = _grade(args.url, task_id, action, reasoning)
        print(f"{task_id}: {score:.3f}")


if __name__ == "__main__":
    main()