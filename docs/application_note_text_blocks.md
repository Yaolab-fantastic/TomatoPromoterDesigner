# Application Note Text Blocks

The following paragraphs are editable manuscript starters aligned with the current repository state. They still require the final public repository URL, DOI, version tag, benchmark numbers, and author list before submission.

## Availability and Implementation

`TomatoPromoterDesigner` is implemented in Python and distributed as an installable command-line toolkit for tomato promoter annotation, tissue-biased expression prediction, candidate sequence design, report generation, and manuscript-facing figure export. The software package includes documentation, example FASTA inputs, processed demonstration data, unit tests, and reproducibility-oriented figure reconstruction utilities that unify previously separate workflows derived from `MpraVAE`, `DNABERT`, and `deepseed`. Source code is available at `REPOSITORY_URL`, and the version used for this manuscript together with archived release materials is available at `DOI_URL`.

## Methods Summary

`TomatoPromoterDesigner` exposes a unified workflow covering `annotation -> prediction -> design -> report generation -> figure export`. The released package combines package-native baseline utilities with legacy-derived components where compatible checkpoints and support files are available. In addition to modern outputs for routine use, the repository can regenerate manuscript-facing summaries and a curated legacy figure bundle from tracked raw and processed inputs.

## Data Availability

The repository contains a curated data layer that separates bundled raw support tables, processed intermediate files, repository-native demonstration outputs, and manifests for large external artifacts. Small files required for software demonstration and figure reconstruction are included directly in the repository. Large genomes, HDF5 corpora, BLAST database shards, and heavyweight model artifacts are distributed separately through persistent archives referenced by the release metadata. File-level provenance is documented in `data/inventory.tsv` and `data/source_registry.tsv`.

## Reproducibility Statement

The public release is designed to make the software workflow reproducible without requiring access to the entire historical workspace. The repository includes deterministic demo commands, example inputs, processed motif outputs, modern SVG summaries, and a curated legacy figure bundle generated from tracked support files. The software version, external artifact manifest, benchmark tables, and archive identifiers should be frozen to match the submitted manuscript.

## Abstract Availability Sentence

Availability and implementation: `TomatoPromoterDesigner` is implemented in Python and is freely available to non-commercial users at `REPOSITORY_URL`; the version used for this study is archived at `DOI_URL`.
