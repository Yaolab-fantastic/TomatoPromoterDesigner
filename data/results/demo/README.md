# Demo Output Guide

This directory contains the repository-bundled demonstration outputs generated from `examples/demo_input.fasta`.

These files are intended to show the expected shape of package results without requiring users or reviewers to rerun the full workflow first.

## Files

- `demo_annotate.csv`
  - motif annotations for each input promoter sequence
- `demo_predict.csv`
  - tissue-wise prediction scores for each input promoter sequence
- `demo_design.csv`
  - ranked candidate designs for fruit-biased promoter optimization
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
  - predicted activity scores for the four tomato tissues
- `preferred_tissue`
  - tissue with the highest predicted score for that sequence

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
  - predicted scores for the designed candidate
- `preserved_motifs`
  - motif summary preserved or tracked during design
  - `not_tracked` indicates that motif preservation was not explicitly tracked for that route
- `design_status`
  - machine-readable description of how the final candidate was produced
  - `mpravae_decoded`: accepted directly from the MpraVAE-derived design route
  - `mpravae_repaired_by_reversion`: accepted after low-confidence edits were reverted for QC
  - `mpravae_qc_fallback`: original sequence retained after candidate QC fallback
  - `baseline_motif_preserving`: produced by the package-native baseline design route
- `num_mutations`
  - number of base differences between `original_sequence` and `designed_sequence`
- `passes_qc`
  - whether the final design passed the built-in promoter QC rule set

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
  - expected promoter length for the tomato workflow
- `average_edit_distance`
  - mean edit distance between original and designed sequences
- `average_num_mutations`
  - mean number of point mutations across candidates
- `min_num_mutations`, `max_num_mutations`
  - mutation count range across candidates
- `num_qc_passed`
  - number of candidates passing QC
- `qc_pass_rate`
  - fraction of candidates passing QC
- `design_status_counts`
  - raw counts by machine-readable design status
- `design_status_display_counts`
  - counts by reader-friendly status label
- `best_candidate_by_sequence`
  - one compact summary entry per input promoter
  - the selected candidate is the one with the strongest target-tissue margin over competing tissues
