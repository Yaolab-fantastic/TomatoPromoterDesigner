import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from tomato_promoter_designer.legacy.dnabert_motif import (
    analyze_attention_dataset,
    kmer2seq,
    read_dnabert_dev_tsv,
    run_dnabert_legacy_annotation,
)


class TestDNABERTLegacyAdapter(unittest.TestCase):
    def test_kmer2seq(self) -> None:
        self.assertEqual(kmer2seq("ATC TCG CGA"), "ATCGA")

    def test_small_attention_analysis(self) -> None:
        dataset = read_dnabert_dev_tsv(self._write_dev_tsv())
        attention = np.array(
            [
                [0.01, 0.01, 0.6, 0.7, 0.8, 0.7, 0.01, 0.01],
                [0.01, 0.01, 0.6, 0.7, 0.8, 0.7, 0.01, 0.01],
                [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
                [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
            ],
            dtype=float,
        )
        motif_records, labeled_sequences, metadata = analyze_attention_dataset(
            dataset,
            attention_scores=attention,
            window_size=4,
            min_len=3,
            p_value_cutoff=0.5,
            min_n_motif=2,
        )
        self.assertEqual(metadata["num_positive_sequences"], 2)
        self.assertTrue(len(motif_records) >= 1)
        self.assertEqual(len(labeled_sequences), 2)
        self.assertIn("M", labeled_sequences[0].labeled_sequence)

    def test_run_annotation_writes_outputs(self) -> None:
        dev_tsv = self._write_dev_tsv()
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "out"
            atten_path = Path(temp_dir) / "atten.npy"
            np.save(
                atten_path,
                np.array(
                    [
                        [0.01, 0.01, 0.6, 0.7, 0.8, 0.7, 0.01, 0.01],
                        [0.01, 0.01, 0.6, 0.7, 0.8, 0.7, 0.01, 0.01],
                        [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
                        [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
                    ],
                    dtype=float,
                ),
            )
            metadata = run_dnabert_legacy_annotation(
                dev_tsv_path=dev_tsv,
                attention_scores_path=atten_path,
                output_dir=output_dir,
                window_size=4,
                min_len=3,
                p_value_cutoff=0.5,
                min_n_motif=2,
            )
            self.assertTrue((output_dir / "motif_summary.csv").exists())
            self.assertTrue((output_dir / "processed_sequences.csv").exists())
            self.assertTrue((output_dir / "run_metadata.json").exists())
            self.assertEqual(json.loads((output_dir / "run_metadata.json").read_text())["num_positive_sequences"], 2)
            self.assertEqual(metadata["num_negative_sequences"], 2)

    def _write_dev_tsv(self) -> Path:
        temp_dir = tempfile.mkdtemp()
        path = Path(temp_dir) / "dev.tsv"
        path.write_text(
            "sequence\tlabel\n"
            "AAA AAC ACG CGT GTT TTA\t1\n"
            "AAA AAC ACG CGT GTT TTA\t1\n"
            "CCC CCG CGA GAA AAA AAT\t0\n"
            "GGG GGA GAT ATT TTT TTA\t0\n",
            encoding="utf-8",
        )
        return path


if __name__ == "__main__":
    unittest.main()
