# Models

This directory contains the bundled lightweight checkpoints used by the explicit project model adapter commands.

## Bundled Checkpoints

| Path | Used by | Notes |
| --- | --- | --- |
| `models/mpravae/best_val_corr_model.pth` | `predict-mpravae`, `design-mpravae` | Tomato four-tissue VAE + predictor checkpoint. The adapter architecture is implemented in `src/tomato_promoter_designer/legacy/mpravae_tomato.py`. |
| `models/deepseed/165_mpra_expr_denselstm.pth` | `predict-deepseed` | Scalar-scoring DenseLSTM checkpoint from the project workflow. |
| `models/deepseed/SeqRegressionModel.py` | `predict-deepseed` | Required class-definition file for loading the pickled deepseed PyTorch model. |

Checksums and status are recorded in `models/weights_manifest.json`.

## Training Compatibility

The repository includes an MpraVAE training entry point:

```bash
PYTHONPATH=src python scripts/train_mpravae.py \
  --config configs/training_mpravae.yaml
```

The generated checkpoint is a `JointPromoterModel` state dictionary and can be used with `predict-mpravae` and `design-mpravae` through the `--checkpoint` option.

## Important Boundary

Package-native commands do not require these files:

```bash
tomato-promoter-designer predict
tomato-promoter-designer design
```

The bundled checkpoints are used only by explicit model adapter commands:

```bash
tomato-promoter-designer predict-mpravae
tomato-promoter-designer design-mpravae
tomato-promoter-designer predict-deepseed
```

Command names containing `legacy` are retained only as backward-compatible aliases for older scripts.

If the model directory is moved outside the repository, set:

```bash
export TOMATO_PROMOTER_DESIGNER_MODELS_DIR=/path/to/models
```
