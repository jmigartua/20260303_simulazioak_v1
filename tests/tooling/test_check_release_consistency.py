from pathlib import Path

from tests.tooling.helpers import load_module


def test_validate_consistency_success() -> None:
    mod = load_module(
        "scripts/check_release_consistency.py",
        "check_release_consistency",
    )
    errors = mod.validate_consistency("0.1.2rc2", ["Unreleased", "0.1.2rc2", "0.1.1"])
    assert errors == []


def test_validate_consistency_missing_project_version() -> None:
    mod = load_module(
        "scripts/check_release_consistency.py",
        "check_release_consistency_missing",
    )
    errors = mod.validate_consistency("0.1.2rc2", ["0.1.1"])
    assert len(errors) == 2
    assert "missing from CHANGELOG.md headings" in errors[0]


def test_changelog_versions_parser(tmp_path: Path) -> None:
    mod = load_module(
        "scripts/check_release_consistency.py",
        "check_release_consistency_parser",
    )
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text(
        "# Changelog\n\n## [Unreleased]\n\n## [0.1.2rc2] - 2026-03-04\n\n## [0.1.1] - 2026-03-04\n",
        encoding="utf-8",
    )
    versions = mod.changelog_versions(changelog)
    assert versions == ["Unreleased", "0.1.2rc2", "0.1.1"]


def test_validate_consistency_requires_latest_released_to_match() -> None:
    mod = load_module(
        "scripts/check_release_consistency.py",
        "check_release_consistency_latest_released",
    )
    errors = mod.validate_consistency("0.1.2rc2", ["Unreleased", "0.1.1"])
    assert len(errors) == 2
    assert "missing from CHANGELOG.md headings" in errors[0]
    assert "latest released changelog heading is '0.1.1'" in errors[1]
