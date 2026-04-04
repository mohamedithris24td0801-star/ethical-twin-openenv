# Ethical Twin OpenEnv Environment

A synthetic healthcare simulation environment built using the OpenEnv pattern for reinforcement learning experiments.

This project simulates virtual patients and allows an agent to choose safe drug dosage decisions. The environment produces step-based rewards so reinforcement learning agents can learn safer treatment strategies without using real patient data.

---

# Problem Statement

Modern healthcare AI systems face two major challenges:

1. **Privacy constraints** – Hospitals cannot freely share real patient records due to regulations.
2. **Bias in datasets** – Many clinical models are trained using limited demographic data, reducing reliability for underrepresented populations.

Because of these issues, testing new treatment strategies using real patient data becomes difficult.

---

# Solution

The Ethical Twin Environment simulates **synthetic patient profiles** and allows agents to experiment with treatment strategies in a safe digital environment.

The system creates virtual patients with simulated vitals and risk scores.
Agents must choose the correct drug dosage strategy based on the patient's risk profile.

This approach allows experimentation without exposing real medical records.

---

# Observation Schema

Each environment step returns a simulated patient observation containing:

* **bp** – simulated blood pressure
* **heart_rate** – simulated heart rate
* **genetic_risk** – genetic risk factor between 0 and 1
* **side_effect_risk** – predicted probability of drug side effects

Example observation:

```
{
  "bp": 120,
  "heart_rate": 82.3,
  "genetic_risk": 0.45,
  "side_effect_risk": 0.18
}
```

---

# Action Space

The agent can choose one of four treatment decisions:

* **low_dose** – minimal medication dosage
* **medium_dose** – standard dosage
* **high_dose** – aggressive treatment dosage
* **stop_drug** – discontinue the medication

---

# Reward Function

The environment provides **step-based feedback**.

Rewards encourage safe treatment strategies.

Typical reward rules:

* **+1.0** when the dosage matches the patient risk profile
* **-0.5** when the dosage is poorly matched
* **+1.5** when stopping the drug prevents high side-effect risk

This reward design helps reinforcement learning agents gradually learn better decisions.

---

# Project Structure

```
ethical_twin_env/

env/
    env.py

server/
    environment.py
    app.py

tasks/
    easy_task.py
    medium_task.py
    hard_task.py

graders/
    easy_grader.py
    medium_grader.py
    hard_grader.py

configs/
    openenv.yaml

models.py
client.py
policy.py
baseline_inference.py
run_local.py
requirements.txt
README.md
```

---

# Installation

Install dependencies:

```
pip install -r requirements.txt
```

(Optional) create a virtual environment first.

---

# Run Local Simulation

Run the environment locally without the API:

```
python run_local.py
```

This will simulate a full episode and print observations, actions, and rewards for each step.

Episodes end automatically after **10 steps**.

---

# Run the API Server

Start the FastAPI server:

```
uvicorn server.app:app --reload
```

Once running, the environment exposes the following endpoints:

```
POST /reset
POST /step
GET /state
```

Interactive API documentation is available at:

```
http://127.0.0.1:8000/docs
```

---

# Baseline Agent

The repository includes a simple rule-based baseline agent in **baseline_inference.py**.

The baseline policy works as follows:

```
if side_effect_risk > 0.25:
    action = stop_drug
elif genetic_risk > 0.6:
    action = low_dose
else:
    action = medium_dose
```

This baseline demonstrates how an agent interacts with the environment API.

Run it with:

```
python baseline_inference.py
```

---

# Tasks

The environment includes three task levels to evaluate decision policies.

### Easy Task

A single patient case with one correct treatment decision.

### Medium Task

A 5-step patient management simulation.

### Hard Task

A 10-step optimization challenge where the agent must maintain safe treatment decisions over time.

---

# Grading System

Simple grading utilities are included to evaluate performance.

* **grade_easy(predicted, correct)**
  Returns **1.0** for a correct decision and **0.0** otherwise.

* **grade_medium(total_reward)**
  Score = `total_reward / 5`, clamped between **0 and 1**.

* **grade_hard(total_reward)**
  Score = `total_reward / 10`, clamped between **0 and 1**.

This provides a consistent scoring scale for comparing policies.

---

# OpenEnv Configuration

The environment metadata is defined in:

```
configs/openenv.yaml
```

It specifies:

* Environment name
* Observation schema
* Available actions
* Reward type
* Task levels

---

# Real-World Healthcare Use Case

This project demonstrates how reinforcement learning environments can support safer healthcare experimentation.

Key advantages:

**Privacy Protection**
Only synthetic patient data is used. No real patient records are required.

**Bias Inspection**
Explicit tasks and grading functions make it easier to analyze decision policies and identify potential biases.

**Safe Experimentation**
Researchers can test treatment strategies in a controlled environment before applying them to real-world systems.

---

# Future Improvements

Possible extensions include:

* Larger synthetic patient datasets
* More complex patient risk models
* Multi-drug treatment strategies
* Integration with reinforcement learning training pipelines such as GRPO

---

# License

This project is intended for educational and research purposes.
