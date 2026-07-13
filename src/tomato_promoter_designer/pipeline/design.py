from __future__ import annotations

from tomato_promoter_designer.io.schema import DesignResult, SequenceRecord
from tomato_promoter_designer.legacy.mpravae_tomato import DEFAULT_MPRAVAE_CHECKPOINT, MpraVAETomatoAdapter
from tomato_promoter_designer.models.generator import MotifPreservingDesigner


def _supports_legacy_mpravae(records: list[SequenceRecord]) -> bool:
    return DEFAULT_MPRAVAE_CHECKPOINT.exists() and all(
        len(record.sequence) == 165 and set(record.sequence).issubset({"A", "C", "G", "T"})
        for record in records
    )


def run_design(
    records: list[SequenceRecord],
    target_tissue: str,
    candidates: int = 5,
    seed: int | None = None,
) -> list[DesignResult]:
    if _supports_legacy_mpravae(records):
        try:
            designer = MpraVAETomatoAdapter()
            return designer.design(records, target_tissue=target_tissue, candidates=candidates, seed=seed or 42)
        except (FileNotFoundError, RuntimeError, ValueError):
            pass
    designer = MotifPreservingDesigner()
    return designer.design(records, target_tissue=target_tissue, candidates=candidates, seed=seed)
