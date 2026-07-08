# Models

This directory is reserved for model manifests, metadata, and eventually published weights.

## Current status

The repository is wired for model integration, but the current package still ships with deterministic baseline implementations so the command-line interface and file contracts remain stable until final public weights are frozen.

## Planned assets

- `weights_manifest.json`
  - model names
  - version hashes
  - expected input length
  - source publication tag
  - download URL or DOI
- trained expression predictor weights
- trained promoter design backend weights
- motif annotation backend metadata

## Recommended release pattern

1. store source code in GitHub
2. tag a release
3. archive the release in Zenodo
4. publish weight artifacts with checksums
5. update `weights_manifest.json`
