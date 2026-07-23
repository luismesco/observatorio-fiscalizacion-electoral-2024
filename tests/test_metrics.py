from __future__ import annotations

import pandas as pd

from observatorio.metrics import count_by, kpis, money


def test_money_coerces_invalid_values() -> None:
    assert money(pd.Series(["10", "bad", "5.5"])) == 15.5


def test_count_by_returns_counts() -> None:
    df = pd.DataFrame({"sentido": ["confirma", "confirma", "revoca"]})
    out = count_by(df, "sentido")
    assert out["casos"].sum() == 3


def test_kpis_scopes_by_case_ids() -> None:
    casos = pd.DataFrame({"caso_id": ["A"], "partido_principal": ["P1"]})
    sanciones = pd.DataFrame({"caso_id": ["A", "B"], "monto_original": [100, 900], "monto_final": [50, 900]})
    agravios = pd.DataFrame({"caso_id": ["A", "B"]})
    stats = kpis(casos, sanciones, agravios)
    assert stats["monto_original"] == 100
    assert stats["agravios"] == 1

