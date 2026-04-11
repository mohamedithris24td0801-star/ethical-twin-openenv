from __future__ import annotations

import argparse
import os
from typing import Any

import requests
from openai import OpenAI


API_BASE_URL = os.environ["API_BASE_URL"]
API_KEY = os.environ["API_KEY"]
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)


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


def _ask_llm(task_id: str, state: dict[str, Any]) -> tuple[str, str]:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "Return a concise action and short reasoning for the task.",
            },
            {
                "role": "user",
                "content": (
                    f"Task: {task_id}\n"
                    f"State: {state}\n"
                    "Choose one action from low_dose, medium_dose, high_dose, stop_drug and explain briefly."
                ),
            },
        ],
        temperature=0,
        max_tokens=64,
    )
    content = (response.choices[0].message.content or "").strip()
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    action = "medium_dose"
    reasoning = content or "Balanced decision based on the task state."

    for line in lines:
        lowered = line.lower()
        for candidate in ("low_dose", "medium_dose", "high_dose", "stop_drug"):
            if candidate in lowered:
                action = candidate
                break
        if action != "medium_dose":
            break

    return action, reasoning


def main() -> None:
    parser = argparse.ArgumentParser(description="Baseline agent for ethical-twin-env")
    parser.add_argument("--url", default="http://127.0.0.1:7860", help="Base URL of the Space or local server")
    args = parser.parse_args()

    state = _reset(args.url)
    print(f"[START] url={args.url.rstrip('/')} task_count=3", flush=True)
    print(f"[STEP] step=0 event=reset task=task_1 state={state}", flush=True)

    tasks = [
        "task_1",
        "task_2",
        "task_3",
    ]

    scores: list[float] = []
    for index, task_id in enumerate(tasks, start=1):
        action, reasoning = _ask_llm(task_id, state)
        score = _grade(args.url, task_id, action, reasoning)
        scores.append(score)
        print(
            f"[STEP] step={index} task={task_id} action={action} score={score:.3f} reasoning={reasoning}",
            flush=True,
        )
        state = {"task_id": task_id, "action": action, "reasoning": reasoning, "score": score}

    average_score = sum(scores) / len(scores)
    print(
        f"[END] task=ethical-twin-env score={average_score:.3f} steps={len(tasks)}",
        flush=True,
    )


if __name__ == "__main__":
    main()