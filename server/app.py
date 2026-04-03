"""FastAPI application for the Ethical Twin environment."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from models import State, StepResult
from server.environment import EnvironmentService

app = FastAPI(title="Ethical Twin Environment", version="1.0.0")
service = EnvironmentService()


class StepRequest(BaseModel):
    action: str


@app.post("/reset", response_model=State)
def reset_environment() -> State:
    return service.reset()


@app.post("/step", response_model=StepResult)
def step_environment(payload: StepRequest) -> StepResult:
    try:
        return service.step(payload.action)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@app.get("/state", response_model=State)
def get_state() -> State:
    return service.state()
