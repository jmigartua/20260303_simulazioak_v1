from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load_module(rel_path: str, module_name: str):
    root = Path(__file__).resolve().parents[2]
    script_path = root / rel_path
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module from {script_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module
