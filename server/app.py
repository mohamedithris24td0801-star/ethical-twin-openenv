from __future__ import annotations

import os

import uvicorn
from fastapi import FastAPI, HTTPException

from graders.easy_grader import grade_easy
from graders.hard_grader import grade_hard
from graders.medium_grader import grade_medium
from models import ActionRequest, GraderRequest, GraderResponse, MessageResponse, State, StepResult, TaskSpec, TasksResponse
from server.environment import EnvironmentService

app = FastAPI(
    title="Ethical Twin Environment",
    description="Virtual clinical trial environment using synthetic patients",
    version="1.0.0",
)

env_service = EnvironmentService()


def grade_task_1(predicted: str, correct: str) -> float:
    return grade_easy(predicted, correct)


def grade_task_2(total_reward: float) -> float:
    return grade_medium(total_reward)


def grade_task_3(total_reward: float) -> float:
    return grade_hard(total_reward)


TASKS = {
    "task_1": {
        "name": "easy",
        "description": "Choose the safest effective dose for one synthetic patient.",
        "grader": "graders.easy_grader.grade_easy",
        "grader_endpoint": "/grader",
        "score_min": 0.001,
        "score_max": 0.999,
        "grader_fn": grade_task_1,
    },
    "task_2": {
        "name": "medium",
        "description": "Run a 5-step treatment simulation and maximize total reward while avoiding unsafe dosing.",
        "grader": "graders.medium_grader.grade_medium",
        "grader_endpoint": "/grader",
        "score_min": 0.001,
        "score_max": 0.999,
        "grader_fn": grade_task_2,
    },
    "task_3": {
        "name": "hard",
        "description": "Run a full 10-step virtual trial and optimize long-term reward.",
        "grader": "graders.hard_grader.grade_hard",
        "grader_endpoint": "/grader",
        "score_min": 0.001,
        "score_max": 0.999,
        "grader_fn": grade_task_3,
    },
}

TASK_ALIASES = {
    "easy": "task_1",
    "medium": "task_2",
    "hard": "task_3",
}

ALLOWED_ACTIONS = ["low_dose", "medium_dose", "high_dose", "stop_drug"]


@app.get("/")
def root() -> MessageResponse:
    return MessageResponse(message="Ethical Twin Environment API running")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.get("/tasks", response_model=TasksResponse)
def tasks() -> TasksResponse:
    return TasksResponse(
        tasks=[
            TaskSpec(
                name=task["name"],
                description=task["description"],
                grader=task["grader"],
                grader_endpoint=task["grader_endpoint"],
            )
            for task in TASKS.values()
        ]
    )


@app.post("/grader", response_model=GraderResponse)
def grader(request: GraderRequest) -> GraderResponse:
    task_key = TASK_ALIASES.get(request.task, request.task)
    task = TASKS.get(task_key)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Unknown task: {request.task}")

    if task_key == "task_1":
        if request.predicted is None or request.correct is None:
            raise HTTPException(status_code=400, detail="predicted and correct are required for task_1")
        score = task["grader_fn"](request.predicted, request.correct)
    else:
        if request.total_reward is None:
            raise HTTPException(status_code=400, detail="total_reward is required for task_2 and task_3")
        score = task["grader_fn"](request.total_reward)

    clamped_score = max(0.001, min(0.999, float(score)))
    return GraderResponse(task=task["name"], score=clamped_score)


@app.post("/reset")
def reset() -> State:
    return env_service.reset()


@app.post("/step")
def step(action: ActionRequest) -> StepResult:
    if action.action not in ALLOWED_ACTIONS:
        raise HTTPException(
            status_code=400,
            detail={"error": "Missing or invalid action", "allowed_actions": ALLOWED_ACTIONS},
        )
    return env_service.step(action.action)


@app.get("/state")
def state() -> State:
    return env_service.state()


def main() -> None:
    """Main entry point for the server."""
    port = int(os.getenv("PORT", "7860"))
    uvicorn.run("server.app:app", host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()