"""Pydantic contracts for agent input/output and API payloads."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Label = Literal["supported", "contradicted", "unknown"]
AgentVersion = Literal["v1", "v2"]
Split = Literal["development", "check"]


class AgentInput(BaseModel):
    """Exactly the four fields the agent may see. Extra fields (gold spans,
    claim lists, labels, ...) are rejected rather than silently dropped."""
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=False)

    answer_id: str = Field(min_length=1, max_length=64)
    brand_id: str = Field(min_length=1, max_length=64)
    question: str = Field(min_length=1)
    ai_answer: str = Field(min_length=1)


class Claim(BaseModel):
    model_config = ConfigDict(extra="forbid")

    claim_id: str
    start_char: int = Field(ge=0)
    end_char: int = Field(gt=0)
    quote: str
    label: Label
    fact_ids: list[str]
    reason: str


class AgentOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    answer_id: str
    claims: list[Claim]


# ---- raw model output (before Python assigns offsets) -----------------------
class RawClaim(BaseModel):
    model_config = ConfigDict(extra="forbid")

    quote: str = Field(min_length=1)
    label: Label
    fact_ids: list[str]
    reason: str = Field(min_length=1, max_length=600)


class RawOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    answer_id: str
    claims: list[RawClaim]


# ---- API --------------------------------------------------------------------
class ClassifyRequest(AgentInput):
    agent_version: AgentVersion


class EvaluationRunRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    agent_version: AgentVersion
    split: Split
