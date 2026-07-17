# TomatoPromoterDesigner

TomatoPromoterDesigner is a Python command-line framework for motif-aware analysis, tissue-associated scoring and candidate design of tomato promoters.

It provides a unified workflow for:

- validating promoter FASTA inputs
- annotating a configured promoter motif set
- reporting root, stem, leaf and fruit-associated heuristic scores
- generating motif-aware candidate promoter sequences
- exporting reports and figure-ready result summaries
- running bundled model-backed routes explicitly when needed
- reproducing retained manuscript-facing result resources

TomatoPromoterDesigner integrates package-native deterministic modules, bundled model-backed routes, preprocessing logic, design utilities and retained project result tables in one inspectable software framework for the accompanying Application Note.

## Installation

Install a downloaded release wheel:

```bash
python -m venv .venv
source .venv/bin/activate
pip install tomato_promoter_designer-0.1.0-py3-none-any.whl
```

The release wheel contains the MpraVAE and deepseed checkpoints, their required
model definitions, the default training configuration and the example input.

For an editable installation from the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

For development:

```bash
pip install -e ".[dev]"
make test
```

## Quick Start

Run the bundled example workflow:

```bash
mkdir -p outputs

tomato-promoter-designer copy-example \
  --output outputs/demo_input.fasta

tomato-promoter-designer validate-input \
  --input outputs/demo_input.fasta

tomato-promoter-designer annotate \
  --input outputs/demo_input.fasta \
  --output outputs/demo_annotate.csv

tomato-promoter-designer predict \
  --input outputs/demo_input.fasta \
  --output outputs/demo_predict.csv

tomato-promoter-designer design \
  --input outputs/demo_input.fasta \
  --target fruit \
  --candidates 3 \
  --seed 42 \
  --output outputs/demo_design.csv

tomato-promoter-designer report \
  --input outputs/demo_design.csv \
  --output outputs/demo_report.json
```

Or run the same demo with:

```bash
make demo
```

## Inputs

The main input is a FASTA file containing one or more promoter sequences. Multi-sequence FASTA files are supported.

Single-sequence example:

```fasta
>promoter_1
ATGCAAAATTTATCG...
```

Multi-sequence example:

```fasta
>promoter_1
ATGCAAAATTTATCG...
>promoter_2
TTTATCAAAAGGCTA...
>promoter_3
CTATTGGGCAAAATA...
```

Validation rules:

- sequence identifiers must be unique
- empty records are rejected
- sequences are normalized to uppercase
- supported symbols are `A`, `C`, `G`, `T`, `N` and `M`

The package-native workflow can process validated promoter sequences of different lengths. MpraVAE-derived adapter routes require 165-bp unambiguous `A/C/G/T` sequences because that is the retained model input shape.

## Choosing A Target Tissue

The `design` command uses `--target` to define the desired tissue-associated design objective:

```bash
--target root
--target stem
--target leaf
--target fruit
```

For example, fruit-targeted design:

```bash
tomato-promoter-designer design \
  --input my_promoters.fasta \
  --target fruit \
  --candidates 5 \
  --seed 42 \
  --output outputs/fruit_design.csv
```

If the input FASTA contains 100 promoters and `--candidates 5` is used, the design table can contain up to 500 candidate rows. Candidates are ranked separately for each input promoter.

## Outputs And How To Use Them

`annotate` writes a motif table:

| Field | Meaning |
| --- | --- |
| `sequence_id` | Input promoter identifier |
| `motif` | Detected motif sequence |
| `start`, `end` | Zero-based motif coordinates |
| `score` | Match score, equal to motif length for exact matching |

`predict` writes a four-tissue scoring table:

| Field | Meaning |
| --- | --- |
| `sequence_id` | Input promoter identifier |
| `sequence` | Normalized promoter sequence |
| `score_root`, `score_stem`, `score_leaf`, `score_fruit` | Tissue-associated heuristic scores |
| `preferred_tissue` | Tissue with the highest score |

The model-backed prediction commands have route-specific outputs:

| Command | Output definition |
| --- | --- |
| `predict-mpravae` | Four tissue model scores using the same `score_root`--`score_fruit` field names; values are not calibrated to the package-native heuristic scale |
| `predict-deepseed` | `backend`, `predicted_log2_expression` and `predicted_linear_expression`; this route is scalar rather than tissue-specific |

`design` writes a candidate table:

| Field | Meaning |
| --- | --- |
| `original_sequence` | Input promoter sequence |
| `designed_sequence` | Designed candidate promoter sequence |
| `target_tissue` | Requested target tissue |
| `candidate_rank` | Rank within candidates for the same input promoter |
| `score_root`, `score_stem`, `score_leaf`, `score_fruit` | Candidate tissue-associated heuristic scores |
| `preserved_motifs` | Motifs protected by the package-native design route |
| `num_mutations` | Number of point differences from the input sequence |
| `passes_qc` | Quality-control flag when available |

Typical use of the design output:

1. Select candidates with high target-tissue score.
2. Prefer candidates with a clear target-tissue margin over non-target tissues.
3. Check that important motifs are preserved.
4. Avoid candidates with unnecessarily high mutation burden.
5. Use the selected `designed_sequence` entries for downstream manual review or experimental validation.

The software prioritizes promoter candidates computationally. Final promoter activity should be validated experimentally.

## Reproduce Manuscript Resources

The small demo verifies installation and command behavior. Manuscript and supplementary figures are based on retained result tables.

Regenerate the retained manuscript-facing result pack:

```bash
make reproduce-results
```

Outputs are written to:

```text
data/results/reproducible_legacy/
```

## Train A Compatible MpraVAE Checkpoint

The repository includes the MpraVAE model architecture, training dataset loader and a lightweight training entry point. This is provided so the model-backed route is not just a standalone `.pth` file.

Run a fast smoke test:

```bash
make train-mpravae-smoke
```

Run the default training configuration:

```bash
PYTHONPATH=src python scripts/train_mpravae.py \
  --config configs/training_mpravae.yaml
```

The generated checkpoint can be passed back into the model-backed commands:

```bash
tomato-promoter-designer predict-mpravae \
  --input examples/demo_input.fasta \
  --checkpoint models/mpravae/trained_mpravae_model.pth \
  --output outputs/mpravae_predict.csv
```

Detailed training documentation is available in `docs/training.md`.

## Rebuild Supplementary Figures With R

The repository includes five R scripts that redraw the supplementary figures from retained source tables. Use them when revising figure style, regenerating PDF versions, or confirming that the submitted panels are traceable to repository data.

Required R packages:

```r
install.packages(c("ggplot2", "readr", "dplyr", "pheatmap", "patchwork"))
```

Run all supplementary figure scripts:

```bash
make reproduce-results
make supplement-figures-r
```

The scripts write PNG and PDF files to `docs/fig/` by default:

| Script | Default input | Default output |
| --- | --- | --- |
| `scripts/render_FigS1_quantitative_reference.R` | `data/raw/mpravae/generated_prediction_results.csv` | `docs/fig/FigS1_quantitative_reference.png` |
| `scripts/render_FigS2_expression_heatmap.R` | `data/results/reproducible_legacy/tables/expression_heatmap_source.csv` | `docs/fig/FigS2_expression_heatmap.png` |
| `scripts/render_FigS3_dnabert_motif_summary.R` | `data/results/reproducible_legacy/tables/dnabert_motif_top20.csv` | `docs/fig/FigS3_dnabert_motif_summary.png` |
| `scripts/render_FigS4_kmer_distribution.R` | `data/results/reproducible_legacy/tables/kmer_frequency_comparison.csv` | `docs/fig/FigS4_kmer_distribution.png` |
| `scripts/render_FigS5_design_candidate_summary.R` | `data/results/reproducible_legacy/tables/design_candidate_summary.csv` | `docs/fig/FigS5_design_candidate_summary.png` |

Each script also accepts an optional input table and output directory:

```bash
Rscript scripts/render_FigS2_expression_heatmap.R \
  data/results/reproducible_legacy/tables/expression_heatmap_source.csv \
  docs/fig
```

## Main Commands

| Command | Purpose |
| --- | --- |
| `copy-example` | Copy the bundled demonstration FASTA to a user-selected path |
| `validate-input` | Validate FASTA records and sequence symbols |
| `annotate` | Scan promoter sequences for configured motif hits |
| `predict` | Generate root, stem, leaf and fruit-associated scores |
| `design` | Generate motif-aware candidate promoters |
| `report` | Build a compact JSON design summary |
| `figures` | Export lightweight figures from result CSV files |
| `model-figures` | Reconstruct retained project model figure bundles |
| `annotate-dnabert` | Run project DNABERT-derived motif post-processing |
| `predict-mpravae` | Run the bundled MpraVAE four-tissue checkpoint adapter |
| `design-mpravae` | Run the bundled MpraVAE latent design checkpoint adapter |
| `predict-deepseed` | Run the bundled deepseed scalar-scoring checkpoint adapter |

`annotate-dnabert` does not run DNABERT inference from FASTA input. It converts
precomputed DNABERT sequence and attention arrays into motif summaries. A
fine-tuned DNABERT checkpoint is required only to regenerate those upstream
attention arrays and is not included in the release wheel.

## Repository Layout

```text
TomatoPromoterDesigner/
├── src/tomato_promoter_designer/   # package source and CLI
├── examples/                       # runnable FASTA examples
├── data/                           # curated data and retained result resources
├── docs/                           # tool documentation and manuscript sources
├── models/                         # bundled lightweight checkpoints and model manifest
├── scripts/                        # data and result reproduction scripts
├── tests/                          # unit and regression tests
└── outputs/                        # local scratch outputs
```

## Documentation

Detailed tool documentation:

```text
docs/tool_documentation.md
docs/training.md
```

Manuscript sources:

```text
docs/application_note_submission.tex
docs/application_note_supplement.tex
docs/application_note_references.bib
```

## Data And Model Boundary

Package-native commands run after installation without loading a checkpoint.
The repository and release wheel also bundle the lightweight MpraVAE and
deepseed checkpoints required by their explicit model-backed routes:

```text
models/mpravae/best_val_corr_model.pth
models/deepseed/165_mpra_expr_denselstm.pth
models/deepseed/SeqRegressionModel.py
models/weights_manifest.json
```

The MpraVAE route includes compatible training code in this repository. The
deepseed route includes its inference model definition and checkpoint, but not a
separate training command. DNABERT support is a post-processing route for
precomputed attention inputs. These three routes therefore have different
reproduction boundaries.

Large genomes, HDF5 corpora, BLAST databases and optional external resources are tracked through manifests rather than bundled into normal git history.

See `docs/tool_documentation.md` for data, model and reproduction details.

## Citation

Citation metadata is provided in `CITATION.cff`. Please cite the Application Note and repository release when using TomatoPromoterDesigner.

## License

The package code is released under the MIT license declared in `LICENSE` and
`pyproject.toml`. Project data, checkpoints, derived resources and third-party
attribution boundaries are documented in `RESOURCE_LICENSES.md` and
`data/source_registry.tsv`.
