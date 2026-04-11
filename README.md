---
title: Ethical Twin Environment
emoji: 🧪
colorFrom: blue
colorTo: green
sdk: docker
sdk_version: "1.0"
python_version: "3.10"
app_file: app.py
pinned: false
---

# Ethical Twin Environment

This project is a small, beginner-friendly reinforcement learning environment for a virtual clinical trial.

It creates synthetic patient data and lets an agent choose one of four actions:

- `low_dose`
- `medium_dose`
- `high_dose`
- `stop_drug`

The environment gives a positive reward when the dosage choice matches the patient risk profile and a negative reward when the choice is unsafe or poorly matched.

## Links

- GitHub: https://github.com/mohamedithris24td0801-star/ethical-twin-openenv
- Hugging Face Space: https://huggingface.co/spaces/mohamedithris-ethical-twin-env

## Project Structure

- `env/env.py` - core environment logic
- `server/app.py` - FastAPI server entrypoint
- `server/environment.py` - wrapper that converts environment output into models
- `tasks/` - challenge definitions for easy, medium, and hard levels
- `graders/` - scoring helpers for each task level
- `configs/openenv.yaml` - OpenEnv-style environment metadata and action schema
- `models.py` - Pydantic models for observations, state, and step results
- `client.py` - simple `requests` client
- `policy.py` - baseline policy used by local simulation
- `run_local.py` - local demo using the baseline policy
- `baseline_inference.py` - script for baseline API interaction
- `Dockerfile` - container setup for local Docker/Hugging Face Spaces

## Install

Create a virtual environment if you want, then install the dependencies:

```bash
pip install -r requirements.txt
```

## Run the local demo

```bash
python run_local.py
```

This runs the environment directly and prints each random step until the episode ends after 10 steps.

## Run the API server

```bash
uvicorn server.app:app --host 0.0.0.0 --port 7860 --reload
```

The server exposes these endpoints:

- `POST /reset`
- `POST /step` with JSON body `{ "action": "medium_dose" }`
- `GET /state`

## Run with Docker

Build and run locally:

```bash
docker build -t ethical-twin-env .
docker run --rm -p 7860:7860 ethical-twin-env
```

The app will be available at `http://localhost:7860`.

## Deploy on Hugging Face Spaces

1. Create a new Space and choose `Docker` as the SDK.
2. Push this repository (including `Dockerfile`) to the Space.
3. Hugging Face will build the image and launch `uvicorn` on port `7860`.
4. After deployment, test endpoints: `POST /reset`, `POST /step`, `GET /state`.

## Use the client

With the server running, you can try the client from Python:

```python
from client import EthicalTwinClient

client = EthicalTwinClient()
print(client.reset())
print(client.step("medium_dose"))
print(client.state())
```

## Notes

- The environment uses synthetic data only.
- The episode ends after 10 steps.
- The code is intentionally simple so it is easy to extend for experiments.
- The project is intended to stay within 2 vCPU and 8 GB RAM limits.

## Tasks

The project now includes three beginner-friendly task levels:

- Easy (`tasks/easy_task.py`): one fixed patient case and one correct action.
- Medium (`tasks/medium_task.py`): a 5-step simulation task.
- Hard (`tasks/hard_task.py`): a 10-step optimization task.

These tasks can be used to test simple policies and compare different action strategies.

## Grading System

The `graders` folder contains simple scoring functions:

- `grade_easy(predicted, correct)` returns `0.99` for an exact match, else `0.01`.
- `grade_medium(total_reward)` normalizes using `total_reward / 5` and clamps to `(0, 1)`.
- `grade_hard(total_reward)` normalizes using `total_reward / 10` and clamps to `(0, 1)`.

This makes evaluation easy to understand while still giving a consistent score range.

## OpenEnv Configuration

`configs/openenv.yaml` describes the environment in a simple OpenEnv-style format:

- Environment name and description
- Observation schema
- Action list
- Reward style
- Available tasks (`easy`, `medium`, `hard`) with explicit grader mappings

## Real-World Healthcare Use Case

This project mirrors a safe prototype of treatment optimization in healthcare.

- Privacy solution: it only uses synthetic patient data, so no real patient records are exposed.
- Bias solution: tasks and grading are explicit and auditable, making it easier to inspect decisions and improve fairness across different simulated risk profiles.

In real deployments, this kind of setup can be part of testing and validation before any clinical decision support tool is considered for real-world use.
