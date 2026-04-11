"""Pydantic models for the Ethical Twin environment."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class EthicalAction(BaseModel):
    task_id: str
    action: str
    reasoning: str = ""


class EthicalObservation(BaseModel):
    bp: float
    heart_rate: float
    genetic_risk: float
    side_effect_risk: float


class EthicalState(BaseModel):
    task_id: str
    step: int = 0
    done: bool = False
    observation: EthicalObservation
    last_action: str | None = None
    reasoning: str = ""
    score: float = 0.0
    metadata: dict[str, Any] = Field(default_factory=dict)
