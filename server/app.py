from fastapi import FastAPI
import os
import uvicorn
from server.environment import EnvironmentService

app = FastAPI(
    title="Ethical Twin Environment",
    description="Virtual clinical trial environment using synthetic patients",
    version="1.0.0"
)

# Initialize environment
env_service = EnvironmentService()


@app.get("/")
def root():
    return {
        "message": "Ethical Twin Environment API running",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/reset")
def reset():
    return env_service.reset()


@app.post("/step")
def step(action: dict):
    action_value = action.get("action") if isinstance(action, dict) else None
    if not action_value:
        return {
            "error": "Missing required field: action",
            "allowed_actions": ["low_dose", "medium_dose", "high_dose", "stop_drug"],
        }
    return env_service.step(action_value)


@app.get("/state")
def state():
    return env_service.state()


def main() -> None:
    """Main entry point for the server."""
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("server.app:app", host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()