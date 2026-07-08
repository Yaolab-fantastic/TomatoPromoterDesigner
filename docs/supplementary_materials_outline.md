# Supplementary Materials Outline

This document is a working outline for the supplementary package that can accompany a `Bioinformatics` `Application Note` submission for `TomatoPromoterDesigner`.

It is designed to map the current repository contents onto a concise manuscript plus a structured supplementary bundle.

## Suggested package structure

### Supplementary Methods

- software architecture overview
  - source: `README.md`
  - source: `docs/methods.md`
- migration lineage for legacy-derived components
  - source: `docs/legacy_mapping.md`
  - source: `docs/migration_inventory.md`
- reproducibility and release assumptions
  - source: `docs/reproducibility.md`

### Supplementary Tables

- Table S1. Repository components and roles
  - summarize `src/`, `data/`, `docs/`, `models/`, `scripts/`, and `tests/`
  - source: `README.md`
- Table S2. Bundled data inventory
  - source: `docs/data_inventory.md`
  - source: `data/inventory.tsv`
- Table S3. Source provenance and redistribution notes
  - source: `data/source_registry.tsv`
  - source: `docs/data_provenance.md`
- Table S4. External large-file manifest
  - source: `data/external/large_files.tsv`
- Table S5. Demo output field definitions
  - source: `data/results/demo/README.md`

### Supplementary Figures

- Figure S1. Predicted tissue activity heatmap
  - file: `data/results/figures_predict/prediction_heatmap.svg`
  - purpose: tissue-wise score overview for package-native prediction output
- Figure S2. Designed candidate comparison
  - file: `data/results/figures_design/design_summary.svg`
  - purpose: candidate ranking, target-tissue margin, and mutation burden summary
- Figure S3. DNABERT motif enrichment summary
  - file: `data/results/figures_motif/motif_enrichment.svg`
  - purpose: motif-ranking view from attention-based post-processing
- Figure S4. MpraVAE training loss dashboard
  - file: `data/results/legacy_figures_bundle/mpravae_loss_dashboard.svg`
  - purpose: recovered training-loss summary from archived model development
- Figure S5. MpraVAE prediction scatter
  - file: `data/results/legacy_figures_bundle/mpravae_prediction_scatter.svg`
  - purpose: recovered predicted-versus-measured validation view
- Figure S6. MpraVAE k-mer distribution comparison
  - file: `data/results/legacy_figures_bundle/mpravae_kmer_scatter.svg`
  - purpose: natural versus generated sequence composition consistency
- Figure S7. MpraVAE semantic sequence space
  - file: `data/results/legacy_figures_bundle/mpravae_semantic_space.svg`
  - purpose: deterministic sequence-space reconstruction for natural and generated promoters
- Figure S8. DeepSeed predictor training summary
  - file: `data/results/legacy_figures_bundle/deepseed_training_curve.svg`
  - purpose: archived optimization summary for the scalar predictor
- Figure S9. Edit-distance diversity comparison
  - file: `data/results/legacy_figures_bundle/mpravae_edit_distance_diversity.svg`
  - purpose: natural, random, and generated promoter diversity comparison

### Supplementary Data Files

- Data S1. Example input FASTA
  - file: `examples/demo_input.fasta`
- Data S2. Demonstration annotation output
  - file: `data/results/demo/demo_annotate.csv`
- Data S3. Demonstration prediction output
  - file: `data/results/demo/demo_predict.csv`
- Data S4. Demonstration design output
  - file: `data/results/demo/demo_design.csv`
- Data S5. Demonstration design summary report
  - file: `data/results/demo/demo_report.json`

## Suggested mapping to the main manuscript

### Main text should contain

- one concise software-focused figure
  - recommended default: `prediction_heatmap.svg` or `design_summary.svg`
- one short software availability paragraph
- one short implementation paragraph
- one compact validation paragraph

### Supplement should absorb

- field-level output definitions
- file-by-file provenance notes
- expanded figure recovery details
- migration lineage details for legacy-derived modules
- release and reproducibility details that are too operational for the main note

## Recommended figure strategy

### If the main text keeps one figure

- use `design_summary.svg` in the main paper
  - strongest direct connection to the design use case
- move `prediction_heatmap.svg` and `motif_enrichment.svg` to Supplementary Figures
- keep recovered `MpraVAE` and `DeepSeed` panels in the supplement unless one is essential for the manuscript narrative

### If the main text keeps one table instead

- use the main text table for software functions, inputs, outputs, and availability
- move all graphical validation views to the supplement

## Suggested supplementary captions

- keep captions short and software-oriented
- mention when a figure is package-native versus reconstructed from archived research outputs
- avoid overclaiming biological validation if the panel is mainly a migration or reproducibility view

## Release-aligned supplementary checklist

- confirm every supplementary figure exists in `data/results/`
- confirm every supplementary table source is either bundled or archived with a DOI
- confirm every mixed-provenance item has a redistribution decision recorded
- make sure supplementary file names match the manuscript references exactly
- freeze the supplementary package against the same software version tag as the paper

## Best current repository entry points

- software overview: `README.md`
- methods summary: `docs/methods.md`
- data inventory: `docs/data_inventory.md`
- provenance notes: `docs/data_provenance.md`
- figure inventory: `docs/figure_inventory.md`
- demo output guide: `data/results/demo/README.md`
