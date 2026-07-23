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


page_setup("Expedientes")
data = load_all()
casos = data["casos"]
agravios = data["agravios"]
sanciones = data["sanciones"]

st.title("Expedientes")
mvp_notice()

if casos.empty:
    st.info("No hay casos cargados.")
    st.stop()

expediente = st.selectbox("Seleccionar expediente", casos["expediente"].tolist())
caso = casos[casos["expediente"] == expediente].iloc[0]
caso_id = str(caso["caso_id"])

st.subheader(expediente)
left, right = st.columns([1, 1])
with left:
    st.write(f"**Nivel:** {caso.get('nivel', '')}")
    st.write(f"**Organo:** {caso.get('organo_resolutor', '')}")
    st.write(f"**Sentido:** {caso.get('sentido', '')}")
    st.write(f"**Actor:** {caso.get('parte_actora', '')}")
with right:
    st.write(f"**Acto de origen:** {caso.get('acto_origen_resumen', '')}")
    st.write(f"**Efectos:** {caso.get('efectos_resumen', '')}")
    st.write(f"**Fuente:** {caso.get('url_sentencia', '')}")
    st.write(f"**Revision:** {caso.get('revision_humana', '')}")

st.subheader("Trayectoria")
st.code(
    f"Acto de origen -> {caso.get('conducta_principal', 'sin dato')} -> Impugnacion -> {caso.get('sentido', 'sin dato')} -> {caso.get('monto_final_estado', 'sin dato')}",
    language="text",
)

st.subheader("Sanciones vinculadas")
st.dataframe(sanciones[sanciones["caso_id"].astype(str) == caso_id], use_container_width=True, hide_index=True)

st.subheader("Agravios")
st.dataframe(agravios[agravios["caso_id"].astype(str) == caso_id], use_container_width=True, hide_index=True)

