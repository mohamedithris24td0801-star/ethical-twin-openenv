import argparse

import requests

DEFAULT_URL = "https://mohamedithris-ethical-twin-env.hf.space"

BASELINE = {
    "task_1": ("emergency_stop", "Minimize harm to all parties."),
    "task_2": ("share_aggregated_only", "Balance privacy and public benefit."),
    "task_3": ("retrain_with_balanced_data", "Fix bias at the root cause."),
}


def emit_start(task_id: str, action: str) -> None:
    print(f"[START] task={task_id} action={action}", flush=True)


def emit_step(task_id: str, step: int, reward: float, action: str) -> None:
    print(
        f"[STEP] task={task_id} step={step} action={action} reward={reward:.4f}",
        flush=True,
    )


def emit_end(task_id: str, score: float, steps: int, status: str = "ok") -> None:
    print(
        f"[END] task={task_id} score={score:.4f} steps={steps} status={status}",
        flush=True,
    )

def run(base_url):
    base_url = base_url.rstrip("/")
    print(f"Running baseline on {base_url}", flush=True)
    total = 0.0
    completed = 0
    for task_id, (action, reasoning) in BASELINE.items():
        emit_start(task_id, action)
        try:
            response = requests.post(
                f"{base_url}/grader",
                json={
                    "task_id": task_id,
                    "action": action,
                    "reasoning": reasoning,
                },
                timeout=30,
            )
            response.raise_for_status()
            score = float(response.json()["score"])
            emit_step(task_id, 1, score, action)
            emit_end(task_id, score, 1)
            total += score
            completed += 1
        except requests.RequestException as exc:
            emit_step(task_id, 1, 0.0, action)
            emit_end(task_id, 0.0, 0, status=f"error={type(exc).__name__}")
            print(f"Request failed for {task_id}: {exc}", flush=True)
        except (KeyError, ValueError, TypeError) as exc:
            emit_step(task_id, 1, 0.0, action)
            emit_end(task_id, 0.0, 0, status=f"error={type(exc).__name__}")
            print(f"Invalid response for {task_id}: {exc}", flush=True)

    average = total / completed if completed else 0.0
    print(f"Average score: {average:.4f}", flush=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=DEFAULT_URL)
    args = parser.parse_args()
    run(args.url)