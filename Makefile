PYTHON ?= .venv/bin/python

.PHONY: help test test-v import-check release-consistency package-check ci-local release-check run-app perf-snapshot-toggle perf-smoke

help:
	@echo "Available targets:"
	@echo "  test                 Run test suite (quiet)"
	@echo "  test-v               Run test suite (verbose)"
	@echo "  import-check         Validate layer import direction"
	@echo "  release-consistency  Validate pyproject/changelog version consistency"
	@echo "  package-check        Validate editable install and dependency health"
	@echo "  ci-local             Run import-check + test-v"
	@echo "  release-check        Run import-check + test-v + package-check"
	@echo "  run-app              Run app CLI in interactive mode"
	@echo "  perf-snapshot-toggle Run reproducible ON/OFF perf comparison"
	@echo "  perf-smoke           Run lightweight ON/OFF benchmark smoke"

test:
	$(PYTHON) -m pytest -q

test-v:
	$(PYTHON) -m pytest -v

import-check:
	$(PYTHON) scripts/check_import_flow.py

release-consistency:
	$(PYTHON) scripts/check_release_consistency.py

package-check:
	@if command -v uv >/dev/null 2>&1; then \
		uv pip install --python $(PYTHON) -e . ; \
	else \
		$(PYTHON) -m ensurepip --upgrade ; \
		$(PYTHON) -m pip install -e . ; \
	fi

ci-local: import-check test-v

release-check: release-consistency import-check test-v package-check

run-app:
	$(PYTHON) -m sim_framework.app.cli --scenario ants_foraging --ticks 100 --runtime-mode interactive

perf-snapshot-toggle:
	$(PYTHON) scripts/run_perf_snapshot_toggle.py --agents 100,300 --ticks 100 --repeats 3

perf-smoke:
	$(PYTHON) scripts/run_perf_snapshot_toggle.py --agents 20 --ticks 10 --repeats 1 --label local_smoke --output-dir Plans
