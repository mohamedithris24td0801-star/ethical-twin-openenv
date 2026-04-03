# Ethical Twin Environment

This project is a small, beginner-friendly reinforcement learning environment for a virtual clinical trial.

It creates synthetic patient data and lets an agent choose one of four actions:

- `low_dose`
- `medium_dose`
- `high_dose`
- `stop_drug`

The environment gives a positive reward when the dosage choice matches the patient risk profile and a negative reward when the choice is unsafe or poorly matched.

## Project Structure

- `env/env.py` - core environment logic
- `models.py` - Pydantic models for observations, state, and step results
- `server/environment.py` - wrapper that converts environment output into models
- `server/app.py` - FastAPI server
- `client.py` - simple `requests` client
- `run_local.py` - local demo using random actions
- `tasks/` - challenge definitions for easy, medium, and hard levels
- `graders/` - scoring helpers for each task level
- `configs/openenv.yaml` - OpenEnv-style environment metadata and action schema

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
uvicorn server.app:app --reload
```

The server exposes these endpoints:

- `POST /reset`
- `POST /step`
- `GET /state`

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

## Tasks

The project now includes three beginner-friendly task levels:

- Easy (`tasks/easy_task.py`): one fixed patient case and one correct action.
- Medium (`tasks/medium_task.py`): a 5-step simulation task.
- Hard (`tasks/hard_task.py`): a 10-step optimization task.

These tasks can be used to test simple policies and compare different action strategies.

## Grading System

The `graders` folder contains simple scoring functions:

- `grade_easy(predicted, correct)` returns `1.0` for an exact match, else `0.0`.
- `grade_medium(total_reward)` normalizes using `total_reward / 5` and clamps to `0..1`.
- `grade_hard(total_reward)` normalizes using `total_reward / 10` and clamps to `0..1`.

This makes evaluation easy to understand while still giving a consistent score range.

## OpenEnv Configuration

`configs/openenv.yaml` describes the environment in a simple OpenEnv-style format:

- Environment name and description
- Observation schema
- Action list
- Reward style
- Available tasks (`easy`, `medium`, `hard`)

## Real-World Healthcare Use Case

This project mirrors a safe prototype of treatment optimization in healthcare.

- Privacy solution: it only uses synthetic patient data, so no real patient records are exposed.
- Bias solution: tasks and grading are explicit and auditable, making it easier to inspect decisions and improve fairness across different simulated risk profiles.

In real deployments, this kind of setup can be part of testing and validation before any clinical decision support tool is considered for real-world use.
