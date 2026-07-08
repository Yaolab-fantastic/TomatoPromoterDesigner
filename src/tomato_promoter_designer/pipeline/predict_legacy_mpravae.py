from __future__ import annotations

from pathlib import Path

from tomato_promoter_designer.io.schema import PredictionResult, SequenceRecord
from tomato_promoter_designer.legacy.mpravae_tomato import MpraVAETomatoAdapter


def run_legacy_mpravae_prediction(
    records: list[SequenceRecord],
    checkpoint_path: str | Path | None = None,
) -> list[PredictionResult]:
    predictor = MpraVAETomatoAdapter(checkpoint_path=checkpoint_path)
    return predictor.predict(records)
