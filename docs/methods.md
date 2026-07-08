# Methods And Integration Plan

## Product view

The platform exposes one user-facing workflow:

1. accept promoter sequence input
2. annotate motif regions
3. estimate tissue-biased expression
4. generate candidate designs
5. export a compact result table and report

## Repository view

The current codebase separates:

- `io/`
  - file and schema handling
- `models/`
  - swappable modeling backends
- `pipeline/`
  - user-facing task orchestration
- `evaluation/`
  - compact result analysis helpers

## Planned migration from legacy research code

In the repository documents, `baseline` refers to deterministic package-native implementations shipped directly in this codebase, while `legacy-derived` refers to functionality adapted from earlier `MpraVAE`, `DNABERT`, or `deepseed` research code.

### Stage 1

- port trained predictor logic into `models/expression_predictor.py`
- replace baseline scoring with loaded weights

### Stage 2

- port DNABERT attention or motif export logic into `models/motif_annotator.py`
- replace static motif list with learned annotations

### Stage 3

- port the selected design backend into `models/generator.py`
- expose a single stable design path through `pipeline/design.py`

### Stage 4

- freeze release candidate inputs, outputs, and benchmark tables
