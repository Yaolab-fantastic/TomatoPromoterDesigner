# Release Checklist for Application Note Submission

## Must complete before submission

- freeze a public version tag that matches the manuscript
- replace all temporary repository and archive placeholders with the real public URL and DOI
- ensure the abstract includes the software availability location
- confirm the software package described in the paper is freely available to non-commercial users
- verify that the software name is consistent across the title, abstract, `README.md`, `CITATION.cff`, and package metadata
- define and document the final independent test set used for the paper
- save the exact result tables and figure inputs that support the manuscript claims
- review `data/source_registry.tsv` and approve the final public redistribution boundary
- archive large external artifacts outside normal git history and connect them back through `models/weights_manifest.json` and `data/external/large_files.tsv`
- prepare any required AI-use disclosure for the cover letter and manuscript package

## Software package checks

- `pip install -e .` works in a clean environment
- the CLI entry point runs without relying on local absolute paths
- `README.md` includes installation, quick-start commands, and data-layout guidance
- `LICENSE` and `CITATION.cff` are present and accurate
- example inputs and expected outputs match the release version

## Reproducibility checks

- unit tests pass
- at least one clean end-to-end demo run has been rerun after the final version tag
- `PYTHONPATH=src python scripts/sync_repository_data.py` completes successfully
- bundled figure exports regenerate without manual intervention
- the release package can recreate the manuscript-facing example outputs from documented commands

## Data and licensing checks

- confirm redistribution status for bundled `MpraVAE`-derived materials
- confirm redistribution status for bundled `deepseed`-derived materials
- preserve attribution and license notice for bundled `DNABERT`-derived materials
- keep mixed-provenance heavy artifacts in DOI-backed archives rather than in standard git history

## Manuscript package checks

- keep the `Application Note` within the current journal length limit
- use a software-first title that includes `TomatoPromoterDesigner`
- keep the implementation paragraph concise and concrete
- mention supplementary information in the abstract if supplementary files are provided
- make sure the paper refers to the unified tool, not to legacy folders as if they were the released software

## Final review references

- `docs/bioinformatics_application_note.md`
- `docs/application_note_text_blocks.md`
- `docs/reproducibility.md`
- `docs/data_provenance.md`
- `docs/data_inventory.md`
