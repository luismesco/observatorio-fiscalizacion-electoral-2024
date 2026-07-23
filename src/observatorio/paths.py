from __future__ import annotations

import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def project_root() -> Path:
    return PROJECT_ROOT


def data_dir() -> Path:
    configured = os.environ.get("OBSERVATORIO_DATA_DIR", "data/processed")
    path = Path(configured)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path


def export_dir() -> Path:
    path = PROJECT_ROOT / "exports"
    path.mkdir(exist_ok=True)
    return path
