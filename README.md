# TomatoPromoterDesigner

`TomatoPromoterDesigner` is a unified Python toolkit for motif-aware design and evaluation of tissue-biased tomato promoters.

The repository is designed to consolidate three currently separate research threads:

- transformer-based promoter generation from `MpraVAE`
- motif annotation inspired by `DNABERT`
- conditional sequence design and scoring logic adapted from `deepseed`

The repository now also carries a curated `data/` layer so the small raw inputs, processed tables, and paper-facing figure bundles needed for reproduction can live alongside the codebase.

This repository now combines a stable package structure with staged migration of earlier research models, so the command-line workflows can use real adapted components where the workspace provides compatible checkpoints.

## What is already here

- installable Python package layout
- a single CLI entry point
- FASTA and CSV I/O helpers
- schema validation for promoter sequences
- a deterministic motif annotation module
- a deterministic baseline expression predictor with legacy-derived prediction adapters
- a design pipeline that preserves annotated motifs and mutates flanking sequence
- report generation in JSON and CSV
- publication-style SVG figure export from prediction, design, and motif-summary tables
- repository documentation, examples, and tests
- legacy-derived adapters for `deepseed`, `DNABERT` post-processing, and tomato `MpraVAE`
- a repaired `MpraVAE` design route that emits novel sequences, uses deterministic posterior-mean scoring, and applies tomato-data-informed QC

## Current release boundaries

The current repository does **not** yet redistribute every final trained `TransVAE`, `DNABERT`, or `preGAN` weight file. The public package therefore keeps some replaceable baseline components while exposing legacy-derived routes where validated checkpoints are available.

That gives us three practical benefits:

1. a package that can already be installed and exercised
2. stable CLI and file formats for downstream paper writing
3. a controlled path to swap in final public models without breaking the software interface

## Repository layout

```text
TomatoPromoterDesigner/
├── pyproject.toml
├── README.md
├── LICENSE
├── data/
├── src/tomato_promoter_designer/
├── docs/
├── examples/
├── models/
├── outputs/
├── scripts/
├── tests/
└── app/optional_web_demo/
```

Directory roles:

- `src/`
  - installable package code and CLI implementation
- `data/`
  - bundled small raw inputs, processed tables, canonical demo results, and paper-facing figure assets intended to ship with the repository
- `outputs/`
  - local runtime workspace for user-generated command outputs during testing or exploration
  - intentionally ignored from normal git history
- `docs/`
  - manuscript-supporting software, data, and reproducibility documentation
- `models/`
  - model weight manifest and packaging-facing model metadata
- `scripts/`
  - repository maintenance utilities such as data synchronization
- `tests/`
  - unit and regression tests

## Installation

Create a virtual environment and install in editable mode:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Quick start

Use the example FASTA in `examples/demo_input.fasta`.

Annotate motifs:

```bash
tomato-promoter-designer annotate \
  --input examples/demo_input.fasta \
  --output outputs/annotate.csv
```

Predict tissue-biased expression scores:

```bash
tomato-promoter-designer predict \
  --input examples/demo_input.fasta \
  --output outputs/predict.csv
```

Design fruit-biased candidates while preserving motif regions:

```bash
tomato-promoter-designer design \
  --input examples/demo_input.fasta \
  --target fruit \
  --candidates 5 \
  --output outputs/design.csv
```

Build a compact report:

```bash
tomato-promoter-designer report \
  --input outputs/design.csv \
  --output outputs/report.json
```

The report JSON includes mutation and QC summaries together with a per-sequence best-candidate overview that is convenient for supplementary materials.

Export manuscript-ready SVG figures:

```bash
tomato-promoter-designer figures \
  --input outputs/design.csv \
  --output-dir outputs/design_figures
```

Export legacy result figures reconstructed from the original deepseed and MpraVAE outputs:

```bash
tomato-promoter-designer legacy-figures \
  --output-dir outputs/legacy_figures
```

Refresh the repository-bundled data layout:

```bash
make sync-data
```

## Current command set

- `annotate`: scan promoter sequences for configured motif hits
- `annotate-legacy-dnabert`: run the migrated DNABERT attention-to-motif post-processing workflow
- `predict`: auto-prefer the real tomato `MpraVAE` predictor for canonical 165 bp A/C/G/T inputs, otherwise fall back to the baseline scorer
- `predict-legacy-mpravae`: run the migrated MpraVAE tomato four-tissue predictor
- `predict-legacy-deepseed`: call the migrated `deepseed` DenseLSTM scalar predictor
  - `predict-legacy` remains accepted as a backward-compatible alias
- `design`: auto-prefer the real `MpraVAE` latent-space designer for canonical tomato inputs, otherwise fall back to the baseline motif-preserving designer
- `design-legacy-mpravae`: run the migrated MpraVAE latent-space design workflow
- `report`: summarize a design result table
- `figures`: export lightweight SVG figures from result CSV tables
- `legacy-figures`: batch-export legacy paper-style figures from migrated deepseed and MpraVAE result files
  - includes reconstructed loss curves, prediction scatter, diversity comparison, and semantic sequence space
- `validate-input`: validate a FASTA file against repository sequence rules

## Terminology

- `baseline`
  - deterministic package-native logic shipped directly inside this repository and used as the default fallback when no compatible migrated checkpoint route is available
- `legacy-derived`
  - functionality adapted from earlier `MpraVAE`, `DNABERT`, or `deepseed` research code and exposed through the unified package
- `legacy figures`
  - manuscript-facing reconstructions or bundled assets derived from earlier result tables, logs, or figure resources
- `adapter`
  - a wrapper that keeps upstream model behavior accessible through the repository's stable package interfaces

## Data contract

Input FASTA sequences are expected to be:

- uppercase or lowercase DNA-like strings
- composed of `A`, `C`, `G`, `T`, optionally `N` and `M`
- ideally length `165` for the current tomato workflow

The software accepts other lengths for development and inspection, but emits warnings through the report layer when sequences diverge from the canonical training length.

## Data layout

- `data/raw/`
  - curated small raw tables and figure assets copied from the legacy workspaces
- `data/processed/`
  - intermediate outputs from migrated workflows such as DNABERT motif post-processing
- `data/results/`
  - demo outputs, modern figure exports, and the reconstructed legacy figure bundle
- `data/external/`
  - manifest of large upstream artifacts intentionally kept outside standard git history

The canonical repository-bundled artifacts live under `data/`. By contrast, `outputs/` is a disposable local working directory for ad hoc CLI runs such as quick tests, notebooks, or temporary figure export checks.

The detailed bundled-data description lives in `docs/data_inventory.md`, and the machine-readable provenance table is `data/inventory.tsv`.

For field-by-field guidance to the bundled demonstration outputs, see `data/results/demo/README.md`.

## Model status and extension points

The package is organized so model upgrades stay local and controlled:

- `models/expression_predictor.py`
  - replace `HeuristicExpressionPredictor` with trained predictor weights
- `legacy/mpravae_tomato.py`
  - now wraps the earlier tomato multi-tissue VAE + predictor checkpoint and latent-space design loop
- `legacy/deepseed_expression.py`
  - already wraps the original `deepseed` scalar-expression checkpoint for staged migration
- `models/motif_annotator.py`
  - replace or augment motif scanning with DNABERT attention-based annotations
- `legacy/dnabert_motif.py`
  - now contains a dependency-light migration of the DNABERT motif post-processing path
- `models/generator.py`
  - replace `MotifPreservingDesigner` with the final design backend
- `pipeline/design.py`
  - expose whichever integrated route is selected for the paper

## Legacy research mapping

| Legacy source | Future home |
| --- | --- |
| `MpraVAE/code/TransVAE.py` | `src/tomato_promoter_designer/models/transvae.py` |
| `MpraVAE/code/transformervae.py` | `src/tomato_promoter_designer/pipeline/design.py` |
| `DNABERT/motif/find_motifs.py` | `src/tomato_promoter_designer/models/motif_annotator.py` |
| `deepseed/Predictor/*` | `src/tomato_promoter_designer/models/expression_predictor.py` |
| `deepseed/Generatorme/preGAN_expr.py` | `src/tomato_promoter_designer/models/generator.py` |

## Testing

Run the unit tests from the repository root:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

Or use the bundled developer targets:

```bash
make install-dev
make test
make demo
```

To exercise the first real legacy-derived model adapter:

```bash
PYTHONPATH=src python -m tomato_promoter_designer.cli predict-legacy-deepseed \
  --input examples/demo_input.fasta \
  --output outputs/deepseed_legacy_predict.csv
```

To exercise the migrated MpraVAE tomato predictor:

```bash
PYTHONPATH=src python -m tomato_promoter_designer.cli predict-legacy-mpravae \
  --input examples/demo_input.fasta \
  --output outputs/mpravae_predict.csv
```

To exercise the migrated MpraVAE latent-space design route:

```bash
PYTHONPATH=src python -m tomato_promoter_designer.cli design-legacy-mpravae \
  --input examples/demo_input.fasta \
  --target fruit \
  --candidates 3 \
  --output outputs/mpravae_design.csv
```

The current `design-legacy-mpravae` workflow now:

- optimizes latent codes toward a target tissue
- samples or decodes candidate promoter sequences from the legacy VAE decoder
- re-scores designed sequences with deterministic posterior-mean prediction
- applies tomato-training-data-informed QC instead of an overly strict generic promoter rule
- minimally reverts low-confidence edits only when QC repair is needed

To exercise the migrated DNABERT motif post-processing route with the legacy example files:

```bash
PYTHONPATH=src python -m tomato_promoter_designer.cli annotate-legacy-dnabert \
  --dev-tsv ../DNABERT/examples/sample_data/vision/dev.tsv \
  --atten-npy ../DNABERT/examples/result/6/atten.npy \
  --output-dir outputs/dnabert_legacy
```

The migrated DNABERT adapter reports whether strict significance filtering retained any motifs. If not, it transparently falls back to a ranked candidate summary so the output remains inspectable without overstating statistical confidence.

## Repository standards

- package code lives under `src/tomato_promoter_designer/`
- frozen or release-ready model files will be tracked through `models/weights_manifest.json`
- paper-facing method and reproducibility notes live under `docs/`
- future demo UI stays isolated in `app/optional_web_demo/` so the package remains the primary artifact

## Citation and contribution

- software citation metadata: `CITATION.cff`
- contribution workflow: `CONTRIBUTING.md`
- legacy code migration map: `docs/legacy_mapping.md`
- release preparation checklist: `docs/release_checklist.md`

## Submission-oriented notes

This repository is intentionally arranged to support `Bioinformatics Application Note` submission requirements:

- stable software name
- single command-line entry point
- documented install path
- clear availability section targets
- explicit examples and test data
- a clean route to versioned release and DOI archiving

The current journal-facing requirement snapshot is summarized in `docs/bioinformatics_application_note.md` and should be rechecked against the official journal guidance at submission time.

The paper-facing roadmap lives in:

- `docs/methods.md`
- `docs/reproducibility.md`
- `models/README.md`
- `docs/figure_inventory.md`
- `docs/data_inventory.md`
- `docs/data_provenance.md`
- `docs/bioinformatics_application_note.md`
- `docs/application_note_text_blocks.md`
- `docs/supplementary_materials_outline.md`
