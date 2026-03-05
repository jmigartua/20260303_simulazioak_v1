from pathlib import Path

from tests.tooling.helpers import load_module


def test_layer_resolution_rules() -> None:
    mod = load_module("scripts/check_import_flow.py", "check_import_flow")

    assert mod._layer_from_module("sim_framework.contracts.models") == "contracts"
    assert mod._layer_from_module("sim_framework.core.engine") == "core"
    assert mod._layer_from_module("sim_framework.scenarios.registry") == "scenarios"
    assert mod._layer_from_module("sim_framework.adapters.web.runtime_bridge") == "adapters"
    assert mod._layer_from_module("sim_framework.app.cli") == "app"
    assert mod._layer_from_module("json") is None
    assert mod._layer_from_module("sim_framework") is None


def test_validate_import_flow_flags_invalid_direction() -> None:
    mod = load_module("scripts/check_import_flow.py", "check_import_flow")
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
    mod = load_module("scripts/check_import_flow.py", "check_import_flow")
    uses = mod.collect_imports()
    violations = mod.validate_import_flow(uses)

    assert uses
    assert not violations
