from __future__ import annotations

from pathlib import Path

from tomato_promoter_designer.visualization.legacy_svg import export_legacy_figure_bundle


def run_legacy_figure_export(
    output_dir: str | Path,
    mpravae_loss_history: str | Path | None = None,
    mpravae_designed_promoters: str | Path | None = None,
    mpravae_prediction_results: str | Path | None = None,
    deepseed_training_log: str | Path | None = None,
    mpravae_mutated_file: str | Path | None = None,
    mpravae_random_promoters: str | Path | None = None,
    mpravae_training_set: str | Path | None = None,
    dnabert_motif_summary: str | Path | None = None,
    dnabert_tfbs_dir: str | Path | None = None,
    deepseed_scatter_png: str | Path | None = None,
    mpravae_blast_dir: str | Path | None = None,
    mpravae_diversity_dir: str | Path | None = None,
) -> dict[str, object]:
    return export_legacy_figure_bundle(
        output_dir=output_dir,
        mpravae_loss_history=mpravae_loss_history,
        mpravae_designed_promoters=mpravae_designed_promoters,
        mpravae_prediction_results=mpravae_prediction_results,
        deepseed_training_log=deepseed_training_log,
        mpravae_mutated_file=mpravae_mutated_file,
        mpravae_random_promoters=mpravae_random_promoters,
        mpravae_training_set=mpravae_training_set,
        dnabert_motif_summary=dnabert_motif_summary,
        dnabert_tfbs_dir=dnabert_tfbs_dir,
        deepseed_scatter_png=deepseed_scatter_png,
        mpravae_blast_dir=mpravae_blast_dir,
        mpravae_diversity_dir=mpravae_diversity_dir,
    )
