import unittest
from pathlib import Path

from tomato_promoter_designer.io.schema import SequenceRecord
from tomato_promoter_designer.legacy.deepseed_expression import (
    DEFAULT_DEEPSEED_CHECKPOINT,
    DeepSeedScalarExpressionPredictor,
    encode_sequence,
)


class TestLegacyAdapters(unittest.TestCase):
    def test_encode_sequence_shape(self) -> None:
        encoded = encode_sequence("ATCG")
        self.assertEqual(tuple(encoded.shape), (4, 4))
        self.assertEqual(float(encoded.sum().item()), 4.0)

    def test_deepseed_prediction_if_checkpoint_available(self) -> None:
        if not Path(DEFAULT_DEEPSEED_CHECKPOINT).exists():
            self.skipTest("Bundled deepseed checkpoint not available.")

        predictor = DeepSeedScalarExpressionPredictor()
        results = predictor.predict(
            [
                SequenceRecord(
                    "seq1",
                    "AAATTGTAACAAATAATACAAAATATTTGTGAATACTAATGATTTCCAAATGGGATACCTTTTTGTTGTAAATAAGTGGAAAGGCAAAGTAGATAAATTCGCCTTTCCTAAGTATCCTTTTGGTCACAATTTCCAAGAGAAAAGAACAGAAAAGAAAAGAGAGAA",
                )
            ]
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].backend, "deepseed_denselstm_scalar")


if __name__ == "__main__":
    unittest.main()
