from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components

from observatorio.data_loader import load_all
from observatorio.metrics import count_by, kpis, money_by
from observatorio.ui import format_money, page_setup, responsive_kpi_grid


page_setup("Reporte imprimible")
data = load_all()
casos = data["casos"]
sanciones = data["sanciones"]
agravios = data["agravios"]
stats = kpis(casos, sanciones, agravios)

st.markdown(
    """
    <div class="print-title">
      <div class="print-kicker">Fiscalizacion electoral | Diputaciones federales 2024</div>
      <h1>Observatorio de Fiscalizacion y Justicia Electoral</h1>
      <p class="source-note">Formato optimizado para imprimir en carta horizontal. Paleta editorial: guinda, dorado y verde; naranja reservado para MC.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

responsive_kpi_grid(
    [
        ("Sentencias", stats["casos"]),
        ("Partidos/coaliciones", stats["sujetos"]),
        ("Conclusiones/sanciones", stats["sanciones"]),
        ("Monto original", format_money(stats["monto_original"])),
        ("Agravios", stats["agravios"]),
    ],
    money_labels={"Monto original"},
)

left, right = st.columns([1, 1])
with left:
    st.subheader("Sentido jurisdiccional")
    sentido = count_by(casos, "sentido")
    if not sentido.empty:
        st.plotly_chart(px.bar(sentido, x="casos", y="sentido", orientation="h", color_discrete_sequence=["#6B1531"]), width="stretch")

with right:
    st.subheader("Monto por sujeto")
    montos = money_by(sanciones, "sujeto_nombre", "monto_original")
    if not montos.empty:
        colors = ["#FF6600" if x == "Movimiento Ciudadano" else "#6B1531" if x == "Morena" else "#2B5C8A" if x == "Partido Accion Nacional" else "#1E5B4F" for x in montos["sujeto_nombre"]]
        fig = px.bar(montos, x="monto_original", y="sujeto_nombre", orientation="h")
        fig.update_traces(marker_color=colors)
        st.plotly_chart(fig, width="stretch")

st.subheader("Expedientes reales incorporados")
cols = ["expediente", "fecha_sentencia", "parte_actora", "sala", "sentido", "efectos_resumen"]
st.dataframe(casos[cols], width="stretch", hide_index=True)

st.subheader("Notas metodologicas para lectura impresa")
st.markdown(
    """
- Corpus inicial: sentencias oficiales localizadas sobre fiscalizacion de campana federal 2023-2024 con incidencia en diputaciones federales.
- No equivale al universo completo de resoluciones administrativas del INE.
- Los montos se reportan solo cuando aparecen en los fragmentos extraidos o en la sentencia consultada.
- Las salas regionales que bloquearon descarga automatica conservan URL oficial y quedan marcadas como descarga local pendiente.
"""
)

components.html("<script>function p(){window.parent.print()}</script><button onclick='p()'>Imprimir carta horizontal</button>", height=45)
