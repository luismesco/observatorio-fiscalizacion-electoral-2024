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
from observatorio.metrics import count_by
from observatorio.ui import mvp_notice, page_setup


page_setup("Agravios y criterios")
data = load_all()
agravios = data["agravios"]
votos = data["votos"]

st.title("Agravios y criterios")
mvp_notice()

left, right = st.columns(2)
with left:
    st.subheader("Categoria de agravio")
    chart_df = count_by(agravios, "categoria", "agravios")
    st.plotly_chart(px.bar(chart_df, x="agravios", y="categoria", orientation="h", color_discrete_sequence=["#1E5B4F"]), use_container_width=True)

with right:
    st.subheader("Calificacion")
    chart_df = count_by(agravios, "calificacion", "agravios")
    st.plotly_chart(px.bar(chart_df, x="agravios", y="calificacion", orientation="h", color_discrete_sequence=["#6B1531"]), use_container_width=True)

st.subheader("Votos separados")
if votos.empty:
    st.info("Vista preparada para fase exhaustiva. La muestra actual no permite una inferencia general.")
else:
    st.dataframe(votos, use_container_width=True, hide_index=True)
