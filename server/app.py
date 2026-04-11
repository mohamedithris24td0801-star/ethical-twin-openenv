from __future__ import annotations

import os

import uvicorn
from fastapi import FastAPI, HTTPException

from models import EthicalAction
from server.environment import EthicalTwinEnvironment, TASKS, grade_task

app = FastAPI(title="ethical-twin-env", version="1.0.0")
environment = EthicalTwinEnvironment()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.get("/tasks")
def tasks() -> dict[str, list[dict[str, object]]]:
    return {
        "tasks": [
            {
                **task,
                "grader_endpoint": "/grader",
            }
            for task in TASKS.values()
        ]
    }


@app.post("/reset")
def reset() -> dict[str, object]:
    state = environment.reset()
    return state.model_dump()


@app.post("/step")
def step(payload: dict[str, object]) -> dict[str, object]:
    action = str(payload.get("action", "")).strip()
    reasoning = str(payload.get("reasoning", "")).strip()
    task_id = str(payload.get("task_id", environment.current_task_id)).strip() or environment.current_task_id
    environment.current_task_id = task_id if task_id in TASKS else environment.current_task_id
    state = environment.step(
        EthicalAction(
            task_id=environment.current_task_id,
            action=action,
            reasoning=reasoning,
        )
    )
    return state.model_dump()


@app.get("/state")
def state() -> dict[str, object]:
    return environment.state().model_dump()


@app.post("/grader")
def grader(payload: dict[str, object]) -> dict[str, object]:
    task_id = str(payload.get("task_id", "")).strip()
    action = str(payload.get("action", "")).strip()
    reasoning = str(payload.get("reasoning", "")).strip()

    if task_id not in TASKS:
        raise HTTPException(status_code=404, detail=f"Unknown task_id: {task_id}")

    score = grade_task(task_id, action, reasoning)
    assert 0.0 < score < 1.0
    return {"task_id": task_id, "score": score}


@app.get("/baseline")
def baseline() -> dict[str, object]:
    return {
        "message": "baseline endpoint ready",
        "tasks": list(TASKS.keys()),
    }


def main() -> None:
    port = int(os.getenv("PORT", "7860"))
    uvicorn.run("server.app:app", host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()