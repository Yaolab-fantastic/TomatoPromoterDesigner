PYTHON ?= python

.PHONY: install install-dev test demo validate train-mpravae-smoke package model-figures legacy-figures reproduce-results reproduce-legacy supplement-figures-r sync-data clean

install:
	$(PYTHON) -m pip install -e .

install-dev:
	$(PYTHON) -m pip install -e ".[dev]"

test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests

demo:
	PYTHONPATH=src $(PYTHON) -m tomato_promoter_designer.cli annotate --input examples/demo_input.fasta --output outputs/demo_annotate.csv
	PYTHONPATH=src $(PYTHON) -m tomato_promoter_designer.cli predict --input examples/demo_input.fasta --output outputs/demo_predict.csv
	PYTHONPATH=src $(PYTHON) -m tomato_promoter_designer.cli design --input examples/demo_input.fasta --target fruit --candidates 3 --seed 42 --output outputs/demo_design.csv
	PYTHONPATH=src $(PYTHON) -m tomato_promoter_designer.cli report --input outputs/demo_design.csv --output outputs/demo_report.json

model-figures:
	PYTHONPATH=src $(PYTHON) -m tomato_promoter_designer.cli model-figures --output-dir outputs/model_figures_bundle

legacy-figures: model-figures

reproduce-results:
	PYTHONPATH=src $(PYTHON) scripts/reproduce_legacy_outputs.py

reproduce-legacy: reproduce-results

supplement-figures-r:
	Rscript scripts/render_FigS1_quantitative_reference.R
	Rscript scripts/render_FigS2_expression_heatmap.R
	Rscript scripts/render_FigS3_dnabert_motif_summary.R
	Rscript scripts/render_FigS4_kmer_distribution.R
	Rscript scripts/render_FigS5_design_candidate_summary.R

sync-data:
	PYTHONPATH=src $(PYTHON) scripts/sync_repository_data.py

validate:
	PYTHONPATH=src $(PYTHON) -m tomato_promoter_designer.cli validate-input --input examples/demo_input.fasta

train-mpravae-smoke:
	PYTHONPATH=src $(PYTHON) scripts/train_mpravae.py --config configs/training_mpravae.yaml --max-rows 8 --epochs 1 --output-checkpoint tmp/test_mpravae_train.pth --metrics-json tmp/test_mpravae_metrics.json
	PYTHONPATH=src $(PYTHON) -m tomato_promoter_designer.cli predict-mpravae --input examples/demo_input.fasta --output tmp/test_mpravae_predict.csv --checkpoint tmp/test_mpravae_train.pth

package:
	$(PYTHON) -m build

clean:
	rm -rf build dist .pytest_cache .coverage htmlcov outputs tmp
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
