from __future__ import annotations

from collections import Counter

from tomato_promoter_designer.io.schema import PredictionResult, SequenceRecord


class HeuristicExpressionPredictor:
    """A deterministic baseline scorer.

    This is intentionally simple: it keeps the software runnable while the
    trained tissue predictor is being integrated.
    """

    _motif_weights = {
        "root": {"CTATT": 1.0, "TTAAA": 0.4},
        "stem": {"TTTAT": 0.8, "ATTTT": 0.3},
        "leaf": {"CTATT": 0.3, "CAAAA": 0.4},
        "fruit": {"CAAAA": 1.2, "ATTTT": 0.8, "TTAAA": 0.2},
    }

    def predict(self, records: list[SequenceRecord]) -> list[PredictionResult]:
        return [self.predict_one(record) for record in records]

    def predict_one(self, record: SequenceRecord) -> PredictionResult:
        seq = record.sequence
        length = max(len(seq), 1)
        base_counts = Counter(seq)
        gc_ratio = (base_counts["G"] + base_counts["C"]) / length
        at_ratio = (base_counts["A"] + base_counts["T"]) / length
        poly_a = seq.count("AAAAA") / max(length - 4, 1)
        motif_counts = {motif: seq.count(motif) for motif in {"CAAAA", "CTATT", "ATTTT", "TTAAA", "TTTAT"}}

        root = 4.2 * gc_ratio + 2.0 * motif_counts["CTATT"] + 0.5 * motif_counts["TTAAA"]
        stem = 3.2 * at_ratio + 1.8 * motif_counts["TTTAT"] + 0.6 * motif_counts["ATTTT"]
        leaf = 2.5 * gc_ratio + 1.1 * motif_counts["CAAAA"] + 0.7 * motif_counts["CTATT"]
        fruit = 3.5 * at_ratio + 2.2 * motif_counts["CAAAA"] + 1.3 * motif_counts["ATTTT"] + 2.0 * poly_a

        scores = {
            "root": round(root, 4),
            "stem": round(stem, 4),
            "leaf": round(leaf, 4),
            "fruit": round(fruit, 4),
        }
        preferred_tissue = max(scores, key=scores.get)
        return PredictionResult(
            sequence_id=record.sequence_id,
            sequence=seq,
            expr_root=scores["root"],
            expr_stem=scores["stem"],
            expr_leaf=scores["leaf"],
            expr_fruit=scores["fruit"],
            preferred_tissue=preferred_tissue,
        )
