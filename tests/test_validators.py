from __future__ import annotations

import pandas as pd

from observatorio.validators import audit_cases, validate_expediente


def test_validate_demo_expediente() -> None:
    assert validate_expediente("DEMO-FED-001")


def test_audit_reports_missing_columns() -> None:
    issues = audit_cases(pd.DataFrame({"caso_id": ["A"]}))
    assert any("Falta columna obligatoria" in issue for issue in issues)

