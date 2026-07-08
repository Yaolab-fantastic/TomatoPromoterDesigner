# Data Layout

This repository keeps publication-facing data in four layers so the software package remains inspectable without forcing every large upstream artifact into git.

## Directories

- `raw/`
  - small raw tables and image assets copied from the legacy `MpraVAE`, `deepseed`, and `DNABERT` workspaces
  - enough to regenerate the bundled legacy figures and motif-processing outputs
- `processed/`
  - intermediate outputs produced by migrated workflows
  - currently centered on the `DNABERT` motif post-processing tables
- `results/`
  - repository-native outputs generated from the unified toolkit
  - includes demo command outputs, modern SVG figures, and the reconstructed legacy figure bundle
- `external/`
  - manifests for large files intentionally left outside git
  - these remain candidates for Zenodo, release assets, or an optional download script

## Boundary with `outputs/`

The `data/` tree stores repository-curated artifacts that are meant to remain stable across reruns and support manuscript reproduction.

The root-level `outputs/` directory serves a different purpose:

- it is the default scratch space for local CLI runs
- it may contain temporary checks, exploratory exports, or user-specific runs
- it is not the canonical location for repository-bundled reference results

## Refreshing the repository data

Run:

```bash
PYTHONPATH=src python scripts/sync_repository_data.py
```

This script copies the selected raw files into `data/raw`, refreshes processed tables, regenerates demo outputs, regenerates bundled figures, and updates `data/inventory.tsv`.

## Inventory files

- `inventory.tsv`
  - machine-readable list of bundled data files and their provenance
- `source_registry.tsv`
  - higher-level registry of upstream origins, license evidence, and redistribution notes
- `summary.json`
  - compact count summary by stage
- `external/large_files.tsv`
  - large upstream artifacts intentionally excluded from the git repository
