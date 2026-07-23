from __future__ import annotations

import re

import pandas as pd


EXPEDIENTE_PATTERN = re.compile(r"^[A-Z]{2,5}-[A-Z0-9-]+/\d{4}$|^DEMO-[A-Z0-9-]+$")


def validate_expediente(value: str) -> bool:
    return bool(EXPEDIENTE_PATTERN.match(str(value).strip()))


def audit_cases(casos: pd.DataFrame) -> list[str]:
    issues: list[str] = []
    required = ["caso_id", "nivel", "expediente", "sentido", "url_sentencia", "revision_humana"]
    for column in required:
        if column not in casos.columns:
            issues.append(f"Falta columna obligatoria: {column}")
    if "expediente" in casos:
        invalid = casos[~casos["expediente"].map(validate_expediente)]
        if not invalid.empty:
            issues.append(f"Expedientes con formato no valido: {len(invalid)}")
    if "revision_humana" in casos:
        pending = casos[~casos["revision_humana"].astype(str).str.lower().isin(["si", "validado"])]
        if not pending.empty:
            issues.append(f"Casos pendientes de revision humana: {len(pending)}")
    return issues

