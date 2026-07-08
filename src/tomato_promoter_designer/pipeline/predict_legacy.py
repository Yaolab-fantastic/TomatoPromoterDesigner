from __future__ import annotations

from pathlib import Path

from tomato_promoter_designer.io.schema import LegacyPredictionResult, SequenceRecord
from tomato_promoter_designer.legacy.deepseed_expression import (
    DeepSeedScalarExpressionPredictor,
)


def run_legacy_prediction(
    records: list[SequenceRecord],
    checkpoint_path: str | Path | None = None,
) -> list[LegacyPredictionResult]:
    predictor = DeepSeedScalarExpressionPredictor(checkpoint_path=checkpoint_path)
    return predictor.predict(records)
