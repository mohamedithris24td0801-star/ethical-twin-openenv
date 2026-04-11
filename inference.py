from __future__ import annotations

import os
from typing import Any

import requests
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")
TASK_NAME = os.getenv("TASK_NAME", "easy")
BENCHMARK_NAME = os.getenv("BENCHMARK", "openenv")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

OPENENV_BASE_URL = os.getenv(
    "OPENENV_BASE_URL",
    "https://mohamedithris-ethical-twin-env.hf.space",
).rstrip("/")
ALLOWED_ACTIONS = ["low_dose", "medium_dose", "high_dose", "stop_drug"]


def _bool_str(value: bool) -> str:
    return "true" if value else "false"


def _error_str(message: str | None) -> str:
    if not message:
        return "null"
    return message.replace("\n", " ").replace("\r", " ").strip() or "null"


def _choose_action(observation: dict[str, Any]) -> str:
    prompt = (
        "Choose exactly one action from this list: low_dose, medium_dose, high_dose, stop_drug. "
        "Reply with only the action token. "
        f"Observation={observation}"
    )
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0,
            max_tokens=8,
        )
        content = (response.choices[0].message.content or "").strip().lower()
        content = content.split()[0].strip(".,;:!?\"'()[]{}")
        if content in ALLOWED_ACTIONS:
            return content
    except Exception:
        pass

    side_effect_risk = float(observation.get("side_effect_risk", 0.0))
    genetic_risk = float(observation.get("genetic_risk", 0.0))
    if side_effect_risk > 0.24:
        return "stop_drug"
    if genetic_risk > 0.55:
        return "low_dose"
    if genetic_risk > 0.30:
        return "medium_dose"
    return "high_dose"


def main() -> None:
    rewards: list[float] = []
    step_no = 0
    had_error = False
    done = False

    print(f"[START] task={TASK_NAME} env={BENCHMARK_NAME} model={MODEL_NAME}", flush=True)

    with requests.Session() as session:
        try:
            reset = session.post(f"{OPENENV_BASE_URL}/reset", timeout=20)
            reset.raise_for_status()
            state = reset.json()
            observation = state.get("observation", {})
            done = bool(state.get("done", False))
        except Exception as exc:
            had_error = True
            done = True
            step_no = 1
            rewards.append(0.0)
            print(
                f"[STEP] step={step_no} action=stop_drug reward=0.00 done=true "
                f"error={_error_str(str(exc))}",
                flush=True,
            )
            print(
                f"[END] success=false steps={step_no} rewards=0.00",
                flush=True,
            )
            return

        while not done and step_no < 64:
            action = _choose_action(observation)
            reward = 0.0
            error_message: str | None = None

            try:
                resp = session.post(
                    f"{OPENENV_BASE_URL}/step",
                    json={"action": action},
                    timeout=20,
                )
                resp.raise_for_status()
                payload = resp.json()

                if "error" in payload and payload["error"]:
                    done = True
                    had_error = True
                    error_message = str(payload["error"])
                else:
                    reward = float(payload.get("reward", 0.0))
                    done = bool(payload.get("done", False))
                    observation = payload.get("observation", observation)
            except Exception as exc:
                done = True
                had_error = True
                error_message = str(exc)

            step_no += 1
            rewards.append(reward)
            print(
                f"[STEP] step={step_no} action={action} reward={reward:.2f} "
                f"done={_bool_str(done)} error={_error_str(error_message)}",
                flush=True,
            )

    reward_csv = ",".join(f"{value:.2f}" for value in rewards)
    success = (not had_error) and (step_no > 0)
    print(
        f"[END] success={_bool_str(success)} steps={step_no} rewards={reward_csv}",
        flush=True,
    )


if __name__ == "__main__":
    main()