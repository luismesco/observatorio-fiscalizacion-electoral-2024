from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import streamlit as st

from observatorio.data_loader import load_all
from observatorio.ui import page_setup


page_setup("Hallazgos portal TEPJF")
data = load_all()
hallazgos = data.get("hallazgos_portal")

st.title("Hallazgos del portal TEPJF")
st.caption(
    "Expedientes localizados con filtros de diputacion federal, fiscalizacion, candidato, "
    "INE/Q-COF-UTF, rebase de tope y casos mediaticos. El estado distingue descargas "
    "reales de bloqueos CAPTCHA del portal."
)

if hallazgos is None or hallazgos.empty:
    st.info("No hay hallazgos registrados.")
else:
    prioridad = st.multiselect(
        "Prioridad",
        sorted(hallazgos["prioridad"].unique()),
        default=sorted(hallazgos["prioridad"].unique()),
    )
    estado = st.multiselect(
        "Estado de descarga",
        sorted(hallazgos["estado_descarga"].unique()),
        default=sorted(hallazgos["estado_descarga"].unique()),
    )
    filtered = hallazgos[
        hallazgos["prioridad"].isin(prioridad)
        & hallazgos["estado_descarga"].isin(estado)
    ]
    st.dataframe(
        filtered[
            [
                "prioridad",
                "expediente",
                "fecha",
                "candidatura",
                "partido_o_coalicion",
                "entidad",
                "distrito",
                "tema",
                "estado_descarga",
                "accion_mvp",
                "url_oficial",
            ]
        ],
        width="stretch",
        hide_index=True,
    )
