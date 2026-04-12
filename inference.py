import argparse
import requests

DEFAULT_URL = "https://mohamedithris-ethical-twin-env.hf.space"

BASELINE = {
    "task_1": ("emergency_stop", "Minimize harm to all parties."),
    "task_2": ("share_aggregated_only", "Balance privacy and public benefit."),
    "task_3": ("retrain_with_balanced_data", "Fix bias at the root cause.")
}

def run(base_url):
    base_url = base_url.rstrip("/")
    print(f"Running baseline on {base_url}\n")
    total = 0.0
    for task_id, (action, reasoning) in BASELINE.items():
        r = requests.post(f"{base_url}/grader", json={
            "task_id": task_id, "action": action, "reasoning": reasoning
        }, timeout=30)
        r.raise_for_status()
        score = r.json()["score"]
        print(f"{task_id}: action={action}, score={score:.4f}")
        total += score
    print(f"\nAverage: {total/3:.4f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=DEFAULT_URL)
    args = parser.parse_args()
    run(args.url)