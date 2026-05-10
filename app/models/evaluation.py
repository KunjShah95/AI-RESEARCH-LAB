"""Evaluation data models"""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional, Any


class EvaluationBase(BaseModel):
    eval_type: str = Field(..., description="Type: agent, paper, summary")
    target_id: UUID
    score: float = Field(..., ge=0.0, le=1.0)
    metrics: dict[str, Any] = Field(default_factory=dict)
    details: Optional[str] = None


class Evaluation(EvaluationBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class EvaluationCreate(EvaluationBase):
    pass


class EvaluationResult(BaseModel):
    evaluation: Evaluation
    passed: bool
    feedback: Optional[str] = None
