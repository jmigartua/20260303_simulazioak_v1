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


def test_validate_consistency_success() -> None:
    mod = _load_module(
        "scripts/check_release_consistency.py",
        "check_release_consistency",
    )
    errors = mod.validate_consistency("0.1.2rc2", ["0.1.2rc2", "0.1.1"])
    assert errors == []


def test_validate_consistency_missing_project_version() -> None:
    mod = _load_module(
        "scripts/check_release_consistency.py",
        "check_release_consistency_missing",
    )
    errors = mod.validate_consistency("0.1.2rc2", ["0.1.1"])
    assert len(errors) == 2
    assert "missing from CHANGELOG.md headings" in errors[0]


def test_changelog_versions_parser(tmp_path: Path) -> None:
    mod = _load_module(
        "scripts/check_release_consistency.py",
        "check_release_consistency_parser",
    )
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text(
        "# Changelog\n\n## [0.1.2rc2] - 2026-03-04\n\n## [0.1.1] - 2026-03-04\n",
        encoding="utf-8",
    )
    versions = mod.changelog_versions(changelog)
    assert versions == ["0.1.2rc2", "0.1.1"]
