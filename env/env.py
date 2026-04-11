"""Simple synthetic clinical-trial style reinforcement learning environment."""

from __future__ import annotations

import random
from typing import Any, Dict, Tuple


class EthicalTwinEnv:
    """A tiny OpenAI Gym-style environment for synthetic patient treatment."""

    ACTIONS = ("low_dose", "medium_dose", "high_dose", "stop_drug")
    MAX_STEPS = 10

    def __init__(self, seed: int | None = None) -> None:
        self.rng = random.Random(seed)
        self.current_step = 0
        self.done = False
        self.patient: Dict[str, float] = {}
        self.last_action: str | None = None
        self.reset()

    def _sample_patient(self) -> Dict[str, float]:
        return {
            "bp": round(self.rng.uniform(90, 140), 1),
            "heart_rate": round(self.rng.uniform(60, 100), 1),
            "genetic_risk": round(self.rng.uniform(0, 1), 2),
            "side_effect_risk": round(self.rng.uniform(0, 0.3), 2),
        }

    def _target_action(self) -> str:
        bp = self.patient["bp"]
        heart_rate = self.patient["heart_rate"]
        genetic_risk = self.patient["genetic_risk"]
        side_effect_risk = self.patient["side_effect_risk"]

        risk_score = (
            (genetic_risk * 0.45)
            + (side_effect_risk * 1.4)
            + max(0.0, (140.0 - bp) / 100.0) * 0.05
            + max(0.0, (heart_rate - 80.0) / 40.0) * 0.05
        )

        if side_effect_risk > 0.24 or risk_score > 0.72:
            return "stop_drug"
        if risk_score > 0.52:
            return "low_dose"
        if risk_score > 0.32:
            return "medium_dose"
        return "high_dose"

    def _apply_action(self, action: str) -> None:
        changes: Dict[str, Tuple[float, float, float]] = {
            "low_dose": (-1.5, -0.6, 0.012),
            "medium_dose": (-3.0, -1.1, 0.025),
            "high_dose": (-5.0, -2.0, 0.05),
            "stop_drug": (0.8, 0.5, -0.02),
        }

        bp_delta, heart_delta, side_effect_delta = changes[action]
        self.patient["bp"] = round(max(80.0, min(180.0, self.patient["bp"] + bp_delta + self.rng.uniform(-0.8, 0.8))), 1)
        self.patient["heart_rate"] = round(max(45.0, min(140.0, self.patient["heart_rate"] + heart_delta + self.rng.uniform(-0.5, 0.5))), 1)
        self.patient["side_effect_risk"] = round(max(0.0, min(1.0, self.patient["side_effect_risk"] + side_effect_delta + self.rng.uniform(-0.01, 0.01))), 2)

    def _observation(self) -> Dict[str, float]:
        return dict(self.patient)

    def reset(self) -> Dict[str, float]:
        self.current_step = 0
        self.done = False
        self.last_action = None
        self.patient = self._sample_patient()
        return self._observation()

    def step(self, action: str) -> Tuple[Dict[str, float], float, bool, Dict[str, Any]]:
        if action not in self.ACTIONS:
            raise ValueError(f"Invalid action: {action}. Allowed actions: {', '.join(self.ACTIONS)}")
        if self.done:
            raise RuntimeError("Episode finished. Call reset() to start a new trial.")

        target_action = self._target_action()
        reward = 1.0 if action == target_action else -0.5

        if action == "high_dose" and (
            self.patient["genetic_risk"] > 0.6 or self.patient["side_effect_risk"] > 0.2
        ):
            reward -= 1.5
        elif action == "stop_drug" and target_action != "stop_drug":
            reward -= 0.5
        elif action == "stop_drug" and target_action == "stop_drug":
            reward += 0.5

        self._apply_action(action)

        self.current_step += 1
        self.last_action = action
        self.done = self.current_step >= self.MAX_STEPS

        info = {
            "step": self.current_step,
            "target_action": target_action,
            "last_action": action,
        }
        return self._observation(), float(reward), self.done, info
