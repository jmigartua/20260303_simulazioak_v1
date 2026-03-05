#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PYPROJECT_PATH = PROJECT_ROOT / "pyproject.toml"
CHANGELOG_PATH = PROJECT_ROOT / "CHANGELOG.md"
CHANGELOG_HEADING_RE = re.compile(r"^## \[(?P<version>[^\]]+)\]")
UNRELEASED_HEADING = "unreleased"


def load_project_version(pyproject_path: Path) -> str:
    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    return str(data["project"]["version"])


def changelog_versions(changelog_path: Path) -> list[str]:
    versions: list[str] = []
    for line in changelog_path.read_text(encoding="utf-8").splitlines():
        match = CHANGELOG_HEADING_RE.match(line.strip())
        if match:
            versions.append(match.group("version"))
    return versions


def validate_consistency(project_version: str, versions: list[str]) -> list[str]:
    errors: list[str] = []
    if not versions:
        errors.append("CHANGELOG.md has no version headings (expected '## [x.y.z]').")
        return errors

    released_versions = [v for v in versions if v.strip().lower() != UNRELEASED_HEADING]
    if not released_versions:
        errors.append("CHANGELOG.md has no released version headings (expected '## [x.y.z]').")
        return errors

    if project_version not in released_versions:
        errors.append(
            f"pyproject version '{project_version}' missing from CHANGELOG.md headings."
        )
    if released_versions[0] != project_version:
        errors.append(
            "latest released changelog heading is "
            f"'{released_versions[0]}', expected '{project_version}'."
        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check release consistency between pyproject version and changelog headings."
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=PROJECT_ROOT,
        help="Project root containing pyproject.toml and CHANGELOG.md.",
    )
    args = parser.parse_args()

    pyproject_path = args.project_root / "pyproject.toml"
    changelog_path = args.project_root / "CHANGELOG.md"
    project_version = load_project_version(pyproject_path)
    versions = changelog_versions(changelog_path)
    errors = validate_consistency(project_version, versions)

    print(f"pyproject version: {project_version}")
    print(f"changelog headings: {', '.join(versions) if versions else '(none)'}")
    if errors:
        print("Result: FAIL")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Result: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
