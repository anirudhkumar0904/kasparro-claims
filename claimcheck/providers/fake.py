"""Scripted provider for controlled tests. It records every payload it is sent
so tests can assert what reached the "model"."""
from __future__ import annotations

import copy
import json
from typing import Any, Callable

from .base import ProviderError, ProviderResponse, ProviderTimeout, ToolCall

Step = Callable[[list[dict[str, Any]]], ProviderResponse] | ProviderResponse | Exception


def tool_call_response(*calls: tuple[str, dict[str, Any]]) -> ProviderResponse:
    tcs = [ToolCall(id=f"toolu_{i}", name=name, input=args) for i, (name, args) in enumerate(calls)]
    return ProviderResponse(
        text="",
        tool_calls=tcs,
        stop_reason="tool_use",
        assistant_content=[{"type": "tool_use", "id": t.id, "name": t.name, "input": t.input} for t in tcs],
    )


def text_response(text: str | dict, stop_reason: str = "end_turn") -> ProviderResponse:
    if isinstance(text, dict):
        text = json.dumps(text)
    return ProviderResponse(text=text, tool_calls=[], stop_reason=stop_reason,
                            assistant_content=[{"type": "text", "text": text}])


class FakeProvider:
    name = "fake"

    def __init__(self, steps: list[Step], model: str = "fake-model"):
        self.model = model
        self._steps = list(steps)
        self.calls: list[dict[str, Any]] = []

    def complete(self, *, system: str, messages: list[dict[str, Any]], tools: list[dict[str, Any]],
                 max_tokens: int, timeout_s: float) -> ProviderResponse:
        self.calls.append(copy.deepcopy({"system": system, "messages": messages, "tools": tools}))
        if not self._steps:
            raise ProviderError("fake provider has no scripted step left")
        step = self._steps.pop(0)
        if isinstance(step, Exception):
            raise step
        if callable(step):
            return step(messages)
        return step


class ScriptedByAnswer:
    """Builds a fresh FakeProvider per answer_id (for runner/API tests)."""

    def __init__(self, scripts: dict[str, list[Step]], default: list[Step] | None = None):
        self.scripts = scripts
        self.default = default
        self.providers: dict[str, FakeProvider] = {}

    def for_answer(self, answer_id: str) -> FakeProvider:
        steps = self.scripts.get(answer_id, self.default)
        if steps is None:
            steps = [ProviderTimeout("scripted timeout")]
        p = FakeProvider(copy.copy(steps))
        self.providers[answer_id] = p
        return p
