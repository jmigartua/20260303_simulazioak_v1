from __future__ import annotations

import sys

import pytest


def pytest_sessionstart(session: pytest.Session) -> None:
    """Fail fast when tests run outside the supported Python policy."""
    _ = session
    if sys.version_info < (3, 11):
        pytest.exit(
            "Python >= 3.11 is required for this project. "
            "Use `.venv/bin/python -m pytest ...`.",
            returncode=2,
        )
