import unittest
from pathlib import Path

from tomato_promoter_designer.io.schema import SequenceRecord
from tomato_promoter_designer.legacy.mpravae_tomato import (
    DEFAULT_MPRAVAE_CHECKPOINT,
    MpraVAETomatoAdapter,
    decode_one_hot,
    is_promoter_like,
    one_hot_encode,
    promoter_qc_summary,
)


class TestMpraVAELegacyAdapter(unittest.TestCase):
    def test_one_hot_roundtrip(self) -> None:
        sequence = "ACGTACGT"
        encoded = one_hot_encode(sequence)
        self.assertEqual(tuple(encoded.shape), (4, 8))
        self.assertEqual(decode_one_hot(encoded), sequence)

    def test_promoter_like_returns_bool(self) -> None:
        sequence = "A" * 60 + "TATATAA" + "C" * 60
        self.assertIsInstance(is_promoter_like(sequence), bool)

    def test_training_informed_qc_accepts_tomato_like_example(self) -> None:
        sequence = (
            "AAATTGTAACAAATAATACAAAATATTTGTGAATACTAATGATTTCCAAATGGGATACCTTTTTGTT"
            "GTAAATAAGTGGAAAGGCAAAGTAGATAAATTCGCCTTTCCTAAGTATCCTTTTGGTCACAATTTCCA"
            "AGAGAAAAGAACAGAAAAGAAAAGAGAGAA"
        )
        qc = promoter_qc_summary(sequence)
        self.assertTrue(qc["passes"])
        self.assertGreaterEqual(qc["gc_fraction"], 0.12)
        self.assertLessEqual(qc["gc_fraction"], 0.52)

    def test_mpravae_prediction_if_checkpoint_available(self) -> None:
        if not Path(DEFAULT_MPRAVAE_CHECKPOINT).exists():
            self.skipTest("Legacy MpraVAE checkpoint not available in this workspace.")

        adapter = MpraVAETomatoAdapter()
        results = adapter.predict(
            [
                SequenceRecord(
                    "seq1",
                    "AAATTGTAACAAATAATACAAAATATTTGTGAATACTAATGATTTCCAAATGGGATACCTTTTTGTTGTAAATAAGTGGAAAGGCAAAGTAGATAAATTCGCCTTTCCTAAGTATCCTTTTGGTCACAATTTCCAAGAGAAAAGAACAGAAAAGAAAAGAGAGAA",
                )
            ]
        )
        self.assertEqual(len(results), 1)
        self.assertIn(results[0].preferred_tissue, {"root", "stem", "leaf", "fruit"})

    def test_mpravae_prediction_is_deterministic_if_checkpoint_available(self) -> None:
        if not Path(DEFAULT_MPRAVAE_CHECKPOINT).exists():
            self.skipTest("Legacy MpraVAE checkpoint not available in this workspace.")

        adapter = MpraVAETomatoAdapter()
        record = SequenceRecord(
            "seq1",
            "AAATTGTAACAAATAATACAAAATATTTGTGAATACTAATGATTTCCAAATGGGATACCTTTTTGTTGTAAATAAGTGGAAAGGCAAAGTAGATAAATTCGCCTTTCCTAAGTATCCTTTTGGTCACAATTTCCAAGAGAAAAGAACAGAAAAGAAAAGAGAGAA",
        )
        first = adapter.predict([record])[0]
        second = adapter.predict([record])[0]
        self.assertEqual(first.to_dict(), second.to_dict())

    def test_mpravae_design_emits_novel_sequences_if_checkpoint_available(self) -> None:
        if not Path(DEFAULT_MPRAVAE_CHECKPOINT).exists():
            self.skipTest("Legacy MpraVAE checkpoint not available in this workspace.")

        adapter = MpraVAETomatoAdapter()
        record = SequenceRecord(
            "seq1",
            "AAATTGTAACAAATAATACAAAATATTTGTGAATACTAATGATTTCCAAATGGGATACCTTTTTGTTGTAAATAAGTGGAAAGGCAAAGTAGATAAATTCGCCTTTCCTAAGTATCCTTTTGGTCACAATTTCCAAGAGAAAAGAACAGAAAAGAAAAGAGAGAA",
        )
        results = adapter.design([record], target_tissue="fruit", candidates=2, seed=20260708)
        self.assertEqual(len(results), 2)
        self.assertTrue(any(result.designed_sequence != result.original_sequence for result in results))
        self.assertTrue(all(result.design_status for result in results))
        self.assertTrue(all(result.passes_qc for result in results))
        self.assertTrue(all(result.num_mutations > 0 for result in results))


if __name__ == "__main__":
    unittest.main()
