PYTHON ?= python

.PHONY: install install-dev test demo validate package legacy-figures reproduce-legacy sync-data clean

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

legacy-figures:
	PYTHONPATH=src $(PYTHON) -m tomato_promoter_designer.cli legacy-figures --output-dir outputs/legacy_figures_bundle

reproduce-legacy:
	PYTHONPATH=src $(PYTHON) scripts/reproduce_legacy_outputs.py

sync-data:
	PYTHONPATH=src $(PYTHON) scripts/sync_repository_data.py

validate:
	PYTHONPATH=src $(PYTHON) -m tomato_promoter_designer.cli validate-input --input examples/demo_input.fasta

package:
	$(PYTHON) -m build

clean:
	rm -rf build dist .pytest_cache .coverage htmlcov outputs tmp
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
