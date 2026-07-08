from __future__ import annotations

from tomato_promoter_designer.legacy.mpravae_tomato import DEFAULT_MPRAVAE_CHECKPOINT, MpraVAETomatoAdapter
from tomato_promoter_designer.io.schema import PredictionResult, SequenceRecord
from tomato_promoter_designer.models.expression_predictor import HeuristicExpressionPredictor


def _supports_legacy_mpravae(records: list[SequenceRecord]) -> bool:
    return DEFAULT_MPRAVAE_CHECKPOINT.exists() and all(
        len(record.sequence) == 165 and set(record.sequence).issubset({"A", "C", "G", "T"})
        for record in records
    )


def run_prediction(records: list[SequenceRecord]) -> list[PredictionResult]:
    if _supports_legacy_mpravae(records):
        try:
            return MpraVAETomatoAdapter().predict(records)
        except (FileNotFoundError, RuntimeError, ValueError):
            pass
    predictor = HeuristicExpressionPredictor()
    return predictor.predict(records)
