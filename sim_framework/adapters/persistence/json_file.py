from __future__ import annotations

from pathlib import Path

from sim_framework.contracts.models import LoadedRun, RunManifest, SimulationState


class JsonFilePersistence:
    """Simple file-based persistence adapter for run manifests + snapshots."""

    def __init__(self, root: str | Path) -> None:
        self._root = Path(root)

    def _run_file(self, run_id: str) -> Path:
        return self._root / run_id / "run.json"

    def save_run(self, manifest: RunManifest, snapshots: list[SimulationState]) -> str:
        run_file = self._run_file(manifest.run_id)
        run_file.parent.mkdir(parents=True, exist_ok=True)

        bundle = LoadedRun(
            manifest=manifest.model_copy(deep=True),
            snapshots=[snapshot.model_copy(deep=True) for snapshot in snapshots],
        )
        run_file.write_text(bundle.model_dump_json(indent=2) + "\n", encoding="utf-8")
        return manifest.run_id

    def load_run(self, run_id: str) -> LoadedRun:
        run_file = self._run_file(run_id)
        if not run_file.exists():
            raise FileNotFoundError(f"Run not found: {run_id}")
        return LoadedRun.model_validate_json(run_file.read_text(encoding="utf-8"))

