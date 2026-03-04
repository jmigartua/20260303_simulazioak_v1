from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def _load_module(rel_path: str, module_name: str):
    root = Path(__file__).resolve().parents[2]
    script_path = root / rel_path
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module from {script_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def test_layer_resolution_rules() -> None:
    mod = _load_module("scripts/check_import_flow.py", "check_import_flow")

    assert mod._layer_from_module("sim_framework.contracts.models") == "contracts"
    assert mod._layer_from_module("sim_framework.core.engine") == "core"
    assert mod._layer_from_module("sim_framework.scenarios.registry") == "scenarios"
    assert mod._layer_from_module("sim_framework.app.cli") == "app"
    assert mod._layer_from_module("json") is None
    assert mod._layer_from_module("sim_framework") is None


def test_validate_import_flow_flags_invalid_direction() -> None:
    mod = _load_module("scripts/check_import_flow.py", "check_import_flow")
    use = mod.ImportUse(
        source_file=Path("sim_framework/contracts/foo.py"),
        source_layer="contracts",
        imported_module="sim_framework.core.engine",
        imported_layer="core",
        line=7,
    )

    violations = mod.validate_import_flow([use])
    assert len(violations) == 1
    assert violations[0].imported_layer == "core"


def test_project_import_flow_has_no_violations() -> None:
    mod = _load_module("scripts/check_import_flow.py", "check_import_flow")
    uses = mod.collect_imports()
    violations = mod.validate_import_flow(uses)

    assert uses
    assert not violations
