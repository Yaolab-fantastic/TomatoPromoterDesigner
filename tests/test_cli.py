import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np


class TestCLI(unittest.TestCase):
    def test_validate_input_command(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        env = os.environ.copy()
        env["PYTHONPATH"] = str(repo_root / "src")
        fasta_path = repo_root / "examples" / "demo_input.fasta"
        cmd = [
            sys.executable,
            "-m",
            "tomato_promoter_designer.cli",
            "validate-input",
            "--input",
            str(fasta_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, env=env, check=True)
        parsed = json.loads(result.stdout)
        self.assertEqual(parsed["num_records"], 2)

    def test_annotate_command_writes_output(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        env = os.environ.copy()
        env["PYTHONPATH"] = str(repo_root / "src")
        fasta_path = repo_root / "examples" / "demo_input.fasta"
        output_path = repo_root / "tmp" / "annotate_cli_test.csv"
        if output_path.exists():
            output_path.unlink()

        cmd = [
            sys.executable,
            "-m",
            "tomato_promoter_designer.cli",
            "annotate",
            "--input",
            str(fasta_path),
            "--output",
            str(output_path),
        ]
        subprocess.run(cmd, capture_output=True, text=True, env=env, check=True)
        self.assertTrue(output_path.exists())
        output_path.unlink()

    def test_predict_legacy_deepseed_command_writes_output(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        checkpoint_path = repo_root / "models" / "deepseed" / "165_mpra_expr_denselstm.pth"
        module_dir = repo_root / "models" / "deepseed"
        if not checkpoint_path.exists():
            self.skipTest("Bundled deepseed checkpoint not available.")

        env = os.environ.copy()
        env["PYTHONPATH"] = str(repo_root / "src")
        fasta_path = repo_root / "examples" / "demo_input.fasta"
        output_path = repo_root / "tmp" / "predict_legacy_cli_test.csv"
        if output_path.exists():
            output_path.unlink()

        cmd = [
            sys.executable,
            "-m",
            "tomato_promoter_designer.cli",
            "predict-legacy-deepseed",
            "--input",
            str(fasta_path),
            "--output",
            str(output_path),
            "--checkpoint",
            str(checkpoint_path),
            "--module-dir",
            str(module_dir),
        ]
        subprocess.run(cmd, capture_output=True, text=True, env=env, check=True)
        self.assertTrue(output_path.exists())
        output_path.unlink()

    def test_predict_legacy_mpravae_command_writes_output(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        checkpoint_path = repo_root / "models" / "mpravae" / "best_val_corr_model.pth"
        if not checkpoint_path.exists():
            self.skipTest("Bundled MpraVAE checkpoint not available.")

        env = os.environ.copy()
        env["PYTHONPATH"] = str(repo_root / "src")
        fasta_path = repo_root / "examples" / "demo_input.fasta"
        output_path = repo_root / "tmp" / "predict_legacy_mpravae_cli_test.csv"
        if output_path.exists():
            output_path.unlink()

        cmd = [
            sys.executable,
            "-m",
            "tomato_promoter_designer.cli",
            "predict-legacy-mpravae",
            "--input",
            str(fasta_path),
            "--output",
            str(output_path),
            "--checkpoint",
            str(checkpoint_path),
        ]
        subprocess.run(cmd, capture_output=True, text=True, env=env, check=True)
        self.assertTrue(output_path.exists())
        output_path.unlink()

    def test_design_legacy_mpravae_command_writes_output(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        checkpoint_path = repo_root / "models" / "mpravae" / "best_val_corr_model.pth"
        if not checkpoint_path.exists():
            self.skipTest("Bundled MpraVAE checkpoint not available.")

        env = os.environ.copy()
        env["PYTHONPATH"] = str(repo_root / "src")
        fasta_path = repo_root / "examples" / "demo_input.fasta"
        output_path = repo_root / "tmp" / "design_legacy_mpravae_cli_test.csv"
        if output_path.exists():
            output_path.unlink()

        cmd = [
            sys.executable,
            "-m",
            "tomato_promoter_designer.cli",
            "design-legacy-mpravae",
            "--input",
            str(fasta_path),
            "--target",
            "fruit",
            "--candidates",
            "2",
            "--output",
            str(output_path),
            "--checkpoint",
            str(checkpoint_path),
        ]
        subprocess.run(cmd, capture_output=True, text=True, env=env, check=True)
        self.assertTrue(output_path.exists())
        content = output_path.read_text(encoding="utf-8")
        self.assertIn("design_status", content)
        output_path.unlink()

    def test_annotate_legacy_dnabert_command_writes_outputs(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        env = os.environ.copy()
        env["PYTHONPATH"] = str(repo_root / "src")

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            dev_tsv = temp_path / "dev.tsv"
            atten_npy = temp_path / "atten.npy"
            output_dir = temp_path / "out"
            dev_tsv.write_text(
                "sequence\tlabel\n"
                "AAA AAC ACG CGT GTT TTA\t1\n"
                "AAA AAC ACG CGT GTT TTA\t1\n"
                "CCC CCG CGA GAA AAA AAT\t0\n"
                "GGG GGA GAT ATT TTT TTA\t0\n",
                encoding="utf-8",
            )
            np.save(
                atten_npy,
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

            cmd = [
                sys.executable,
                "-m",
                "tomato_promoter_designer.cli",
                "annotate-legacy-dnabert",
                "--dev-tsv",
                str(dev_tsv),
                "--atten-npy",
                str(atten_npy),
                "--output-dir",
                str(output_dir),
                "--window-size",
                "4",
                "--min-len",
                "3",
                "--pval-cutoff",
                "0.5",
                "--min-n-motif",
                "2",
            ]
            subprocess.run(cmd, capture_output=True, text=True, env=env, check=True)
            self.assertTrue((output_dir / "motif_summary.csv").exists())
            self.assertTrue((output_dir / "processed_sequences.csv").exists())

    def test_figures_command_writes_svg(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        env = os.environ.copy()
        env["PYTHONPATH"] = str(repo_root / "src")

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            input_csv = temp_path / "predict.csv"
            output_dir = temp_path / "figures"
            input_csv.write_text(
                "sequence_id,sequence,expr_root,expr_stem,expr_leaf,expr_fruit,preferred_tissue\n"
                "seq1,ACGT,1.0,2.0,1.5,0.8,stem\n",
                encoding="utf-8",
            )
            cmd = [
                sys.executable,
                "-m",
                "tomato_promoter_designer.cli",
                "figures",
                "--input",
                str(input_csv),
                "--output-dir",
                str(output_dir),
            ]
            subprocess.run(cmd, capture_output=True, text=True, env=env, check=True)
            self.assertTrue((output_dir / "prediction_heatmap.svg").exists())
            self.assertTrue((output_dir / "manifest.json").exists())

    def test_legacy_figures_command_writes_svg(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        env = os.environ.copy()
        env["PYTHONPATH"] = str(repo_root / "src")

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            output_dir = temp_path / "legacy_figures"
            cmd = [
                sys.executable,
                "-m",
                "tomato_promoter_designer.cli",
                "legacy-figures",
                "--output-dir",
                str(output_dir),
                "--mpravae-loss-history",
                str(repo_root / "data" / "raw" / "mpravae" / "loss_history.csv"),
                "--mpravae-designed-promoters",
                str(repo_root / "data" / "raw" / "mpravae" / "designed_promoters.csv"),
                "--mpravae-prediction-results",
                str(repo_root / "data" / "raw" / "mpravae" / "generated_prediction_results.csv"),
                "--deepseed-training-log",
                str(repo_root / "data" / "raw" / "deepseed" / "training_log165_mpra_expr_denselstm.csv"),
                "--mpravae-mutated-file",
                str(repo_root / "data" / "raw" / "mpravae" / "mutated_file.csv"),
                "--mpravae-random-promoters",
                str(repo_root / "data" / "raw" / "mpravae" / "random_promoters_200.csv"),
                "--mpravae-training-set",
                str(repo_root / "data" / "raw" / "mpravae" / "training_set.csv"),
                "--dnabert-motif-summary",
                str(repo_root / "data" / "processed" / "dnabert_legacy" / "motif_summary.csv"),
                "--dnabert-tfbs-dir",
                str(repo_root / "data" / "raw" / "dnabert" / "tfbs_assets"),
            ]
            subprocess.run(cmd, capture_output=True, text=True, env=env, check=True)
            self.assertTrue((output_dir / "manifest.json").exists())
            self.assertTrue((output_dir / "mpravae_loss_dashboard.svg").exists())
            self.assertTrue((output_dir / "mpravae_edit_distance_diversity.svg").exists())
            self.assertTrue((output_dir / "mpravae_semantic_space.svg").exists())


if __name__ == "__main__":
    unittest.main()
