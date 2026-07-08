# Data Inventory

## Goal

The repository now distinguishes between:

- small raw inputs that are safe to bundle in git
- processed intermediate tables needed for reproducibility
- final repository-native results and figure bundles
- large upstream artifacts that should be tracked by manifest instead of copied directly

## Bundled raw data

- `data/raw/mpravae/`
  - training loss history
  - designed promoter table
  - generated prediction verification table
  - mutation-pair and random-promoter tables
  - tomato promoter training set
  - legacy BLAST and diversity PNG assets
- `data/raw/deepseed/`
  - DenseLSTM training log
  - original scatter PNG
- `data/raw/dnabert/`
  - `dev.tsv`
  - `atten.npy`
  - TFBS logo assets

## Bundled processed data

- `data/processed/dnabert_legacy/`
  - motif summary
  - processed sequence annotations
  - run metadata

## Bundled results

- `data/results/demo/`
  - deterministic repository demo outputs
  - includes `README.md` with field-level output descriptions
- `data/results/figures_*`
  - modern SVG figure exports
- `data/results/legacy_figures_bundle/`
  - reconstructed legacy paper-style figure bundle

## Large files intentionally left outside git

See `data/external/large_files.tsv`.

These include the largest genome FASTA files, HDF5 corpora, BLAST database shards, and heavyweight model archives or checkpoints. They are better managed through release assets, Zenodo, or an optional download layer rather than standard git history.
