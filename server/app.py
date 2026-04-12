from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from server.environment import EthicalTwinEnvironment, TASKS, grade_task

app = FastAPI(title="Ethical Twin Environment", version="1.0.0")

env = EthicalTwinEnvironment()


class ResetRequest(BaseModel):
    task_id: Optional[str] = None


class StepRequest(BaseModel):
    action: str
    reasoning: Optional[str] = ""


class GraderRequest(BaseModel):
    task_id: str
    action: str
    reasoning: Optional[str] = ""


@app.get("/health")
def health():
    return {"status": "ok", "environment": "ethical-twin-env"}


@app.get("/tasks")
def get_tasks():
    task_list = []
    for task_id, task in TASKS.items():
        task_list.append({
            "id": task["id"],
            "name": task["name"],
            "difficulty": task["difficulty"],
            "description": task["description"],
            "available_actions": task["scenario"]["available_actions"],
            "ethical_principles": task["ethical_principles"],
            "grader": "grade_task",
            "grader_endpoint": "/grader"
        })
    return {"tasks": task_list, "total": len(task_list)}


@app.post("/reset")
def reset(req: ResetRequest = None):
    task_id = req.task_id if req else None
    return env.reset(task_id=task_id)


@app.post("/step")
def step(req: StepRequest):
    result = env.step(action=req.action, reasoning=req.reasoning or "")
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.get("/state")
def state():
    return env.state()


@app.post("/grader")
def grader(req: GraderRequest):
    if req.task_id not in TASKS:
        raise HTTPException(status_code=404, detail=f"Task '{req.task_id}' not found.")
    valid_actions = TASKS[req.task_id]["scenario"]["available_actions"]
    if req.action not in valid_actions:
        raise HTTPException(status_code=400, detail=f"Invalid action. Valid: {valid_actions}")
    score = grade_task(req.task_id, req.action, req.reasoning or "")
    assert 0.0 < score < 1.0, f"Score out of range: {score}"
    return {
        "task_id": req.task_id,
        "action": req.action,
        "score": score
    }


@app.get("/baseline")
def baseline():
    results = {}
    for task_id, task in TASKS.items():
        optimal = task["optimal_action"]
        score = grade_task(task_id, optimal, "optimal")
        results[task_id] = {"optimal_action": optimal, "score": score}
    avg = sum(r["score"] for r in results.values()) / len(results)
    return {"baseline_scores": results, "average_score": round(avg, 4)}