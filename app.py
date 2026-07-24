from __future__ import annotations

import base64
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
from observatorio.ui import format_money, page_setup


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


def pdf_data_uri(path: str) -> str:
    payload = cached_pdf(path)
    if not payload:
        return "#"
    encoded = base64.b64encode(payload).decode("ascii")
    return f"data:application/pdf;base64,{encoded}"


def money_compact(value: float | int | str) -> str:
    try:
        amount = float(value)
    except (TypeError, ValueError):
        return "$0"
    if abs(amount) >= 1_000_000:
        return f"${amount / 1_000_000:.1f} M"
    if abs(amount) >= 1_000:
        return f"${amount / 1_000:.1f} K"
    return f"${amount:,.0f}"


def responsive_kpi_grid(items: list[tuple[str, str | int | float, str | None]], *, money_labels: set[str] | None = None) -> None:
    money_labels = money_labels or set()
    cards = ['<div class="responsive-kpi-grid">']
    for label, value, detail in items:
        value_class = "kpi-value money" if label in money_labels else "kpi-value"
        cards.append(
            '<div class="responsive-kpi">'
            f'<div class="kpi-label">{html.escape(str(label))}</div>'
            f'<div class="{value_class}">{html.escape(str(value))}</div>'
            f'<div class="kpi-detail">{html.escape(str(detail or ""))}</div>'
            "</div>"
        )
    cards.append("</div>")
    st.markdown("".join(cards), unsafe_allow_html=True)


def filter_controls() -> dict[str, list[str]]:
    with st.expander("Ajustar corte de datos", expanded=False):
        cols = st.columns(4)
        filters: dict[str, list[str]] = {}
        for idx, (label, column) in enumerate(
            [
                ("Nivel", "nivel"),
                ("Partido", "partido_principal"),
                ("Conducta", "conducta_principal"),
                ("Sentido", "sentido"),
            ]
        ):
            options = sorted([x for x in casos[column].unique() if str(x)]) if column in casos.columns else []
            filters[column] = cols[idx].multiselect(label, options, default=options)
    return filters


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

st.markdown(
    f"""
    <div class="download-dock" aria-label="Descargas del observatorio">
      <span>Descarga este análisis</span>
      <a class="pill primary" href="{pdf_data_uri(pdf_options["Qué se sancionó en las elecciones de diputaciones federales 2024"]["path"])}"
         download="{pdf_options["Qué se sancionó en las elecciones de diputaciones federales 2024"]["file_name"]}">Fiscalización</a>
      <a class="pill secondary" href="{pdf_data_uri(pdf_options["Criterios de fiscalización electoral derivados del proceso 2023-2024"]["path"])}"
         download="{pdf_options["Criterios de fiscalización electoral derivados del proceso 2023-2024"]["file_name"]}">Criterios</a>
    </div>
    """,
    unsafe_allow_html=True,
)

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
    <section class="home-section reading-section">
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
      <div class="reading-rail">
        <div><b>01</b><span>Lee la síntesis editorial y descarga el PDF que corresponda.</span></div>
        <div><b>02</b><span>Ajusta el corte de datos sin salir de la página.</span></div>
        <div><b>03</b><span>Contrasta partido, sentido de resolución y tabla de expedientes.</span></div>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="home-doc-grid">
      <div class="home-doc-card">
        <b>Análisis de diputaciones y criterios</b>
        <span>Descarga los PDF desde el selector superior y consulta el panel de datos en esta misma página.</span>
        <a href="#descargas">Ir a descargas</a>
      </div>
      <div class="home-doc-card">
        <b>Corpus de sentencias TEPJF</b>
        <span>El corte de sentencias y los hallazgos se sintetizan en los PDF editoriales y en las gráficas de datos.</span>
        <a href="#panel-datos">Ir al panel</a>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <span class="home-panel-anchor" id="panel-datos"></span>
    <section class="data-editorial-head">
      <div>
        <div class="label">Panel de datos</div>
        <div class="title">Corte 2023-2024</div>
      </div>
      <p>
        Corte operativo federal para reconstruir acto de origen, impugnación, agravios,
        sentido, efectos y diputaciones electas. Las cifras se presentan con lectura
        ejecutiva y monto exacto documentado.
      </p>
    </section>
    """,
    unsafe_allow_html=True,
)

filters = filter_controls()
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
responsive_kpi_grid(
    [
        ("Casos", stats["casos"], "Expedientes base"),
        ("Sujetos", stats["sujetos"], "Partidos o coaliciones"),
        ("Sanciones", stats["sanciones"], "Registros INE"),
        ("Monto original", money_compact(stats["monto_original"]), format_money(stats["monto_original"])),
        ("Monto final conocido", money_compact(stats["monto_final"]), format_money(stats["monto_final"])),
        ("Agravios", stats["agravios"], "Conceptos clasificados"),
    ],
    money_labels={"Monto original", "Monto final conocido"},
)

st.markdown('<div class="chart-kicker">Lectura por sujeto obligado</div>', unsafe_allow_html=True)
st.subheader("Casos por partido")
chart_df = count_by(casos_filtrados, "partido_principal")
if not chart_df.empty:
    fig = px.bar(chart_df, x="casos", y="partido_principal", orientation="h", color_discrete_sequence=["#6B1531"])
    fig.update_layout(
        height=max(360, 54 * len(chart_df) + 120),
        margin=dict(l=160, r=36, t=12, b=44),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        font=dict(family="Montserrat", size=13),
        xaxis=dict(automargin=True),
        yaxis=dict(automargin=True),
    )
    fig.update_traces(cliponaxis=False)
    st.plotly_chart(fig, width="stretch")
else:
    st.info("Sin datos para los filtros seleccionados.")

st.markdown('<div class="chart-kicker">Resultado jurisdiccional</div>', unsafe_allow_html=True)
st.subheader("Sentido de resolucion")
chart_df = count_by(casos_filtrados, "sentido")
if not chart_df.empty:
    fig = px.bar(chart_df, x="casos", y="sentido", orientation="h", color_discrete_sequence=["#1E5B4F"])
    fig.update_layout(
        height=max(320, 54 * len(chart_df) + 120),
        margin=dict(l=160, r=36, t=12, b=44),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        font=dict(family="Montserrat", size=13),
        xaxis=dict(automargin=True),
        yaxis=dict(automargin=True),
    )
    fig.update_traces(cliponaxis=False)
    st.plotly_chart(fig, width="stretch")
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
st.dataframe(casos_filtrados[[c for c in visible_cols if c in casos_filtrados.columns]], width="stretch", hide_index=True)
st.download_button("Descargar CSV filtrado", casos_filtrados.to_csv(index=False).encode("utf-8"), "casos_filtrados.csv", "text/csv")

st.subheader("Lectura ejecutiva")
st.write(
    "El observatorio se concentra en diputaciones federales 2024: distingue sentencias de fondo, revocaciones para efectos, "
    "sobreseimientos y asuntos de queja en materia de fiscalizacion sin presentar el corpus como universo exhaustivo."
)
