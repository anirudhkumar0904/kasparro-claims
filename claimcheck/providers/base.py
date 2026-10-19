"""Provider-neutral response types and errors.

Messages use the Anthropic message shape internally (role + content blocks of
type text / tool_use / tool_result) because that is the live provider; the
fake provider consumes the same shape.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


class ProviderError(Exception):
    """Provider failure. `message` must already be sanitized (no keys/bodies)."""

    error_type = "provider_error"

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ProviderTimeout(ProviderError):
    error_type = "provider_timeout"


@dataclass
class ToolCall:
    id: str
    name: str
    input: Any


@dataclass
class ProviderResponse:
    text: str
    tool_calls: list[ToolCall]
    stop_reason: str
    assistant_content: list[dict[str, Any]]
    usage: dict[str, int] = field(default_factory=dict)


class Provider(Protocol):
    name: str
    model: str

    def complete(self, *, system: str, messages: list[dict[str, Any]], tools: list[dict[str, Any]],
                 max_tokens: int, timeout_s: float) -> ProviderResponse: ...
