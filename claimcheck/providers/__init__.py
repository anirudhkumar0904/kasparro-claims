from typing import Callable

from .base import Provider, ProviderError, ProviderResponse, ProviderTimeout, ToolCall  # noqa: F401


class ProviderFactory:
    """Callable answer_id -> Provider that also records provider name/model
    for run metadata (a live run reuses one client; tests script per answer)."""

    def __init__(self, fn: Callable[[str], Provider], name: str, model: str):
        self._fn = fn
        self.name = name
        self.model = model

    def __call__(self, answer_id: str) -> Provider:
        return self._fn(answer_id)


def live_provider_factory(settings) -> ProviderFactory:
    provider = make_live_provider(settings)
    return ProviderFactory(lambda _aid: provider, provider.name, provider.model)


def make_live_provider(settings):
    """Build the configured live provider from settings + environment key."""
    from .. import config
    from .anthropic_provider import AnthropicProvider

    if settings.provider != "anthropic":
        raise ProviderError(f"unsupported provider {settings.provider!r}")
    return AnthropicProvider(api_key=config.api_key() or "", model=settings.model,
                             api_base=settings.api_base, max_retries=settings.sdk_max_retries)
