from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import pandas as pd
import streamlit as st

from observatorio.ui import page_setup


page_setup("TFJA y delitos electorales")

path = ROOT / "data" / "analysis" / "tfja_fisel_screening.csv"

st.title("Cruce TFJA / FISEL")
st.caption(
    "Matriz preliminar para verificar si personas detectadas en sentencias de diputaciones "
    "aparecen con faltas administrativas, sanciones firmes o posibles delitos electorales."
)

st.warning(
    "El TFJA conoce responsabilidades administrativas; los delitos electorales corresponden "
    "a fiscalias/FISEL y organos penales. Esta tabla no prueba inexistencia de sanciones: "
    "documenta fuentes consultadas, bloqueos tecnicos y pendientes de validacion."
)

if not path.exists():
    st.info("No existe matriz de verificacion.")
else:
    data = pd.read_csv(path, keep_default_na=False)
    estado = st.multiselect("Estado", sorted(data["estado_verificacion"].unique()), default=sorted(data["estado_verificacion"].unique()))
    view = data[data["estado_verificacion"].isin(estado)]
    st.dataframe(view, width="stretch", hide_index=True)

    st.subheader("Fuentes oficiales para continuar")
    st.markdown(
        """
- TFJA: Sistema de Consulta de Servidores Publicos Sancionados.
- TFJA: Consulta de sentencia.
- FISEL/FGR: comunicados y material de delitos electorales.
- Plataforma Digital Nacional/SFP: registro de personas servidoras publicas y particulares sancionados.
"""
    )
