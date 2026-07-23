from __future__ import annotations

import pandas as pd


def money(series: pd.Series) -> float:
    if series.empty:
        return 0.0
    return pd.to_numeric(series, errors="coerce").fillna(0).sum()


def kpis(casos: pd.DataFrame, sanciones: pd.DataFrame, agravios: pd.DataFrame) -> dict[str, float | int]:
    caso_ids = set(casos.get("caso_id", pd.Series(dtype=str)).astype(str))
    sanciones_scope = sanciones
    agravios_scope = agravios
    if caso_ids:
        sanciones_scope = sanciones[sanciones.get("caso_id", "").astype(str).isin(caso_ids)]
        agravios_scope = agravios[agravios.get("caso_id", "").astype(str).isin(caso_ids)]
    return {
        "casos": int(len(casos)),
        "sujetos": int(casos.get("partido_principal", pd.Series(dtype=str)).nunique()),
        "sanciones": int(len(sanciones_scope)),
        "monto_original": money(sanciones_scope.get("monto_original", pd.Series(dtype=float))),
        "monto_final": money(sanciones_scope.get("monto_final", pd.Series(dtype=float))),
        "agravios": int(len(agravios_scope)),
    }


def count_by(df: pd.DataFrame, column: str, value_name: str = "casos") -> pd.DataFrame:
    if df.empty or column not in df:
        return pd.DataFrame(columns=[column, value_name])
    return (
        df.groupby(column, dropna=False)
        .size()
        .reset_index(name=value_name)
        .sort_values(value_name, ascending=True)
    )


def money_by(sanciones: pd.DataFrame, column: str, amount: str = "monto_original") -> pd.DataFrame:
    if sanciones.empty or column not in sanciones or amount not in sanciones:
        return pd.DataFrame(columns=[column, amount])
    out = sanciones.copy()
    out[amount] = pd.to_numeric(out[amount], errors="coerce").fillna(0)
    return out.groupby(column, dropna=False)[amount].sum().reset_index().sort_values(amount, ascending=True)

