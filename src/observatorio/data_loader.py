from __future__ import annotations

from pathlib import Path

import pandas as pd

from .paths import data_dir


TABLES = {
    "casos": "casos.csv",
    "sanciones": "sanciones.csv",
    "agravios": "agravios.csv",
    "sujetos": "sujetos.csv",
    "actos_origen": "actos_origen.csv",
    "votos": "votos.csv",
    "fuentes": "fuentes.csv",
    "hallazgos_portal": "hallazgos_portal.csv",
}


def _read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, keep_default_na=False)


def load_table(name: str, base_dir: Path | None = None) -> pd.DataFrame:
    if name not in TABLES:
        raise KeyError(f"Tabla no configurada: {name}")
    base = base_dir or data_dir()
    return _read_csv(base / TABLES[name])


def load_all(base_dir: Path | None = None) -> dict[str, pd.DataFrame]:
    base = base_dir or data_dir()
    return {name: _read_csv(base / filename) for name, filename in TABLES.items()}


def filtered_cases(
    casos: pd.DataFrame,
    nivel: list[str] | None = None,
    partido: list[str] | None = None,
    conducta: list[str] | None = None,
    sentido: list[str] | None = None,
) -> pd.DataFrame:
    if casos.empty:
        return casos
    out = casos.copy()
    filters = {
        "nivel": nivel,
        "partido_principal": partido,
        "conducta_principal": conducta,
        "sentido": sentido,
    }
    for column, values in filters.items():
        if values and column in out.columns:
            out = out[out[column].isin(values)]
    return out
