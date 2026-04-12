---
title: Ethical Twin Environment
emoji: ""
colorFrom: blue
colorTo: green
sdk: docker
sdk_version: "1.0"
python_version: "3.10"
app_file: app.py
pinned: false
---

# Ethical Twin Environment

An end-to-end OpenEnv-style execution environment for ethical decision-making tasks in healthcare-like scenarios.

This project provides:

- A FastAPI-based environment server with Gymnasium-style APIs.
- Multiple task difficulties with explicit graders.
- A Docker-ready setup for Hugging Face Spaces deployment.
- An inference entrypoint that emits structured output and uses injected LLM proxy credentials.

## Links

- GitHub: https://github.com/mohamedithris24td0801-star/ethical-twin-openenv
- Hugging Face Space: https://huggingface.co/spaces/mohamedithris/ethical-twin-env

## Quick Start

Install dependencies:

```bash
pip install -r requirements.txt
```

Run API server locally:

```bash
uvicorn server.app:app --host 0.0.0.0 --port 7860 --reload
```

Run inference script:

```bash
python inference.py --url http://127.0.0.1:7860
```

## Validation-Friendly Inference

The inference pipeline is built for hackathon validators and does the following:

- Prints structured stdout blocks for each task:
  - [START] task=... action=...
  - [STEP] step=... reward=...
  - [END] task=... score=... steps=...
- Uses flush-enabled prints to avoid buffered-output parsing issues.
- Uses injected LLM proxy credentials:
  - API_BASE_URL
  - API_KEY
- Makes OpenAI-compatible requests through the provided proxy endpoint.

## OpenEnv-Style API Overview

The server supports simple environment interaction methods:

- POST /reset
- POST /step
- GET /state

Additional utility endpoints:

- GET /health
- GET /tasks
- POST /grader
- GET /baseline

## Architecture

### Component Overview

```text
+----------------------------------------------------------+
|                   Client / Evaluation                    |
|  - inference.py                                          |
|  - client.py                                             |
+-----------------------------+----------------------------+
                              |
                              | HTTP
                              v
+----------------------------------------------------------+
|            FastAPI Environment Server (Docker)           |
|  - server/app.py                                         |
|  - server/environment.py                                 |
|  - Tasks + Graders                                       |
+----------------------------------------------------------+
```

### Core Components

1. Environment Server
- File: server/app.py
- Hosts all REST endpoints and exposes main() entrypoint.

2. Environment Logic
- File: server/environment.py
- Handles task state, transitions, and action processing.

3. Tasks
- Folder: tasks/
- Contains easy, medium, and hard scenario definitions.

4. Graders
- Folder: graders/
- Provides normalized scoring functions with outputs constrained to (0, 1).

5. Inference Runner
- File: inference.py
- Calls LLM proxy, chooses actions, calls /grader, and prints structured output.

## Project Structure

```text
ethical_twin_env/
|- Dockerfile
|- openenv.yaml
|- inference.py
|- baseline_inference.py
|- client.py
|- models.py
|- policy.py
|- run_local.py
|- train_agent.py
|- requirements.txt
|- pyproject.toml
|- server/
|  |- __init__.py
|  |- app.py
|  |- environment.py
|- env/
|  |- __init__.py
|  |- env.py
|- tasks/
|  |- __init__.py
|  |- easy_task.py
|  |- medium_task.py
|  |- hard_task.py
|- graders/
|  |- __init__.py
|  |- easy_grader.py
|  |- medium_grader.py
|  |- hard_grader.py
|- configs/
   |- openenv.yaml
   |- env/
   |- graders/
```

## OpenEnv Manifest

Root manifest: openenv.yaml

Current runtime config includes:

- runtime: fastapi
- app: server.app:app
- port: 7860
- actions:
  - low_dose
  - medium_dose
  - high_dose
  - stop_drug
- tasks with explicit grader mappings

Note:
Keep root openenv.yaml and configs/openenv.yaml aligned.

## Docker and Hugging Face Deployment

Build locally:

```bash
docker build -t ethical-twin-env .
```

Run locally:

```bash
docker run --rm -p 7860:7860 ethical-twin-env
```

Deploy to HF Space:

1. Create or use a Docker Space.
2. Push this repository to the Space remote.
3. Wait for image build and startup.
4. Test /health, /tasks, /grader.

## Programmatic Usage

### Async-like Environment Access via HTTP Client

```python
from client import EthicalTwinClient

client = EthicalTwinClient(base_url="http://127.0.0.1:7860")
print(client.reset())
print(client.step("medium_dose"))
print(client.state())
```

### Inference with Injected Proxy Credentials

```bash
set API_BASE_URL=https://your-proxy-url
set API_KEY=your-proxy-key
python inference.py --url https://mohamedithris-ethical-twin-env.hf.space
```

## Design Principles

- Simple API surface: reset, step, state.
- Type-safe models with Pydantic.
- Secure and isolated deployment with Docker.
- Explicit scoring and task definitions for transparent evaluation.
- Validator-ready inference behavior for structured logs and proxy-based LLM usage.

## Development

Run local baseline simulation:

```bash
python run_local.py
```

Train agent entrypoint:

```bash
python train_agent.py
```

Baseline API scoring run:

```bash
python baseline_inference.py
```

## Requirements

- Python 3.10+
- Docker Desktop or Docker Engine
- FastAPI
- Uvicorn
- Requests
- OpenAI SDK (OpenAI-compatible proxy usage)
- openenv-core

## Troubleshooting

If validation says structured output is missing:

- Ensure inference.py is the executed entrypoint.
- Ensure [START], [STEP], [END] are printed to stdout.
- Ensure print(..., flush=True) is used.

If validation says no LLM proxy calls were made:

- Ensure API_BASE_URL and API_KEY are read from environment variables.
- Ensure OpenAI client is initialized with those variables.
- Ensure no hardcoded key or external provider bypass is used.

## License

This project is provided for educational and hackathon use.
Use the repository license terms where applicable.
