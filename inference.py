from __future__ import annotations

import argparse
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
    print(f"[START] url={args.url.rstrip('/')} task_count=3", flush=True)
    print(f"[STEP] step=0 event=reset task=task_1 state={state}", flush=True)

    tasks = [
        ("task_1", "medium_dose", "The patient profile suggests a balanced intervention with attention to safety."),
        ("task_2", "low_dose", "The medium-horizon scenario prioritizes risk reduction and conservative dosing."),
        ("task_3", "stop_drug", "The long-horizon scenario favors stopping treatment when uncertainty and harm dominate."),
    ]

    scores: list[float] = []
    for index, (task_id, action, reasoning) in enumerate(tasks, start=1):
        score = _grade(args.url, task_id, action, reasoning)
        scores.append(score)
        print(
            f"[STEP] step={index} task={task_id} action={action} score={score:.3f} reasoning={reasoning}",
            flush=True,
        )

    average_score = sum(scores) / len(scores)
    print(
        f"[END] task=ethical-twin-env score={average_score:.3f} steps={len(tasks)}",
        flush=True,
    )


if __name__ == "__main__":
    main()