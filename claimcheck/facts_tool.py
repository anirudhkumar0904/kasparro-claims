"""Read-only fact lookup exposed to the model as get_brand_facts(brand_id)."""
from __future__ import annotations

from typing import Any

from . import config
from .data import Fact, load_facts

TOOL_NAME = "get_brand_facts"


class UnknownBrandError(LookupError):
    def __init__(self, brand_id: str):
        super().__init__(f"unknown brand_id {brand_id!r}")
        self.brand_id = brand_id


class FactStore:
    def __init__(self, facts: list[Fact] | None = None):
        self._facts = facts if facts is not None else load_facts()
        self._by_brand: dict[str, list[Fact]] = {}
        for f in self._facts:
            self._by_brand.setdefault(f.brand_id, []).append(f)
        self._by_id = {f.fact_id: f for f in self._facts}

    @property
    def brand_ids(self) -> list[str]:
        return sorted(self._by_brand)

    def has_brand(self, brand_id: str) -> bool:
        return brand_id in self._by_brand

    def fact(self, fact_id: str) -> Fact | None:
        return self._by_id.get(fact_id)

    def has_fact(self, fact_id: str) -> bool:
        return fact_id in self._by_id

    def get_brand_facts(self, brand_id: str) -> dict[str, Any]:
        if brand_id not in self._by_brand:
            raise UnknownBrandError(brand_id)
        return {
            "fact_version": config.FACT_VERSION,
            "brand_id": brand_id,
            "facts": [f.as_tool_row() for f in self._by_brand[brand_id]],
        }

    def tool_spec(self) -> dict[str, Any]:
        """Provider-neutral JSON-schema tool definition."""
        return {
            "name": TOOL_NAME,
            "description": (
                "Read-only lookup of the official product catalogue. Returns every fact row "
                f"(fact_version {config.FACT_VERSION}) for one brand: fact_id, model_id, field, "
                "typed value, unit, condition and validity dates. Call once per brand you need, "
                "including any other brand mentioned in a comparison."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "brand_id": {
                        "type": "string",
                        "enum": self.brand_ids,
                        "description": "Lowercase brand identifier.",
                    }
                },
                "required": ["brand_id"],
                "additionalProperties": False,
            },
        }
