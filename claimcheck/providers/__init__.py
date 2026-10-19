from typing import Callable

from .base import Provider, ProviderError, ProviderResponse, ProviderTimeout, ToolCall  # noqa: F401


class ProviderFactory:
    """Callable answer_id -> Provider that also records provider name/model
    for run metadata (a live run reuses one client; tests script per answer)."""

    def __init__(self, fn: Callable[[str], Provider], name: str, model: str,
                 preflight: Callable[[], None] | None = None):
        self._fn = fn
        self.name = name
        self.model = model
        self._preflight = preflight

    def __call__(self, answer_id: str) -> Provider:
        return self._fn(answer_id)

    def preflight(self) -> None:
        """Raise ProviderError early (e.g. missing API key) before any work starts."""
        if self._preflight is not None:
            self._preflight()


def live_provider_factory(settings) -> ProviderFactory:
    """Lazily builds one live client, so a missing key surfaces as a ProviderError
    inside the request (mapped to 502) instead of failing dependency injection."""
    cache: dict[str, Provider] = {}

    def get(_aid: str = "") -> Provider:
        if "p" not in cache:
            cache["p"] = make_live_provider(settings)
        return cache["p"]

    return ProviderFactory(get, settings.provider, settings.model, preflight=lambda: get())


def make_live_provider(settings):
    """Build the configured live provider from settings + environment key."""
    from .. import config
    from .anthropic_provider import AnthropicProvider

    if settings.provider != "anthropic":
        raise ProviderError(f"unsupported provider {settings.provider!r}")
    return AnthropicProvider(api_key=config.api_key() or "", model=settings.model,
                             api_base=settings.api_base, max_retries=settings.sdk_max_retries)
