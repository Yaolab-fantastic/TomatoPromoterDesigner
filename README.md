# TomatoPromoterDesigner

TomatoPromoterDesigner is a Python command-line framework for motif-aware analysis, tissue-associated prediction and candidate design of tomato promoters.

It provides a unified workflow for:

- validating promoter FASTA inputs
- annotating tomato promoter motifs
- reporting root, stem, leaf and fruit-associated heuristic scores
- generating motif-aware candidate promoter sequences
- exporting reports and figure-ready result summaries
- running bundled legacy-derived checkpoint adapters explicitly when needed
- reproducing retained manuscript-facing result resources

TomatoPromoterDesigner is a software framework, not a newly trained promoter deep learning model. The repository contains package-native deterministic modules, documented legacy-derived adapters and retained result tables used for the accompanying Application Note.

## Installation

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

tomato-promoter-designer validate-input \
  --input examples/demo_input.fasta

tomato-promoter-designer annotate \
  --input examples/demo_input.fasta \
  --output outputs/demo_annotate.csv

tomato-promoter-designer predict \
  --input examples/demo_input.fasta \
  --output outputs/demo_predict.csv

tomato-promoter-designer design \
  --input examples/demo_input.fasta \
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

`predict` writes a four-tissue prediction table:

| Field | Meaning |
| --- | --- |
| `sequence_id` | Input promoter identifier |
| `sequence` | Normalized promoter sequence |
| `expr_root`, `expr_stem`, `expr_leaf`, `expr_fruit` | Tissue-associated heuristic scores |
| `preferred_tissue` | Tissue with the highest score |

`design` writes a candidate table:

| Field | Meaning |
| --- | --- |
| `original_sequence` | Input promoter sequence |
| `designed_sequence` | Designed candidate promoter sequence |
| `target_tissue` | Requested target tissue |
| `candidate_rank` | Rank within candidates for the same input promoter |
| `expr_root`, `expr_stem`, `expr_leaf`, `expr_fruit` | Candidate tissue-associated heuristic scores |
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
make reproduce-legacy
```

Outputs are written to:

```text
data/results/reproducible_legacy/
```

## Main Commands

| Command | Purpose |
| --- | --- |
| `validate-input` | Validate FASTA records and sequence symbols |
| `annotate` | Scan promoter sequences for configured motif hits |
| `predict` | Generate root, stem, leaf and fruit-associated scores |
| `design` | Generate motif-aware candidate promoters |
| `report` | Build a compact JSON design summary |
| `figures` | Export lightweight figures from result CSV files |
| `legacy-figures` | Reconstruct retained legacy-derived figure bundles |
| `annotate-legacy-dnabert` | Run retained DNABERT-derived motif post-processing |
| `predict-legacy-mpravae` | Run the bundled MpraVAE-derived four-tissue checkpoint adapter |
| `design-legacy-mpravae` | Run the bundled MpraVAE-derived latent design checkpoint adapter |
| `predict-legacy-deepseed` | Run the bundled deepseed-derived scalar-expression checkpoint adapter |

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
```

Manuscript sources:

```text
docs/application_note_submission.tex
docs/application_note_supplement.tex
docs/application_note_references.bib
```

## Data And Model Boundary

Package-native commands run after installation and do not require model checkpoints. The current repository also bundles lightweight retained checkpoints for explicit legacy-derived routes:

```text
models/mpravae/best_val_corr_model.pth
models/deepseed/165_mpra_expr_denselstm.pth
models/deepseed/SeqRegressionModel.py
models/weights_manifest.json
```

Large genomes, HDF5 corpora, BLAST databases and optional external resources are tracked through manifests rather than bundled into normal git history.

See `docs/tool_documentation.md` for data, model and reproduction details.

## Citation

Citation metadata is provided in `CITATION.cff`. Please cite the Application Note and repository release when using TomatoPromoterDesigner.

## License

The package code is released under the license declared in `LICENSE` and `pyproject.toml`. Some retained data resources and legacy-derived assets have separate provenance or redistribution constraints documented in the repository data manifests.
