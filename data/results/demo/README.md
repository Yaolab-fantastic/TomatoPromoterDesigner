# Demo Output Guide

This directory contains the repository-bundled demonstration outputs generated from `examples/demo_input.fasta`.

These files are intended to show the expected shape of package results without requiring users or reviewers to rerun the full workflow first.

## Files

- `demo_annotate.csv`
  - motif annotations for each input promoter sequence
- `demo_predict.csv`
  - package-native tissue-associated heuristic scores for each input promoter sequence
- `demo_design.csv`
  - ranked package-native candidate designs for fruit-targeted promoter scoring
- `demo_report.json`
  - compact supplementary-style summary of the design output

## `demo_annotate.csv`

- `sequence_id`
  - input promoter identifier from the FASTA file
- `motif`
  - detected motif name
- `start`
  - zero-based motif start position in the input sequence
- `end`
  - zero-based motif end position
- `score`
  - motif match score reported by the annotation routine

## `demo_predict.csv`

- `sequence_id`
  - input promoter identifier
- `sequence`
  - promoter sequence used for prediction
- `expr_root`, `expr_stem`, `expr_leaf`, `expr_fruit`
  - deterministic tissue-associated heuristic scores for the four output tissues
- `preferred_tissue`
  - tissue with the highest reported score for that sequence

## `demo_design.csv`

- `sequence_id`
  - input promoter identifier
- `target_tissue`
  - tissue selected for design optimization
- `candidate_rank`
  - rank of the candidate within the output set for the same input promoter
- `original_sequence`
  - starting promoter sequence
- `designed_sequence`
  - designed candidate sequence produced by the workflow
- `expr_root`, `expr_stem`, `expr_leaf`, `expr_fruit`
  - deterministic tissue-associated heuristic scores for the designed candidate
- `preserved_motifs`
  - motif summary preserved or tracked during design
- `design_status`
  - machine-readable description of how the final candidate was produced
  - `baseline_motif_preserving`: produced by the package-native baseline design route
  - MpraVAE-derived statuses appear only in outputs from the explicit `design-legacy-mpravae` command
- `num_mutations`
  - number of base differences between `original_sequence` and `designed_sequence`
- `passes_qc`
  - route-specific quality-control flag when available; blank values indicate no QC flag was emitted by the package-native route

## `demo_report.json`

- `num_rows`
  - total number of rows in `demo_design.csv`
- `num_input_sequences`
  - number of unique input promoters
- `num_unique_designed_sequences`
  - number of unique candidate sequences in the design table
- `target_tissues`
  - tissues requested during design generation
- `canonical_length`
  - common input length in the bundled demo; MpraVAE-derived routes specifically require 165-bp unambiguous sequences
- `average_edit_distance`
  - mean edit distance between original and designed sequences
- `average_num_mutations`
  - mean number of point mutations across candidates
- `min_num_mutations`, `max_num_mutations`
  - mutation count range across candidates
- `num_qc_passed`
  - number of candidates passing QC when route-specific QC flags are available
- `qc_pass_rate`
  - fraction of candidates passing QC when route-specific QC flags are available
- `design_status_counts`
  - raw counts by machine-readable design status
- `design_status_display_counts`
  - counts by reader-friendly status label
- `best_candidate_by_sequence`
  - one compact summary entry per input promoter
  - the selected candidate is the one with the strongest target-tissue margin over competing tissues
