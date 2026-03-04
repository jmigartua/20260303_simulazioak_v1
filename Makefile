PYTHON ?= .venv/bin/python

.PHONY: help test test-v import-check ci-local run-app perf-snapshot-toggle

help:
	@echo "Available targets:"
	@echo "  test                 Run test suite (quiet)"
	@echo "  test-v               Run test suite (verbose)"
	@echo "  import-check         Validate layer import direction"
	@echo "  ci-local             Run import-check + test-v"
	@echo "  run-app              Run app CLI in interactive mode"
	@echo "  perf-snapshot-toggle Run reproducible ON/OFF perf comparison"

test:
	$(PYTHON) -m pytest -q

test-v:
	$(PYTHON) -m pytest -v

import-check:
	$(PYTHON) scripts/check_import_flow.py

ci-local: import-check test-v

run-app:
	$(PYTHON) -m sim_framework.app.cli --scenario ants_foraging --ticks 100 --runtime-mode interactive

perf-snapshot-toggle:
	$(PYTHON) scripts/run_perf_snapshot_toggle.py --agents 100,300 --ticks 100 --repeats 3
