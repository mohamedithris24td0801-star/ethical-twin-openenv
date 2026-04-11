"""Pydantic models for the Ethical Twin service."""

from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class Observation(BaseModel):
    bp: float
    heart_rate: float
    genetic_risk: float
    side_effect_risk: float


class State(BaseModel):
    step: int = 0
    done: bool = False
    observation: Observation
    last_action: Optional[str] = None
    target_action: Optional[str] = None


class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: Dict[str, Any] = Field(default_factory=dict)
    state: State
