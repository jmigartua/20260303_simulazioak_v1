#!/usr/bin/env python3
from __future__ import annotations

import ast
import sys
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = PROJECT_ROOT / "sim_framework"


ALLOWED_IMPORTS: dict[str, set[str]] = {
    "contracts": {"contracts"},
    "core": {"contracts", "core"},
    "scenarios": {"contracts", "core", "scenarios"},
    "app": {"contracts", "core", "scenarios", "app"},
}


@dataclass(frozen=True)
class ImportUse:
    source_file: Path
    source_layer: str
    imported_module: str
    imported_layer: str
    line: int


def _layer_from_source(path: Path) -> str | None:
    rel = path.relative_to(PACKAGE_ROOT)
    if not rel.parts:
        return None
    layer = rel.parts[0]
    return layer if layer in ALLOWED_IMPORTS else None


def _layer_from_module(module: str) -> str | None:
    if module == "sim_framework":
        return None
    if not module.startswith("sim_framework."):
        return None
    parts = module.split(".")
    if len(parts) < 2:
        return None
    layer = parts[1]
    return layer if layer in ALLOWED_IMPORTS else None


def _iter_imports(path: Path) -> list[tuple[str, int]]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    out: list[tuple[str, int]] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module is None:
                continue
            out.append((node.module, node.lineno))
        elif isinstance(node, ast.Import):
            for alias in node.names:
                out.append((alias.name, node.lineno))
    return out


def collect_imports() -> list[ImportUse]:
    uses: list[ImportUse] = []

    for path in PACKAGE_ROOT.rglob("*.py"):
        source_layer = _layer_from_source(path)
        if source_layer is None:
            continue
        for module, line in _iter_imports(path):
            imported_layer = _layer_from_module(module)
            if imported_layer is None:
                continue
            uses.append(
                ImportUse(
                    source_file=path,
                    source_layer=source_layer,
                    imported_module=module,
                    imported_layer=imported_layer,
                    line=line,
                )
            )
    return uses


def validate_import_flow(uses: list[ImportUse]) -> list[ImportUse]:
    violations: list[ImportUse] = []
    for use in uses:
        if use.imported_layer not in ALLOWED_IMPORTS[use.source_layer]:
            violations.append(use)
    return violations


def main() -> int:
    uses = collect_imports()
    violations = validate_import_flow(uses)

    print(f"Total imports: {len(uses)}")
    print("Expected flow: contracts <- core <- scenarios <- app")

    if violations:
        print("\nViolations:")
        for item in violations:
            rel = item.source_file.relative_to(PROJECT_ROOT)
            print(
                f"- {rel}:{item.line} "
                f"{item.source_layer} imports {item.imported_module}"
            )
        return 1

    print("Result: OK (0 violations)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
