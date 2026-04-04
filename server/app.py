from fastapi import FastAPI
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
    return env_service.step(action)


@app.get("/state")
def state():
    return env_service.state()


def main() -> None:
    """Main entry point for the server."""
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()