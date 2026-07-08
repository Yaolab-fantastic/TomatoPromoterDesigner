# Figure Inventory

This repository now exposes two figure layers so the software can support both day-to-day tool use and paper-facing legacy result recovery.

## Modern pipeline figures

- `figures` on prediction CSV
  - output: `prediction_heatmap.svg`
  - purpose: tissue-wise score overview
- `figures` on design CSV
  - output: `design_summary.svg`
  - purpose: target-tissue margin and mutation burden comparison
- `figures` on DNABERT motif summary CSV
  - output: `motif_enrichment.svg`
  - purpose: top enriched motif ranking

## Legacy-style figure bundle

- `legacy-figures`
  - output: `mpravae_loss_dashboard.svg`
  - source: `../MpraVAE/code/transformerresult/results1/loss_curves/loss_history.csv`
  - purpose: training and validation loss summary
- `legacy-figures`
  - output: `mpravae_kmer_scatter.svg`
  - source: `../MpraVAE/results/designed_promoters.csv`
  - purpose: natural versus generated 4-mer distribution consistency
- `legacy-figures`
  - output: `mpravae_prediction_scatter.svg`
  - source: `../MpraVAE/results/generated_prediction_results.csv`
  - purpose: predicted versus true expression scatter
- `legacy-figures`
  - output: `deepseed_training_curve.svg`
  - source: `../deepseed/Predictor/results1/training_log165_mpra_expr_denselstm.csv`
  - purpose: legacy predictor optimization summary
- `legacy-figures`
  - output: `mpravae_edit_distance_diversity.svg`
  - source: `../MpraVAE/data/bianjijuli/mutated_file.csv` and `../MpraVAE/data/random_promoters_200.csv`
  - purpose: natural versus random versus generated promoter diversity comparison
- `legacy-figures`
  - output: `mpravae_semantic_space.svg`
  - source: `../MpraVAE/results/designed_promoters.csv` and `../MpraVAE/data/vaedata/training_set.csv`
  - purpose: deterministic semantic-space reconstruction contrasting natural and generated promoter manifolds
- `legacy-figures`
  - output: `dnabert_tfbs_assets/TFBS_*.png`
  - source: `../DNABERT/motif/result/6-2` or `../DNABERT/motif/result/6-3` plus motif summary ranking
  - purpose: collect original DNABERT TFBS logo assets into the unified repository outputs
- `legacy-figures`
  - output: `scatter_165_mpra_expr_denselstm.png`
  - source: `../deepseed/Predictor/results1/scatter_fig/`
  - purpose: preserve the original deepseed scatter figure asset
- `legacy-figures`
  - output: `blast/*.png`
  - source: `../MpraVAE/data/blast_result.txt` plus `../MpraVAE/data/sequences_with_id.csv`
  - purpose: rebuild BLAST validation figures with repository-safe labels and fonts
- `legacy-figures`
  - output: `bianjijuli/*.png`
  - source: `../MpraVAE/results/bianjijuli`
  - purpose: preserve original diversity validation figures

## Notes on visual continuity

- `mpravae_semantic_space.svg` intentionally replaces the old ad hoc `t-SNE` verification script with a deterministic `PCA on k-mer vectors` view.

This keeps the same biological question, whether generated promoters occupy a similar sequence manifold, while making the result much easier to reproduce inside the unified software package.
