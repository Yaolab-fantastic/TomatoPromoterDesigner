# Reproducibility

## Current baseline

The current release is deterministic by design.

- default random seed: `20260708`
- baseline fallback predictors are deterministic
- the design backend is deterministic when `--seed` is provided

In this repository, `baseline` means package-native deterministic implementations and `legacy-derived` means routes adapted from earlier research codebases.

## What must be frozen before submission

- final train/validation/test split
- explicit independent test set used for the manuscript
- exact weight files used for released predictions
- package version tag
- dependency versions
- benchmark result tables
- example input and expected output pair

## Recommended release checklist

1. tag repository version
2. archive source in Zenodo
3. archive model weights
4. update `models/weights_manifest.json`
5. rerun demo commands
6. verify output hashes

## Bundled repository data

The repository now ships with a curated `data/` layout for small raw inputs, processed tables, and paper-facing figure bundles.

- refresh it with `PYTHONPATH=src python scripts/sync_repository_data.py`
- inspect provenance in `data/inventory.tsv`
- inspect intentionally excluded large artifacts in `data/external/large_files.tsv`

This keeps the software package reproducible while avoiding multi-hundred-megabyte genome files, HDF5 corpora, or heavyweight checkpoints in normal git history.
