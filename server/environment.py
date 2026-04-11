"""Wrapper that exposes the environment through Pydantic models."""

from __future__ import annotations

from env.env import EthicalTwinEnv
from models import Observation, State, StepResult


class EnvironmentService:
    def __init__(self, seed: int | None = None) -> None:
        self.env = EthicalTwinEnv(seed=seed)
        self._state = self._build_state(observation=self.env.reset())

    def _build_state(self, observation: dict, action: str | None = None, target_action: str | None = None) -> State:
        return State(
            step=self.env.current_step,
            done=self.env.done,
            observation=Observation(**observation),
            last_action=action,
            target_action=target_action,
        )

    def reset(self) -> State:
        observation = self.env.reset()
        self._state = self._build_state(observation=observation)
        return self._state

    def step(self, action: str) -> StepResult:
        observation, reward, done, info = self.env.step(action)
        self._state = self._build_state(
            observation=observation,
            action=action,
            target_action=info.get("target_action"),
        )
        return StepResult(
            observation=self._state.observation,
            reward=reward,
            done=done,
            info=info,
            state=self._state,
        )

    def state(self) -> State:
        return self._state
