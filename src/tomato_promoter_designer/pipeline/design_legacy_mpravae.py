from __future__ import annotations

from pathlib import Path

from tomato_promoter_designer.io.schema import DesignResult, SequenceRecord
from tomato_promoter_designer.legacy.mpravae_tomato import MpraVAETomatoAdapter


def run_legacy_mpravae_design(
    records: list[SequenceRecord],
    target_tissue: str,
    checkpoint_path: str | Path | None = None,
    candidates: int = 5,
    seed: int = 20260708,
) -> list[DesignResult]:
    designer = MpraVAETomatoAdapter(checkpoint_path=checkpoint_path)
    return designer.design(records, target_tissue=target_tissue, candidates=candidates, seed=seed)
