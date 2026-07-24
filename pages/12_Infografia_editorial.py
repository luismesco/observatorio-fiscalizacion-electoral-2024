from __future__ import annotations

import base64
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import pandas as pd
import plotly.express as px
import streamlit as st

from observatorio.ui import page_setup, responsive_kpi_grid


page_setup("Infografia editorial")

analysis = ROOT / "data" / "analysis"
resumen = pd.read_csv(analysis / "tepjf_corpus_resumen.csv", keep_default_na=False)
tfja = pd.read_csv(analysis / "tfja_fisel_screening.csv", keep_default_na=False)
ganadores = pd.read_csv(analysis / "ganadores_constancia.csv", keep_default_na=False)
personas = pd.read_csv(analysis / "tepjf_personas_detectadas.csv", keep_default_na=False)
diputados = pd.read_csv(analysis / "diputados_lxvi_electos.csv", keep_default_na=False)


def image_data_uri(relative_path: str) -> str:
    path = ROOT / relative_path
    if not path.exists():
        return ""
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"

st.markdown(
    """
    <div class="newspaper-shell">
      <div class="masthead">
        <div class="kicker">Observatorio de Fiscalizacion y Justicia Electoral</div>
        <div class="headline">Diputaciones bajo lupa</div>
        <div class="deck">
          Corte editorial del corpus TEPJF 2023-2024, universo de 500 diputaciones LXVI,
          constancias de mayoria, fiscalizacion, propaganda y verificacion nominal
          documentada en registros publicos administrativos y electorales.
        </div>
      </div>
      <div class="folio-row">
        <span>Corte operativo</span><span>Formato carta horizontal</span><span>Fuentes oficiales</span><span>Revision nominal documentada</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

responsive_kpi_grid(
    [
        ("Sentencias", len(resumen)),
        ("Constancia", int(resumen["constancia_mayoria"].sum())),
        ("Fiscalizacion", int(resumen["fiscalizacion"].sum())),
        ("Rebase/tope", int(resumen["rebase_tope"].sum())),
        ("Propaganda", int(resumen["propaganda"].sum())),
        ("Nombres verificados", len(tfja)),
        ("Diputaciones LXVI", len(diputados)),
    ]
)

st.subheader("Ganadores confirmados con foto oficial")
ganadores_confirmados = ganadores[ganadores["clasificacion"].eq("ganador_confirmado")]
cards = ['<div class="portrait-grid">']
for _, row in ganadores_confirmados.iterrows():
    photo = image_data_uri(row["foto_png"])
    cards.append(
        '<div class="portrait-card">'
        f'<img src="{photo}" alt="{row["persona"]}">'
        "<div>"
        f'<div class="name">{row["persona"]}</div>'
        f'<div class="meta">{row["entidad"]} &middot; Distrito {row["distrito"]} &middot; {row["principio"]}</div>'
        f'<div class="meta">{row["coalicion_partido"]}</div>'
        f'<div class="status">{row["estado_verificacion"].replace("_", " ")}</div>'
        f'<div class="meta">{row["resultado_electoral"]}</div>'
        "</div>"
        "</div>"
    )
cards.append("</div>")
st.markdown("".join(cards), unsafe_allow_html=True)

st.caption(
    "Fotos extraidas en PNG desde fichas oficiales de la Camara de Diputados. "
    "La busqueda de sanciones se reporta como coincidencia localizada o no localizada, no como certificacion legal."
)

left, right = st.columns([1.2, .8])
with left:
    st.subheader("Mapa de temas del corpus jurisdiccional")
    topic_cols = ["constancia_mayoria", "fiscalizacion", "rebase_tope", "nulidad", "rp", "inelegibilidad", "propaganda"]
    topic_df = pd.DataFrame(
        {"tema": topic_cols, "sentencias": [int(resumen[col].sum()) for col in topic_cols]}
    ).sort_values("sentencias")
    fig = px.bar(topic_df, x="sentencias", y="tema", orientation="h")
    fig.update_traces(marker_color=["#1E5B4F" if t != "fiscalizacion" else "#6B1531" for t in topic_df["tema"]])
    fig.update_layout(showlegend=False, margin=dict(l=0, r=0, t=8, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, width="stretch")

with right:
    st.subheader("Control nominal")
    st.markdown(
        """
        <div class="verdict-ok">
          <strong>Sin coincidencia publica confirmada</strong><br>
          Las consultas nominales en el Registro federal de Servidores Publicos Sancionados
          devolvieron: "No se encontraron coincidencias" para los cuatro nombres prioritarios
          ya revisados manualmente.
        </div>
        <div class="rule"></div>
        <div class="verdict-warn">
          <strong>Alcance limitado</strong><br>
          No equivale a certificacion de inexistencia. TFJA sancionados tuvo problema DNS
          local; FISEL/FGR no mostro coincidencias nominales publicas en busqueda oficial.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.subheader("Composicion de diputaciones electas")
party = diputados.groupby("partido_estimado", as_index=False).size().rename(columns={"size": "diputaciones"}).sort_values("diputaciones")
fig = px.bar(party, x="diputaciones", y="partido_estimado", orientation="h", text="diputaciones")
fig.update_traces(marker_color=["#6B1531" if x == "MORENA" else "#1E5B4F" if x == "PVEM" else "#B88A2A" if x == "PT" else "#2B5C8A" if x == "PAN" else "#FF6600" if x == "MC" else "#8A1F2D" for x in party["partido_estimado"]], textposition="outside")
fig.update_layout(showlegend=False, margin=dict(l=0, r=24, t=8, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig, width="stretch")

st.subheader("Universo oficial de diputaciones")
st.dataframe(
    diputados[
        [
            "nombre_listado",
            "partido_estimado",
            "principio_estimado",
            "entidad",
            "distrito_circunscripcion",
            "perfil_url",
            "foto_png_bn",
        ]
    ],
    width="stretch",
    hide_index=True,
)

st.subheader("Personas verificadas")
st.dataframe(
    tfja[
        [
            "persona",
            "calidad_detectada",
            "resultado_administrativo",
            "resultado_delitos_electorales",
            "estado_verificacion",
        ]
    ],
    width="stretch",
    hide_index=True,
)

st.subheader("Menciones nominales detectadas en expedientes")
st.dataframe(
    personas[["expediente", "persona_detectada", "contexto"]],
    width="stretch",
    hide_index=True,
)

st.subheader("Ganadores y personas mencionadas curadas")
st.dataframe(
    ganadores[
        [
            "persona",
            "clasificacion",
            "expedientes_relacionados",
            "entidad",
            "distrito",
            "resultado_administrativo",
            "resultado_delitos_electorales",
            "estado_verificacion",
        ]
    ],
    width="stretch",
    hide_index=True,
)

st.subheader("Sentencias con constancia de mayoria")
st.dataframe(
    resumen[resumen["constancia_mayoria"].eq(1)][
        ["expediente", "year", "tema_inventario", "medio", "sentido_probable", "nulidad", "rebase_tope"]
    ],
    width="stretch",
    hide_index=True,
)
