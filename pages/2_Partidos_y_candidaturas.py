from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import plotly.express as px
import streamlit as st

from observatorio.data_loader import load_all
from observatorio.metrics import money_by
from observatorio.ui import mvp_notice, page_setup


page_setup("Partidos y candidaturas")
data = load_all()
casos = data["casos"]
sanciones = data["sanciones"]

st.title("Partidos y candidaturas")
mvp_notice()

if sanciones.empty:
    st.info("No hay sanciones cargadas.")
else:
    st.subheader("Monto original por sujeto")
    chart_df = money_by(sanciones, "sujeto_nombre", "monto_original")
    fig = px.bar(chart_df, x="monto_original", y="sujeto_nombre", orientation="h")
    colors = ["#FF6600" if x == "Movimiento Ciudadano" else "#6B1531" if x == "Morena" else "#2B5C8A" if x == "Partido Accion Nacional" else "#1E5B4F" for x in chart_df["sujeto_nombre"]]
    fig.update_traces(marker_color=colors)
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Personas candidatas en la muestra")
cols = ["expediente", "persona_candidata", "partido_principal", "consecuencia_no_economica", "gravedad_textual"]
available = [c for c in cols if c in casos.columns]
st.dataframe(casos[available], use_container_width=True, hide_index=True)
