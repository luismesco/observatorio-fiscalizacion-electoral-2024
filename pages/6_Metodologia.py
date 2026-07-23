from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import streamlit as st

from observatorio.data_loader import load_all
from observatorio.ui import mvp_notice, page_setup
from observatorio.validators import audit_cases


page_setup("Metodologia")
data = load_all()
casos = data["casos"]

st.title("Metodologia")
mvp_notice()

st.subheader("Reglas del corte")
st.write(
    "El observatorio separa competencias federal y local, conserva fuente para cada dato relevante "
    "y no convierte una muestra en afirmacion exhaustiva."
)

st.subheader("Control de calidad")
issues = audit_cases(casos)
if issues:
    for issue in issues:
        st.warning(issue)
else:
    st.success("La estructura minima de casos no reporta faltantes criticos.")

st.subheader("Campos clave")
st.markdown(
    """
- `nivel`: Federal o CDMX.
- `acto_origen_resumen`: resolucion, dictamen o procedimiento del que deriva la impugnacion.
- `sentido`: resultado jurisdiccional.
- `monto_final_estado`: firme, pendiente, desconocido o no aplica.
- `revision_humana`: estado de control antes de presentar datos reales.
- `fragmento_fuente`: evidencia textual del dato capturado.
"""
)
