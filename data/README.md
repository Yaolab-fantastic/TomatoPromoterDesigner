# Data Layout

This repository keeps publication-facing data in four layers so the software package remains inspectable without placing every large optional artifact in git.

## Directories

- `raw/`
  - project input tables and support assets for MpraVAE, deepseed and DNABERT-derived processing
  - enough to regenerate the retained manuscript figures and motif-processing outputs
- `processed/`
  - intermediate outputs produced by migrated workflows
  - currently centered on the `DNABERT` motif post-processing tables
- `results/`
  - repository-native outputs generated from the unified toolkit
  - includes demo command outputs, SVG figures and retained manuscript result bundles
- `external/`
  - manifests for large files intentionally left outside git
  - these remain candidates for Zenodo, release assets, or an optional download script
- `../models/`
  - bundled lightweight MpraVAE and deepseed checkpoints used by explicit model-backed commands

## Boundary with `outputs/`

The `data/` tree stores repository-curated artifacts that are meant to remain stable across reruns and support manuscript reproduction.

The root-level `outputs/` directory serves a different purpose:

- it is the default scratch space for local CLI runs
- it may contain temporary checks, exploratory exports, or user-specific runs
- it is not the canonical location for repository-bundled reference results

## Reproducing manuscript-facing data

Run:

```bash
make reproduce-results
```

This command regenerates the retained result pack used by the Application Note figures and supplementary materials under `data/results/reproducible_legacy/`.

For the broader data-sync utility used during repository maintenance, run:

```bash
PYTHONPATH=src python scripts/sync_repository_data.py
```

This script copies selected raw files into `data/raw`, refreshes processed tables, regenerates demo outputs, regenerates bundled figures, and updates `data/inventory.tsv`.

## Inventory files

- `inventory.tsv`
  - machine-readable list of bundled data files and their provenance
- `source_registry.tsv`
  - higher-level registry of project origins, license scope and redistribution notes
- `summary.json`
  - compact count summary by stage
- `external/external_resources.tsv`
  - optional large artifacts intentionally excluded from normal git history

## Documentation

- `docs/tool_documentation.md`
  - tool usage, manuscript reproduction, data resources, model boundaries and provenance notes
