import unittest

from tomato_promoter_designer.io.schema import SequenceRecord, validate_records
from tomato_promoter_designer.preprocessing.kmer_encode import seq_to_kmers


class TestIOAndSchema(unittest.TestCase):
    def test_validate_records_normalizes_case(self) -> None:
        records = [SequenceRecord("seq1", "acgttt")]
        validated = validate_records(records)
        self.assertEqual(validated[0].sequence, "ACGTTT")

    def test_seq_to_kmers(self) -> None:
        self.assertEqual(seq_to_kmers("ACGT", 2), ["AC", "CG", "GT"])


if __name__ == "__main__":
    unittest.main()

