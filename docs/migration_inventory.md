# Migration Inventory

## Summary

The current `TomatoPromoterDesigner` repository now has a clean package structure, but the legacy research codebases are at different levels of migration readiness. This document records what was inspected and what can be integrated next without guesswork.

## MpraVAE

- relevant paths:
  - `../MpraVAE/code/TransVAE.py`
  - `../MpraVAE/code/transformervae.py`
  - `../MpraVAE/code/generate.py`
  - `../MpraVAE/code/model.py`
- useful assets already present:
  - multiple `.pth` files under `../MpraVAE/code/models*` and `../MpraVAE/model/`
  - tomato-oriented training tables under `../MpraVAE/data/vaedata/`
- assessment:
  - `transformervae.py` contains the strongest link to the current tomato multi-tissue framing
  - the file is not yet cleanly reusable as a package module and appears internally inconsistent
  - `TransVAE.py` is a large standalone implementation that will require a focused adapter rather than direct copying
  - `vaecnn.py` provides a cleaner tomato multi-tissue VAE + predictor architecture and is now the practical migration base
- migration priority:
  - medium-high scientific relevance
  - medium-low short-term ease of integration

## DNABERT

- relevant paths:
  - `../DNABERT/motif/find_motifs.py`
  - `../DNABERT/motif/motif_utils.py`
  - `../DNABERT/motif/motif-biaozhu.py`
  - `../DNABERT/examples/run_finetune.py`
  - `../DNABERT/examples/visualize.py`
- useful assets already present:
  - post-attention motif analysis code is fairly self-contained
  - attention-based motif discovery logic is reusable after upstream score generation
- assessment:
  - downstream motif processing is reusable
  - upstream inference still depends on a DNABERT model directory, tokenizer, and attention export workflow that are not yet packaged here
  - the new repository now contains a dependency-light migrated post-processing adapter for `dev.tsv + atten.npy`
  - when strict filtering returns no motifs, the adapter now emits a clearly flagged ranked-candidate fallback summary
- migration priority:
  - high for interpretability and manuscript story
  - medium short-term integration effort

## deepseed

- relevant paths:
  - `../deepseed/Predictor/promoter_predictor.py`
  - `../deepseed/Predictor/SeqRegressionModel.py`
  - `../deepseed/Generatorme/preGAN_expr.py`
- useful assets already present:
  - scalar-expression checkpoint at `../deepseed/Predictor/results/model/165_mpra_expr_denselstm.pth`
- assessment:
  - the predictor is the cleanest immediately runnable legacy model
  - it predicts a single scalar expression output, not the four-tissue tomato target currently used by the baseline predictor
  - the generator code exists, but checkpointing and packaging are much less straightforward
- migration priority:
  - highest short-term integration readiness
  - lower direct alignment with the final tomato tissue-specific software story

## What has now been integrated

- `predict-legacy-deepseed` CLI route
- `legacy/deepseed_expression.py` adapter
- `annotate-legacy-dnabert` CLI route
- `legacy/dnabert_motif.py` adapter
- `predict-legacy-mpravae` CLI route
- `design-legacy-mpravae` CLI route
- `legacy/mpravae_tomato.py` adapter
- weights manifest entry for the legacy deepseed scalar predictor

## Recommended next migration sequence

1. replace the current baseline `predict` and `design` routes with validated real-model defaults once behavior is benchmarked
2. decide whether to keep the current `vaecnn`-style tomato adapter or continue to a fuller `TransVAE` migration
3. decide whether the deepseed generator is scientifically necessary for the final paper or should remain a provenance-only legacy component
