# Models

This directory contains the bundled lightweight checkpoints used by the explicit legacy-derived adapter commands.

## Bundled Checkpoints

| Path | Used by | Notes |
| --- | --- | --- |
| `models/mpravae/best_val_corr_model.pth` | `predict-legacy-mpravae`, `design-legacy-mpravae` | Tomato four-tissue VAE + predictor checkpoint. The adapter architecture is implemented in `src/tomato_promoter_designer/legacy/mpravae_tomato.py`. |
| `models/deepseed/165_mpra_expr_denselstm.pth` | `predict-legacy-deepseed` | Scalar-expression DenseLSTM checkpoint retained from the deepseed workflow. |
| `models/deepseed/SeqRegressionModel.py` | `predict-legacy-deepseed` | Required class-definition file for loading the pickled deepseed PyTorch model. |

Checksums and status are recorded in `models/weights_manifest.json`.

## Important Boundary

Package-native commands do not require these files:

```bash
tomato-promoter-designer predict
tomato-promoter-designer design
```

The bundled checkpoints are used only by explicit legacy commands:

```bash
tomato-promoter-designer predict-legacy-mpravae
tomato-promoter-designer design-legacy-mpravae
tomato-promoter-designer predict-legacy-deepseed
```

If the model directory is moved outside the repository, set:

```bash
export TOMATO_PROMOTER_DESIGNER_MODELS_DIR=/path/to/models
```
