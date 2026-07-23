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


page_setup("Descargas TEPJF 2023-2024")

manifest_path = ROOT / "data" / "interim" / "tepjf_diputaciones_2023_2024_manifest.csv"

st.title("Descargas TEPJF 2023-2024")
st.caption(
    "Inventario de expedientes localizados con filtros de diputaciones federales, "
    "candidaturas, computos distritales, asignacion RP y fiscalizacion."
)

if not manifest_path.exists():
    st.info("Aun no existe manifiesto de descargas.")
else:
    manifest = pd.read_csv(manifest_path, keep_default_na=False)
    cols = st.columns(4)
    cols[0].metric("Inventario", len(manifest))
    cols[1].metric("Descargadas", int((manifest["status"] == "descargado").sum()))
    cols[2].metric("CAPTCHA portal", int((manifest["status"] == "captcha_portal").sum()))
    cols[3].metric("Anios", manifest["year"].nunique())

    year = st.multiselect("Anio", sorted(manifest["year"].unique()), default=sorted(manifest["year"].unique()))
    status = st.multiselect("Estado", sorted(manifest["status"].unique()), default=sorted(manifest["status"].unique()))
    topic = st.multiselect("Tema", sorted(manifest["tema"].unique()), default=sorted(manifest["tema"].unique()))

    view = manifest[
        manifest["year"].isin(year)
        & manifest["status"].isin(status)
        & manifest["tema"].isin(topic)
    ]
    st.dataframe(
        view[["expediente", "year", "tema", "status", "file_size", "filename", "url"]],
        use_container_width=True,
        hide_index=True,
    )
