from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import pandas as pd
import plotly.express as px
import streamlit as st

from observatorio.ui import page_setup


page_setup("Analisis corpus TEPJF")

analysis_dir = ROOT / "data" / "analysis"
summary_path = analysis_dir / "tepjf_corpus_resumen.csv"
snippets_path = analysis_dir / "tepjf_corpus_fragmentos.csv"
personas_path = analysis_dir / "tepjf_personas_detectadas.csv"

st.title("Analisis del corpus TEPJF")
st.caption("Lectura automatica de 52 sentencias descargadas del portal TEPJF sobre diputaciones 2023-2024.")

if not summary_path.exists():
    st.info("Ejecuta scripts/analyze_tepjf_corpus.py para generar el analisis.")
else:
    resumen = pd.read_csv(summary_path, keep_default_na=False)
    snippets = pd.read_csv(snippets_path, keep_default_na=False) if snippets_path.exists() else pd.DataFrame()
    personas = pd.read_csv(personas_path, keep_default_na=False) if personas_path.exists() else pd.DataFrame()

    cols = st.columns(5)
    cols[0].metric("Sentencias", len(resumen))
    cols[1].metric("Fiscalizacion", int(resumen["fiscalizacion"].sum()))
    cols[2].metric("Constancia mayoria", int(resumen["constancia_mayoria"].sum()))
    cols[3].metric("Rebase/tope", int(resumen["rebase_tope"].sum()))
    cols[4].metric("Personas detectadas", personas["persona_detectada"].nunique() if not personas.empty else 0)

    left, right = st.columns([1, 1])
    with left:
        temas = resumen.groupby("tema_inventario", as_index=False).size().sort_values("size", ascending=True)
        st.plotly_chart(px.bar(temas, x="size", y="tema_inventario", orientation="h", color_discrete_sequence=["#6B1531"]), use_container_width=True)
    with right:
        medios = resumen.groupby("medio", as_index=False).size().sort_values("size", ascending=True)
        st.plotly_chart(px.bar(medios, x="size", y="medio", orientation="h", color_discrete_sequence=["#1E5B4F"]), use_container_width=True)

    st.subheader("Matriz de lectura")
    st.dataframe(resumen, use_container_width=True, hide_index=True)

    st.subheader("Fragmentos clave")
    categoria = st.multiselect("Categoria", sorted(snippets["categoria"].unique()) if not snippets.empty else [], default=sorted(snippets["categoria"].unique()) if not snippets.empty else [])
    if not snippets.empty:
        view = snippets[snippets["categoria"].isin(categoria)] if categoria else snippets
        st.dataframe(view, use_container_width=True, hide_index=True)

    st.subheader("Personas detectadas en contexto")
    if personas.empty:
        st.info("No se detectaron personas con los patrones actuales.")
    else:
        st.dataframe(personas, use_container_width=True, hide_index=True)
