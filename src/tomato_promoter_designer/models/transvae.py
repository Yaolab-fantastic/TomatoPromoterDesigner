from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class TransVAEAdapter:
    """Future integration point for the trained TransVAE backend."""

    model_name: str = "transvae_stub"
    weights_path: str | None = None

    def is_ready(self) -> bool:
        return self.weights_path is not None
