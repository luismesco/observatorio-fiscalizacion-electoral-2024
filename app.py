from __future__ import annotations

import html
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import plotly.express as px
import streamlit as st

from observatorio.data_loader import filtered_cases, load_all
from observatorio.metrics import count_by, kpis
from observatorio.ui import add_global_filters, format_money, mvp_notice, page_setup


page_setup("Observatorio de Fiscalización")
data = load_all()
casos = data["casos"]
sanciones = data["sanciones"]
agravios = data["agravios"]


@st.cache_data(show_spinner=False)
def cached_pdf(path: str) -> bytes:
    pdf_path = ROOT / path
    if not pdf_path.exists():
        return b""
    return pdf_path.read_bytes()


st.markdown(
    """
    <nav class="site-nav">
      <div class="site-brand">Observatorio Electoral</div>
      <div class="site-links">
        <a class="active" href="/">Inicio</a>
        <a href="/Diputaciones_electas">Diputaciones</a>
        <a href="/Infografia_editorial">Infografía</a>
        <a href="/Analisis_corpus_TEPJF">Sentencias</a>
      </div>
    </nav>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="intro-lede">
      <div>
        <div class="intro-kicker">Observatorio de Fiscalización Electoral</div>
        <div class="intro-title"><span>Diputaciones</span><span>federales</span><span>2024</span></div>
      </div>
      <div class="intro-copy">
        Hub editorial para consultar qué se sancionó en la elección de diputaciones federales
        y qué criterios emitieron Sala Superior y Sala Regional Ciudad de México en materia de
        fiscalización electoral del proceso federal 2023-2024.
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

pdf_options = {
    "Qué se sancionó en las elecciones de diputaciones federales 2024": {
        "path": "exports/diputaciones_electas_reporte.pdf",
        "file_name": "que_se_sanciono_diputaciones_federales_2024.pdf",
        "note": "PDF editorial con sanciones, expedientes, montos, efectos y lectura territorial.",
    },
    "Criterios de fiscalización electoral derivados del proceso 2023-2024": {
        "path": "exports/criterios_fiscalizacion_diputaciones_2024.pdf",
        "file_name": "criterios_fiscalizacion_diputaciones_2024.pdf",
        "note": "PDF de criterios de Sala Superior y Sala Regional Ciudad de México, enfocado en diputaciones federales.",
    },
}
download_left, download_right = st.columns([.72, .28])
selected_pdf = download_left.selectbox(
    "Análisis disponible",
    list(pdf_options),
    key="home_pdf_analysis_download",
)
selected_payload = pdf_options[selected_pdf]
selected_bytes = cached_pdf(selected_payload["path"])
download_left.markdown(
    f'<div class="download-note">{html.escape(selected_payload["note"])}</div>',
    unsafe_allow_html=True,
)
download_right.download_button(
    "Descarga este análisis",
    data=selected_bytes,
    file_name=selected_payload["file_name"],
    mime="application/pdf",
    disabled=not selected_bytes,
)

st.markdown(
    """
    <section class="plain-steps">
      <div>
        <strong>1. Qué se sancionó</strong>
        <span>Lectura ejecutiva de conductas, montos observados, expedientes y efectos de las resoluciones.</span>
      </div>
      <div>
        <strong>2. Criterios emitidos</strong>
        <span>Fichas jurídicas navegables por tema, órgano y utilidad antes, durante y después del proceso electoral.</span>
      </div>
      <div>
        <strong>3. Consulta interactiva</strong>
        <span>Explora diputaciones electas, sentencias, corpus documental, verificación y hallazgos desde las secciones de la app.</span>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

nav_left, nav_right = st.columns([1, 1])
with nav_left:
    st.page_link("pages/13_Diputaciones_electas.py", label="Abrir análisis de diputaciones y criterios", icon=":material/article:")
with nav_right:
    st.page_link("pages/10_Analisis_corpus_TEPJF.py", label="Abrir corpus de sentencias TEPJF", icon=":material/travel_explore:")

st.title("Panel de datos del corte 2023-2024")
st.caption("Corte operativo federal para reconstruir acto de origen, impugnación, agravios, sentido, efectos y diputaciones electas.")
mvp_notice()

filters = add_global_filters(casos)
casos_filtrados = filtered_cases(
    casos,
    nivel=filters["nivel"],
    partido=filters["partido_principal"],
    conducta=filters["conducta_principal"],
    sentido=filters["sentido"],
)
ids = set(casos_filtrados["caso_id"].astype(str)) if not casos_filtrados.empty else set()
sanciones_filtradas = sanciones[sanciones["caso_id"].astype(str).isin(ids)] if ids and not sanciones.empty else sanciones.head(0)
agravios_filtrados = agravios[agravios["caso_id"].astype(str).isin(ids)] if ids and not agravios.empty else agravios.head(0)

stats = kpis(casos_filtrados, sanciones_filtradas, agravios_filtrados)
cols = st.columns(6)
cols[0].metric("Casos", stats["casos"])
cols[1].metric("Sujetos", stats["sujetos"])
cols[2].metric("Sanciones", stats["sanciones"])
cols[3].metric("Monto original", format_money(stats["monto_original"]))
cols[4].metric("Monto final conocido", format_money(stats["monto_final"]))
cols[5].metric("Agravios", stats["agravios"])

left, right = st.columns([1, 1])
with left:
    st.subheader("Casos por partido")
    chart_df = count_by(casos_filtrados, "partido_principal")
    if not chart_df.empty:
        st.plotly_chart(px.bar(chart_df, x="casos", y="partido_principal", orientation="h", color_discrete_sequence=["#6B1531"]), use_container_width=True)
    else:
        st.info("Sin datos para los filtros seleccionados.")

with right:
    st.subheader("Sentido de resolucion")
    chart_df = count_by(casos_filtrados, "sentido")
    if not chart_df.empty:
        st.plotly_chart(px.bar(chart_df, x="casos", y="sentido", orientation="h", color_discrete_sequence=["#1E5B4F"]), use_container_width=True)
    else:
        st.info("Sin datos para los filtros seleccionados.")

st.subheader("Tabla de expedientes")
visible_cols = [
    "nivel",
    "expediente",
    "organo_resolutor",
    "partido_principal",
    "conducta_principal",
    "sentido",
    "efectos_resumen",
    "revision_humana",
]
st.dataframe(casos_filtrados[[c for c in visible_cols if c in casos_filtrados.columns]], use_container_width=True, hide_index=True)
st.download_button("Descargar CSV filtrado", casos_filtrados.to_csv(index=False).encode("utf-8"), "casos_filtrados.csv", "text/csv")

st.subheader("Lectura ejecutiva")
st.write(
    "El observatorio se concentra en diputaciones federales 2024: distingue sentencias de fondo, revocaciones para efectos, "
    "sobreseimientos y asuntos de queja en materia de fiscalizacion sin presentar el corpus como universo exhaustivo."
)
