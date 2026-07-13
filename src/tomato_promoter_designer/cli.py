from __future__ import annotations

import argparse
import json
from pathlib import Path

from tomato_promoter_designer.io.csv import write_dict_rows
from tomato_promoter_designer.io.fasta import read_fasta
from tomato_promoter_designer.pipeline.design_legacy_mpravae import (
    run_legacy_mpravae_design,
)
from tomato_promoter_designer.pipeline.annotate_legacy_dnabert import (
    run_legacy_dnabert_motif_annotation,
)
from tomato_promoter_designer.pipeline.annotate import run_annotation
from tomato_promoter_designer.pipeline.design import run_design
from tomato_promoter_designer.pipeline.predict_legacy_mpravae import (
    run_legacy_mpravae_prediction,
)
from tomato_promoter_designer.pipeline.predict_legacy import run_legacy_prediction
from tomato_promoter_designer.pipeline.predict import run_prediction
from tomato_promoter_designer.pipeline.figures import run_figure_export
from tomato_promoter_designer.pipeline.legacy_figures import run_legacy_figure_export
from tomato_promoter_designer.pipeline.report import build_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tomato-promoter-designer",
        description="Motif-aware tissue-biased tomato promoter design toolkit.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    annotate = subparsers.add_parser("annotate", help="Annotate motif hits in promoter FASTA input.")
    annotate.add_argument("--input", required=True, help="Input FASTA file.")
    annotate.add_argument("--output", required=True, help="Output CSV path.")

    annotate_dnabert = subparsers.add_parser(
        "annotate-legacy-dnabert",
        help="Run the migrated DNABERT attention-to-motif post-processing workflow.",
    )
    annotate_dnabert.add_argument("--dev-tsv", required=True, help="DNABERT dev.tsv file with k-mer sequences and labels.")
    annotate_dnabert.add_argument("--atten-npy", required=True, help="Attention score array exported by DNABERT.")
    annotate_dnabert.add_argument("--output-dir", required=True, help="Output directory for motif summary and labeled sequences.")
    annotate_dnabert.add_argument("--window-size", type=int, default=24)
    annotate_dnabert.add_argument("--min-len", type=int, default=5)
    annotate_dnabert.add_argument("--pval-cutoff", type=float, default=0.005)
    annotate_dnabert.add_argument("--min-n-motif", type=int, default=3)

    predict = subparsers.add_parser(
        "predict",
        help="Predict tissue-biased expression scores, auto-preferring the real MpraVAE backend.",
    )
    predict.add_argument("--input", required=True, help="Input FASTA file.")
    predict.add_argument("--output", required=True, help="Output CSV path.")

    predict_mpravae = subparsers.add_parser(
        "predict-legacy-mpravae",
        help="Run the migrated MpraVAE tomato four-tissue predictor.",
    )
    predict_mpravae.add_argument("--input", required=True, help="Input FASTA file.")
    predict_mpravae.add_argument("--output", required=True, help="Output CSV path.")
    predict_mpravae.add_argument("--checkpoint", required=False, help="Optional path to an MpraVAE tomato checkpoint.")

    predict_legacy = subparsers.add_parser(
        "predict-legacy",
        aliases=["predict-legacy-deepseed"],
        help="Run the migrated legacy deepseed scalar-expression predictor.",
    )
    predict_legacy.add_argument("--input", required=True, help="Input FASTA file.")
    predict_legacy.add_argument("--output", required=True, help="Output CSV path.")
    predict_legacy.add_argument(
        "--checkpoint",
        required=False,
        help="Optional path to a legacy deepseed checkpoint.",
    )

    design = subparsers.add_parser(
        "design",
        help="Generate designed candidates, auto-preferring the real MpraVAE backend.",
    )
    design.add_argument("--input", required=True, help="Input FASTA file.")
    design.add_argument("--target", required=True, choices=["root", "stem", "leaf", "fruit"])
    design.add_argument("--candidates", type=int, default=5, help="Number of ranked candidates to emit per input sequence.")
    design.add_argument("--seed", type=int, default=42, help="Random seed for deterministic design.")
    design.add_argument("--output", required=True, help="Output CSV path.")

    design_mpravae = subparsers.add_parser(
        "design-legacy-mpravae",
        help="Run the migrated MpraVAE latent-space design workflow.",
    )
    design_mpravae.add_argument("--input", required=True, help="Input FASTA file.")
    design_mpravae.add_argument("--target", required=True, choices=["root", "stem", "leaf", "fruit"])
    design_mpravae.add_argument("--candidates", type=int, default=5)
    design_mpravae.add_argument("--seed", type=int, default=42)
    design_mpravae.add_argument("--output", required=True, help="Output CSV path.")
    design_mpravae.add_argument("--checkpoint", required=False, help="Optional path to an MpraVAE tomato checkpoint.")

    report = subparsers.add_parser("report", help="Build a compact JSON report from a design CSV.")
    report.add_argument("--input", required=True, help="Input design CSV.")
    report.add_argument("--output", required=True, help="Output JSON.")

    figures = subparsers.add_parser("figures", help="Export publication-style SVG figures from result CSV tables.")
    figures.add_argument("--input", required=True, help="Input CSV from predict, design, or motif summary.")
    figures.add_argument("--output-dir", required=True, help="Output directory for SVG figure files.")
    figures.add_argument("--top-n", type=int, default=15, help="Maximum number of motif rows to render for motif summary figures.")

    legacy_figures = subparsers.add_parser(
        "legacy-figures",
        help="Export legacy paper-style SVG figures from migrated deepseed and MpraVAE result files.",
    )
    legacy_figures.add_argument("--output-dir", required=True, help="Output directory for legacy SVG figure files.")
    legacy_figures.add_argument("--mpravae-loss-history", required=False, help="Optional MpraVAE loss_history.csv path.")
    legacy_figures.add_argument("--mpravae-designed-promoters", required=False, help="Optional designed_promoters.csv path.")
    legacy_figures.add_argument("--mpravae-prediction-results", required=False, help="Optional generated_prediction_results.csv path.")
    legacy_figures.add_argument("--deepseed-training-log", required=False, help="Optional deepseed training log CSV path.")
    legacy_figures.add_argument("--mpravae-mutated-file", required=False, help="Optional MpraVAE mutated_file.csv path for edit-distance diversity.")
    legacy_figures.add_argument("--mpravae-random-promoters", required=False, help="Optional MpraVAE random_promoters_200.csv path for edit-distance diversity.")
    legacy_figures.add_argument("--mpravae-training-set", required=False, help="Optional MpraVAE training_set.csv path for semantic-space reconstruction.")
    legacy_figures.add_argument("--dnabert-motif-summary", required=False, help="Optional DNABERT motif_summary.csv path for collecting TFBS assets.")
    legacy_figures.add_argument("--dnabert-tfbs-dir", required=False, help="Optional DNABERT TFBS PNG directory.")
    legacy_figures.add_argument("--deepseed-scatter-png", required=False, help="Optional deepseed legacy scatter PNG path to copy into the bundle.")
    legacy_figures.add_argument("--mpravae-blast-dir", required=False, help="Optional MpraVAE blast PNG directory to collect.")
    legacy_figures.add_argument("--mpravae-diversity-dir", required=False, help="Optional MpraVAE legacy diversity PNG directory to collect.")

    validate = subparsers.add_parser("validate-input", help="Validate FASTA content and print a small summary.")
    validate.add_argument("--input", required=True, help="Input FASTA file.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "validate-input":
        records = read_fasta(args.input)
        summary = {
            "num_records": len(records),
            "min_length": min(len(record.sequence) for record in records),
            "max_length": max(len(record.sequence) for record in records),
        }
        print(json.dumps(summary, indent=2))
        return 0

    if args.command == "annotate-legacy-dnabert":
        metadata = run_legacy_dnabert_motif_annotation(
            dev_tsv_path=args.dev_tsv,
            attention_scores_path=args.atten_npy,
            output_dir=args.output_dir,
            window_size=args.window_size,
            min_len=args.min_len,
            p_value_cutoff=args.pval_cutoff,
            min_n_motif=args.min_n_motif,
        )
        print(json.dumps(metadata, indent=2))
        return 0

    if args.command in {"annotate", "predict", "predict-legacy", "predict-legacy-deepseed", "predict-legacy-mpravae", "design", "design-legacy-mpravae"}:
        records = read_fasta(args.input)

    if args.command == "annotate":
        hits = run_annotation(records)
        rows = [hit.to_dict() for hit in hits]
        if not rows:
            rows = [
                {
                    "sequence_id": record.sequence_id,
                    "motif": "none",
                    "start": -1,
                    "end": -1,
                    "score": 0.0,
                }
                for record in records
            ]
        write_dict_rows(rows, args.output)
        return 0

    if args.command == "predict":
        predictions = run_prediction(records)
        write_dict_rows([item.to_dict() for item in predictions], args.output)
        return 0

    if args.command == "predict-legacy-mpravae":
        predictions = run_legacy_mpravae_prediction(records, checkpoint_path=args.checkpoint)
        write_dict_rows([item.to_dict() for item in predictions], args.output)
        return 0

    if args.command in {"predict-legacy", "predict-legacy-deepseed"}:
        predictions = run_legacy_prediction(records, checkpoint_path=args.checkpoint)
        write_dict_rows([item.to_dict() for item in predictions], args.output)
        return 0

    if args.command == "design":
        designs = run_design(records, target_tissue=args.target, candidates=args.candidates, seed=args.seed)
        write_dict_rows([item.to_dict() for item in designs], args.output)
        return 0

    if args.command == "design-legacy-mpravae":
        designs = run_legacy_mpravae_design(
            records,
            target_tissue=args.target,
            checkpoint_path=args.checkpoint,
            candidates=args.candidates,
            seed=args.seed,
        )
        write_dict_rows([item.to_dict() for item in designs], args.output)
        return 0

    if args.command == "report":
        report = build_report(args.input, args.output)
        print(json.dumps(report, indent=2))
        return 0

    if args.command == "figures":
        manifest = run_figure_export(args.input, args.output_dir, top_n=args.top_n)
        print(json.dumps(manifest, indent=2))
        return 0

    if args.command == "legacy-figures":
        manifest = run_legacy_figure_export(
            output_dir=args.output_dir,
            mpravae_loss_history=args.mpravae_loss_history,
            mpravae_designed_promoters=args.mpravae_designed_promoters,
            mpravae_prediction_results=args.mpravae_prediction_results,
            deepseed_training_log=args.deepseed_training_log,
            mpravae_mutated_file=args.mpravae_mutated_file,
            mpravae_random_promoters=args.mpravae_random_promoters,
            mpravae_training_set=args.mpravae_training_set,
            dnabert_motif_summary=args.dnabert_motif_summary,
            dnabert_tfbs_dir=args.dnabert_tfbs_dir,
            deepseed_scatter_png=args.deepseed_scatter_png,
            mpravae_blast_dir=args.mpravae_blast_dir,
            mpravae_diversity_dir=args.mpravae_diversity_dir,
        )
        print(json.dumps(manifest, indent=2))
        return 0

    raise RuntimeError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
