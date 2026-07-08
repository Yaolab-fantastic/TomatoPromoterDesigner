# Bioinformatics Application Note Package

## Current assessment

`TomatoPromoterDesigner` now looks like a plausible `Bioinformatics` `Application Note` companion package because the work is presented as one installable software artifact rather than as several disconnected research folders. The repository has a stable package name, a single CLI entry point, runnable examples, bundled demonstration data, figure-generation utilities, and explicit provenance notes for migrated legacy components.

The remaining work is no longer mainly about code sprawl. It is about final release discipline: freezing exactly what is public, documenting what remains external, and aligning the manuscript text with the software package that will actually be released.

## Official requirement snapshot

Checked against Oxford Academic sources on `2026-07-08`.

- `Bioinformatics` states that an `Application Note` should be no more than `4 journal pages`, which corresponds to about `2,600 words`; a note with `1 figure or table` is expected to be closer to `2,000 words`.
- The journal states that the software or data described in the paper must be `freely available to non-commercial users` at submission time.
- The journal asks authors to provide a `stable URL` and recommends archiving the submitted version and test data in a persistent public service such as `Zenodo`, `Figshare`, `Software Heritage`, `Bioconductor`, or `CRAN`; the abstract should identify where the software is available.
- The abstract should mention any `supplementary information` when such material exists.
- For machine-learning methods, the journal expects `clear independent test-set evaluation`.
- Oxford University Press also states that any acceptable use of `AI or large language models` in code, images, or supplementary generation must be disclosed, including in the cover letter and the manuscript or acknowledgements where applicable.

## What this means for this repository

- The repository is already strong on packaging:
  - installable Python project
  - single CLI entry point
  - examples, tests, and reproducibility notes
  - curated `data/` layer with provenance tables
- The repository is not yet fully ready for submission in three places:
  - the public repository URL and DOI archive are not frozen
  - redistribution status for bundled `MpraVAE`- and `deepseed`-derived files still needs a final decision
  - the manuscript needs a concise, software-first validation story with an explicit independent test set

## Required pre-submission actions

1. Freeze the public software release.
   - Tag the exact repository version that matches the manuscript.
   - Make sure `README.md`, `CITATION.cff`, and the manuscript all use the same software name and version.

2. Publish stable availability endpoints.
   - Create the final public repository URL.
   - Archive the release in a DOI-bearing service.
   - Add the repository URL and DOI to the manuscript abstract, `CITATION.cff`, and package metadata.

3. Finalize the public redistribution boundary.
   - Recheck `data/source_registry.tsv` and `docs/data_provenance.md`.
   - Decide whether mixed-provenance legacy assets stay in the public repository, move to a separate archive, or are replaced by regenerated derivatives.

4. Freeze the manuscript-facing validation evidence.
   - Define the final train, validation, and independent test split.
   - Save the exact benchmark tables used in the paper.
   - Ensure the software package can reproduce the figures and tables that are claimed in the note.

5. Complete clean-environment verification.
   - Install from scratch in a fresh environment.
   - Run the documented demo commands.
   - Rebuild the bundled figures and confirm the expected outputs.

6. Prepare required disclosures.
   - Draft the software availability statement for the abstract.
   - Add any required AI-use disclosure to the manuscript package if AI-assisted coding, image generation, or supplementary generation is retained.

7. Freeze the supplementary package structure.
   - Decide which figure stays in the main note and which items move to supplementary material.
   - Align filenames and labels with `docs/supplementary_materials_outline.md`.

## Recommended manuscript framing

- Title:
  - include the software name directly
- Abstract:
  - open with the biological need for tissue-biased tomato promoter design
  - introduce `TomatoPromoterDesigner` as the software contribution
  - end with availability and reproducibility, not speculative biological claims
- Availability and Implementation:
  - emphasize Python implementation, CLI access, example data, processed demo outputs, and stable archive locations
- Methods:
  - present the unified workflow as `annotation -> prediction -> design -> reporting -> figure export`
  - describe migrated `MpraVAE`, `DNABERT`, and `deepseed` components as implementation lineage, not as separate tools competing for attention

## Practical verdict

Targeting `Bioinformatics` `Application Note` is reasonable for this project if the paper stays software-first and the release package is frozen before submission. The repository now supports that trajectory well; the biggest remaining risks are release availability, redistribution boundaries, and final validation packaging rather than overall repository structure.

## Official links

- `Bioinformatics` author guidelines: `https://academic.oup.com/BIOINFORMATICS/pages/author-guidelines`
- OUP AI policy hub: `https://academic.oup.com/journals/pages/artificial-intelligence-ai-tools`
