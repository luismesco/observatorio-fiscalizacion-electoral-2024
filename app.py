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
from observatorio.ui import add_global_filters, format_money, page_setup


page_setup("Observatorio de Fiscalización")
data = load_all()
casos = data["casos"]
sanciones = data["sanciones"]
agravios = data["agravios"]
base_stats = kpis(casos, sanciones, agravios)


@st.cache_data(show_spinner=False)
def cached_pdf(path: str) -> bytes:
    pdf_path = ROOT / path
    if not pdf_path.exists():
        return b""
    return pdf_path.read_bytes()


st.markdown(
    """
    <nav class="site-nav home-nav">
      <div class="site-brand">Observatorio Electoral</div>
      <div class="site-links">
        <a class="active" href="#inicio">Inicio</a>
        <a href="#descargas">Descargas</a>
        <a href="#publicaciones">Publicaciones</a>
        <a href="#interactivo">Interactivo</a>
        <a href="#panel-datos">Datos</a>
      </div>
    </nav>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <span class="home-panel-anchor" id="inicio"></span>
    <section class="home-hero">
      <div>
        <div class="home-kicker">Observatorio de Fiscalización Electoral</div>
        <div class="home-title"><span>Diputaciones</span><span>federales</span><span>2024</span></div>
      </div>
      <div>
        <div class="home-deck">
          Una experiencia editorial e interactiva para consultar qué se sancionó en la elección
          de diputaciones federales y qué criterios emitieron Sala Superior y Sala Regional Ciudad
          de México en materia de fiscalización electoral del proceso 2023-2024.
        </div>
        <div class="home-folio">
          <div><b>{base_stats["casos"]}</b><span>Expedientes base</span></div>
          <div><b>{base_stats["sanciones"]}</b><span>Registros de sanción</span></div>
          <div><b>{base_stats["agravios"]}</b><span>Agravios clasificados</span></div>
        </div>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <span class="home-panel-anchor" id="descargas"></span>
    <section class="home-download-band">
      <div class="home-section-head">
        <div>
          <div class="label">Descargas editoriales</div>
          <div class="title">Elige el análisis</div>
        </div>
        <div class="body">
          Los PDF finales están integrados en la app para descarga directa. El selector cambia el archivo
          disponible sin sacar al lector del flujo de lectura.
        </div>
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
    <span class="home-panel-anchor" id="publicaciones"></span>
    <section class="home-section">
      <div class="home-section-head">
        <div>
          <div class="label">Publicaciones principales</div>
          <div class="title">Dos puertas de lectura</div>
        </div>
        <div class="body">
          La app combina piezas editoriales cerradas en PDF con una lectura navegable por datos,
          criterios, expedientes y entidades. Primero lee, después explora.
        </div>
      </div>
      <div class="home-doc-grid">
        <div class="home-doc-card">
          <b>Qué se sancionó en las elecciones de diputaciones federales 2024</b>
          <span>Lectura ejecutiva de conductas, montos observados, expedientes, sujetos obligados y efectos de las resoluciones.</span>
          <a href="#descargas">Seleccionar PDF</a>
        </div>
        <div class="home-doc-card">
          <b>Criterios de fiscalización electoral derivados del proceso 2023-2024</b>
          <span>Fichas jurídicas por órgano, expediente, tema, regla, efecto, relevancia y utilidad temporal.</span>
          <a href="#interactivo">Explorar criterios</a>
        </div>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <span class="home-panel-anchor" id="interactivo"></span>
    <section class="home-section">
      <div class="home-section-head">
        <div>
          <div class="label">Lectura interactiva</div>
          <div class="title">Navega sin perder contexto</div>
        </div>
        <div class="body">
          La sección de diputaciones concentra la retícula completa: descargas, criterios plegables,
          mapa territorial, expedientes consultables y registro de curules.
        </div>
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

st.markdown('<span class="home-panel-anchor" id="panel-datos"></span>', unsafe_allow_html=True)
st.title("Panel de datos del corte 2023-2024")
st.caption("Corte operativo federal para reconstruir acto de origen, impugnación, agravios, sentido, efectos y diputaciones electas.")

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
