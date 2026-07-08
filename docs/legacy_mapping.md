# Legacy Mapping and Migration Notes

## Current situation

The original research code is distributed across multiple folders in the broader workspace:

- `MpraVAE/`
- `DNABERT/`
- `deepseed/`

Those directories contain useful method components, but they are not yet organized as a single installable, documented, release-oriented tool.

## Migration target inside this repository

| Legacy area | Planned repository destination | Integration status |
| --- | --- | --- |
| promoter sequence preprocessing | `src/tomato_promoter_designer/preprocessing/` | module ready |
| motif discovery and annotation | `src/tomato_promoter_designer/models/motif_annotator.py` | baseline implementation active |
| expression prediction | `src/tomato_promoter_designer/models/expression_predictor.py` | baseline implementation active |
| sequence generation and editing | `src/tomato_promoter_designer/models/generator.py` | baseline implementation active |
| report and result export | `src/tomato_promoter_designer/pipeline/report.py` | active |
| future trained checkpoints | `models/` | manifest ready |

## Migration rules

- move logic by function, not by copying whole legacy folders
- keep command-line inputs and outputs stable while replacing model internals
- preserve enough provenance in docstrings or comments so the paper can trace each migrated module
- add a test whenever a released model replaces a baseline implementation

## Immediate next integration tasks

1. wrap the final promoter-expression predictor behind the `run_prediction` interface
2. expose DNABERT-derived motif scoring through `run_annotation`
3. replace the current baseline design logic with the selected generative backend
4. register frozen checkpoints and hashes in `models/weights_manifest.json`

See also `docs/migration_inventory.md` for the current adapter readiness assessment.
