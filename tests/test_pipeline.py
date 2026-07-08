import unittest

from tomato_promoter_designer.io.schema import SequenceRecord
from tomato_promoter_designer.pipeline.annotate import run_annotation
from tomato_promoter_designer.pipeline.design import run_design
from tomato_promoter_designer.pipeline.predict import run_prediction


class TestPipelines(unittest.TestCase):
    def setUp(self) -> None:
        self.records = [
            SequenceRecord(
                "seq1",
                "AAATTGTAACAAATAATACAAAATATTTGTGAATACTAATGATTTCCAAATGGGATACCTTTTTGTTGTAAATAAGTGGAAAGGCAAAGTAGATAAATTCGCCTTTCCTAAGTATCCTTTTGGTCACAATTTCCAAGAGAAAAGAACAGAAAAGAAAAGAGAGAA",
            )
        ]

    def test_annotation_returns_hits(self) -> None:
        hits = run_annotation(self.records)
        self.assertTrue(len(hits) >= 1)

    def test_prediction_returns_one_result(self) -> None:
        results = run_prediction(self.records)
        self.assertEqual(len(results), 1)
        self.assertIn(results[0].preferred_tissue, {"root", "stem", "leaf", "fruit"})

    def test_design_returns_ranked_candidates(self) -> None:
        results = run_design(self.records, target_tissue="fruit", candidates=2, seed=42)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].candidate_rank, 1)
        self.assertEqual(results[1].candidate_rank, 2)


if __name__ == "__main__":
    unittest.main()

