# Quickstart

These commands write into `outputs/`, which is the local working directory for ad hoc runs. The stable demonstration artifacts bundled with the repository are stored separately under `data/results/`.

## 1. Validate the example data

```bash
tomato-promoter-designer validate-input --input examples/demo_input.fasta
```

## 2. Annotate motif hits

```bash
tomato-promoter-designer annotate \
  --input examples/demo_input.fasta \
  --output outputs/annotate.csv
```

## 3. Predict tissue scores

```bash
tomato-promoter-designer predict \
  --input examples/demo_input.fasta \
  --output outputs/predict.csv
```

## 4. Design fruit-biased candidates

```bash
tomato-promoter-designer design \
  --input examples/demo_input.fasta \
  --target fruit \
  --candidates 3 \
  --output outputs/design.csv
```

## 5. Build a report

```bash
tomato-promoter-designer report \
  --input outputs/design.csv \
  --output outputs/report.json
```

The resulting JSON now includes overall mutation statistics, QC pass-rate summaries, and a best-candidate snapshot for each input promoter.

The repository-bundled reference outputs and their field descriptions are available under `data/results/demo/README.md`.
