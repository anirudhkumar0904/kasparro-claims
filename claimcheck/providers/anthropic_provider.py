"""Live Anthropic Messages API provider with native tool calling."""
from __future__ import annotations

from typing import Any

import anthropic

from .base import ProviderError, ProviderNotConfigured, ProviderResponse, ProviderTimeout, ToolCall


class AnthropicProvider:
    name = "anthropic"

    def __init__(self, api_key: str, model: str, api_base: str, max_retries: int = 0):
        if not api_key:
            raise ProviderNotConfigured("ANTHROPIC_API_KEY is not configured")
        self.model = model
        # max_retries=0: a retry would silently add model calls beyond what the
        # trace shows; a failure becomes an answer-level error instead.
        self._client = anthropic.Anthropic(api_key=api_key, base_url=api_base, max_retries=max_retries)

    def complete(self, *, system: str, messages: list[dict[str, Any]], tools: list[dict[str, Any]],
                 max_tokens: int, timeout_s: float) -> ProviderResponse:
        try:
            resp = self._client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system,
                tools=tools,
                messages=messages,
                timeout=timeout_s,
            )
        except anthropic.APITimeoutError as exc:
            raise ProviderTimeout(f"provider request exceeded {timeout_s:.0f}s timeout") from exc
        except anthropic.APIStatusError as exc:
            raise ProviderError(f"provider returned HTTP {exc.status_code} ({type(exc).__name__})") from exc
        except anthropic.APIError as exc:
            raise ProviderError(f"provider request failed ({type(exc).__name__})") from exc

        text_parts: list[str] = []
        calls: list[ToolCall] = []
        content: list[dict[str, Any]] = []
        for block in resp.content:
            if block.type == "text":
                text_parts.append(block.text)
                content.append({"type": "text", "text": block.text})
            elif block.type == "tool_use":
                calls.append(ToolCall(id=block.id, name=block.name, input=block.input))
                content.append({"type": "tool_use", "id": block.id, "name": block.name, "input": block.input})
            # other block types (e.g. thinking) are not requested by this agent
        usage = {
            "input_tokens": getattr(resp.usage, "input_tokens", 0) or 0,
            "output_tokens": getattr(resp.usage, "output_tokens", 0) or 0,
        }
        return ProviderResponse(
            text="".join(text_parts),
            tool_calls=calls,
            stop_reason=resp.stop_reason or "",
            assistant_content=content,
            usage=usage,
        )
