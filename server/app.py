from __future__ import annotations

import os

import uvicorn
from fastapi import FastAPI, HTTPException

from server.environment import EthicalTwinEnvironment, TASKS, grade_task

app = FastAPI(title="ethical-twin-env", version="1.0.0")
env = EthicalTwinEnvironment()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/tasks")
def tasks() -> dict[str, object]:
    payload = []
    for task_id in ("task_1", "task_2", "task_3"):
        task = TASKS[task_id]
        payload.append(
            {
                "id": task["id"],
                "name": task["name"],
                "difficulty": task["difficulty"],
                "description": task["description"],
                "available_actions": task["scenario"]["available_actions"],
                "grader": "grade_task",
                "grader_endpoint": "/grader",
            }
        )
    return {"tasks": payload, "total": 3}


@app.post("/reset")
def reset(payload: dict[str, object] | None = None) -> dict[str, object]:
    payload = payload or {}
    task_id = payload.get("task_id")
    try:
        return env.reset(task_id=str(task_id)) if task_id else env.reset()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/step")
def step(payload: dict[str, object]) -> dict[str, object]:
    action = str(payload.get("action", "")).strip()
    reasoning = str(payload.get("reasoning", "")).strip()
    if not action:
        raise HTTPException(status_code=400, detail="Missing action")
    return env.step(action=action, reasoning=reasoning)


@app.get("/state")
def state() -> dict[str, object]:
    return env.state()


@app.post("/grader")
def grader(payload: dict[str, object]) -> dict[str, object]:
    task_id = str(payload.get("task_id", "")).strip()
    action = str(payload.get("action", "")).strip()
    reasoning = str(payload.get("reasoning", "")).strip()

    if task_id not in TASKS:
        raise HTTPException(status_code=400, detail=f"Unknown task_id: {task_id}")
    if not action:
        raise HTTPException(status_code=400, detail="Missing action")

    score = grade_task(task_id, action, reasoning)
    assert 0.0 < score < 1.0
    return {"task_id": task_id, "score": score}


@app.get("/baseline")
def baseline() -> dict[str, object]:
    results = []
    for task_id in ("task_1", "task_2", "task_3"):
        task = TASKS[task_id]
        action = task["scenario"]["optimal_action"]
        reasoning = "Baseline policy selects the documented optimal action for this ethical scenario."
        score = grade_task(task_id, action, reasoning)
        assert 0.0 < score < 1.0
        results.append({"task_id": task_id, "action": action, "score": score})

    average = sum(item["score"] for item in results) / len(results)
    return {"results": results, "average_score": average, "total": len(results)}


def main() -> None:
    port = int(os.getenv("PORT", "7860"))
    uvicorn.run("server.app:app", host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()