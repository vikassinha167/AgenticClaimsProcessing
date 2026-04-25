from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List

from pydantic import BaseModel, Field


class PolicyCategory(str, Enum):
    coding = "coding"
    validation = "validation"
    fraud = "fraud"


class PolicyRule(BaseModel):
    rule_id: str
    description: str
    severity: str
    conditions: Dict[str, Any]
    actions: List[str] = Field(default_factory=list)


class PolicyBundle(BaseModel):
    policy_id: str
    name: str
    category: PolicyCategory
    allowed_procedures: List[str]
    max_line_item_amount: float
    exceptions: Dict[str, Any] = Field(default_factory=dict)
    rules: List[PolicyRule] = Field(default_factory=list)
