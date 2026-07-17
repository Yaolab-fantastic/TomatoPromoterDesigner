# Training Guide

This document describes the repository training entry point for the MpraVAE model-backed route.

The training code is intentionally lightweight and inspectable. It provides the model architecture, dataset reader, objective function and checkpoint writer needed to train a checkpoint compatible with:

```bash
tomato-promoter-designer predict-mpravae
tomato-promoter-designer design-mpravae
```

## Files

| File | Purpose |
| --- | --- |
| `src/tomato_promoter_designer/legacy/mpravae_tomato.py` | MpraVAE model architecture and prediction/design adapter |
| `src/tomato_promoter_designer/training/mpravae.py` | Training dataset, config loader and training loop |
| `scripts/train_mpravae.py` | Command-line training wrapper |
| `configs/training_mpravae.yaml` | Default training configuration |
| `data/raw/mpravae/training_set.csv` | Repository training table used by the default config |

## Training Data Format

The default training table uses one promoter sequence column and four tissue-associated target columns:

| Column | Meaning |
| --- | --- |
| `realB` | 165-bp promoter sequence containing only `A/C/G/T` |
| `expr_tissue_1` | Root-associated training target |
| `expr_tissue_2` | Stem-associated training target |
| `expr_tissue_3` | Leaf-associated training target |
| `expr_tissue_4` | Fruit-associated training target |

Rows with non-165-bp sequences, ambiguous bases or missing numeric targets are skipped by the training dataset loader.

## Full Training Command

```bash
PYTHONPATH=src python scripts/train_mpravae.py \
  --config configs/training_mpravae.yaml
```

By default this writes:

```text
models/mpravae/trained_mpravae_model.pth
models/mpravae/trained_mpravae_metrics.json
```

The checkpoint is a PyTorch `state_dict` for `JointPromoterModel`, so it can be used directly with the model-backed commands:

```bash
tomato-promoter-designer predict-mpravae \
  --input examples/demo_input.fasta \
  --checkpoint models/mpravae/trained_mpravae_model.pth \
  --output outputs/mpravae_predict.csv

tomato-promoter-designer design-mpravae \
  --input examples/demo_input.fasta \
  --target fruit \
  --checkpoint models/mpravae/trained_mpravae_model.pth \
  --output outputs/mpravae_design.csv
```

## Smoke Test

For a fast check that the training and loading path works:

```bash
make train-mpravae-smoke
```

This trains on eight rows for one epoch, writes a temporary checkpoint under `tmp/`, and immediately loads it through `predict-mpravae`.

## Training Objective

The training loop optimizes a combined loss:

```text
total loss =
  reconstruction_weight * sequence reconstruction loss
+ prediction_weight     * four-tissue score regression loss
+ kl_weight             * VAE KL divergence
```

The decoder reconstructs one-hot promoter sequences, and the predictor learns four continuous tissue-associated scores from the latent representation.

## Notes

The bundled checkpoint in `models/mpravae/best_val_corr_model.pth` is provided so users can run the model-backed route immediately. The training script documents how a compatible checkpoint can be regenerated or replaced with a newly trained checkpoint using the same architecture and output format.
