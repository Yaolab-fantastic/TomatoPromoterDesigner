# Resource Licensing And Attribution

The repository source code, package documentation, package-native outputs and
project-authored model code are released under the repository MIT license.

The bundled MpraVAE and deepseed checkpoints, tomato promoter project tables,
processed result tables and manuscript-reproduction resources were generated
within the TomatoPromoterDesigner project. They are distributed with this
repository for reproducible research use under the repository release terms.
File-level origins and roles are recorded in `data/source_registry.tsv`, and
checkpoint checksums are recorded in `models/weights_manifest.json`.

DNABERT-derived processing uses methods and resources based on DNABERT. Users
must retain the relevant DNABERT citation and attribution when redistributing
DNABERT-derived motif resources. A fine-tuned DNABERT checkpoint is not bundled
with TomatoPromoterDesigner; the `annotate-dnabert` command consumes precomputed
sequence and attention inputs.

Large optional genomes, corpora and BLAST databases are not distributed in the
default repository or Python wheel. Their availability and intended use are
listed in `data/external/external_resources.tsv`; their original licenses and
database terms continue to apply.
