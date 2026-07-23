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
from observatorio.metrics import count_by, money_by
from observatorio.ui import mvp_notice, page_setup


page_setup("Conductas y sanciones")
data = load_all()
casos = data["casos"]
sanciones = data["sanciones"]

st.title("Conductas y sanciones")
mvp_notice()

left, right = st.columns(2)
with left:
    st.subheader("Frecuencia por conducta")
    chart_df = count_by(casos, "conducta_principal")
    st.plotly_chart(px.bar(chart_df, x="casos", y="conducta_principal", orientation="h", color_discrete_sequence=["#6B1531"]), use_container_width=True)

with right:
    st.subheader("Monto original por conducta")
    chart_df = money_by(sanciones, "conducta", "monto_original")
    st.plotly_chart(px.bar(chart_df, x="monto_original", y="conducta", orientation="h", color_discrete_sequence=["#1E5B4F"]), use_container_width=True)

st.subheader("Detalle de sanciones")
st.dataframe(sanciones, use_container_width=True, hide_index=True)
