from __future__ import annotations

import base64
import html
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import pandas as pd
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

TEPJF_URLS = {
    "SUP-RAP-342/2024": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-RAP-0342-2024-",
    "SUP-RAP-352/2024": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-RAP-0352-2024-",
    "SUP-RAP-357/2024": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-RAP-0357-2024-",
    "SUP-RAP-413/2024": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-RAP-0413-2024-",
    "SUP-REC-764/2024": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-REC-0764-2024-",
    "SCM-RAP-47/2024": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SCM-RAP-0047-2024-",
    "SCM-JIN-27/2024": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SCM-JIN-0027-2024-",
    "SCM-JIN-30/2024": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SCM-JIN-0030-2024-",
}

CRITERIA = [
    {
        "id": "FIS-01",
        "title": "Exhaustividad del dictamen, anexos y conclusiones",
        "organ": "Sala Superior / Sala Regional Ciudad de México",
        "source": "SUP-RAP-342/2024; SCM-RAP-47/2024",
        "theme": "Dictamen y resolución",
        "rule": "La autoridad debe permitir reconstruir la relación entre hallazgo, anexo, conclusión y sanción.",
        "effect": "Revocación para efectos, revocación parcial o confirmación.",
        "relevance": "La lectura del dictamen no se reduce al monto: exige identificar conclusión, soporte y respuesta administrativa.",
        "utility": "Antes: diseñar matrices de observaciones. Durante: ubicar anexo y conclusión. Después: documentar qué quedó firme y qué debe rehacerse.",
    },
    {
        "id": "FIS-02",
        "title": "Fallas del Sistema Integral de Fiscalización",
        "organ": "Sala Superior",
        "source": "SUP-RAP-342/2024; SUP-RAP-357/2024; SUP-RAP-413/2024",
        "theme": "SIF",
        "rule": "La referencia genérica a fallas del SIF no desvirtúa una infracción si no se acredita cómo impidió cumplir una obligación concreta.",
        "effect": "Confirmación cuando el agravio es genérico; posible revocación parcial si incide en una conclusión específica.",
        "relevance": "Distingue problemas técnicos documentados de defensas abstractas frente a registros extemporáneos u omisiones.",
        "utility": "Antes: preparar bitácoras técnicas. Durante: conservar evidencia de carga, módulo y operación. Después: vincular la falla con una conclusión concreta.",
    },
    {
        "id": "FIS-03",
        "title": "Documentación soporte y comprobación fiscal",
        "organ": "Sala Superior",
        "source": "SUP-RAP-352/2024; SUP-RAP-357/2024",
        "theme": "Comprobación de gasto",
        "rule": "La falta de soporte fiscal, contractual o contable idóneo puede sostener sanciones si el sujeto obligado no desvirtúa la observación.",
        "effect": "Confirmación de conclusiones o sanciones cuando no se acredita el soporte.",
        "relevance": "Da un estándar práctico para revisar facturas, contratos, muestras y correspondencia entre operación, proveedor y campaña.",
        "utility": "Antes: definir expedientes digitales mínimos. Durante: revisar soporte por operación. Después: depurar registros firmes y pendientes.",
    },
    {
        "id": "FIS-04",
        "title": "Omisión de reportar propaganda, eventos o gastos",
        "organ": "Sala Superior / Sala Regional Ciudad de México",
        "source": "SUP-RAP-342/2024; SUP-RAP-357/2024; SUP-RAP-413/2024; SCM-RAP-47/2024",
        "theme": "Gasto no reportado",
        "rule": "La omisión se analiza por existencia del gasto o propaganda, beneficio electoral, obligación de reporte y suficiencia del soporte.",
        "effect": "Confirmación, revocación para efectos o revocación parcial.",
        "relevance": "Ordena observaciones de propaganda, eventos y gastos que no aparecen en la contabilidad ordinaria.",
        "utility": "Antes: crear catálogos de conducta. Durante: vincular evidencia con evento o pieza. Después: separar omisiones firmes de estudios rehechos.",
    },
    {
        "id": "FIS-05",
        "title": "Fiscalización y nulidad de elección",
        "organ": "Sala Superior / Sala Regional Ciudad de México",
        "source": "SCM-JIN-27/2024; SUP-REC-764/2024; SUP-RAP-352/2024; SUP-RAP-413/2024",
        "theme": "Rebase de tope y determinancia",
        "rule": "La sanción administrativa aislada no equivale por sí misma a nulidad; se requiere monto, acumulación al tope, determinancia y vínculo con la elección.",
        "effect": "Confirmación de validez o análisis de nulidad sólo si se acredita el impacto exigido.",
        "relevance": "Separa la lectura administrativa de fiscalización de la consecuencia jurisdiccional sobre validez de la elección.",
        "utility": "Antes: ubicar topes y umbrales. Durante: monitorear acumulación de gastos. Después: distinguir sanción, rebase y nulidad.",
    },
    {
        "id": "FIS-06",
        "title": "Efectos de revocación",
        "organ": "Sala Superior / Sala Regional Ciudad de México",
        "source": "SUP-RAP-342/2024; SUP-RAP-357/2024; SUP-RAP-413/2024; SCM-RAP-47/2024",
        "theme": "Efectos",
        "rule": "El sentido de una sentencia puede confirmar una parte, revocar otra o exigir un nuevo pronunciamiento de la autoridad.",
        "effect": "Confirmación parcial, revocación para efectos, recálculo o nueva resolución.",
        "relevance": "Permite que dictamen, resolución y sentencia queden en una misma cadena editorial sin lenguaje innecesariamente técnico.",
        "utility": "Antes: prever salidas posibles. Durante: capturar puntos resolutivos. Después: dar seguimiento a recálculos, reposiciones y montos firmes.",
    },
]


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


def text_label(value: str) -> str:
    replacements = {
        "documentacion soporte faltante": "documentación soporte faltante",
        "omision de presentar XML": "omisión de presentar XML",
        "omision de reportar gastos": "omisión de reportar gastos",
        "omision de reportar inserciones en medios impresos": "omisión de reportar inserciones en medios impresos",
        "omision de reportar propaganda en internet": "omisión de reportar propaganda en internet",
        "propaganda internet federal no reportada": "propaganda en internet federal no reportada",
        "rebase pago efectivo representantes de casilla": "rebase por pago en efectivo a representantes de casilla",
        "registro extemporaneo": "registro extemporáneo",
        "comprobantes fiscales XML faltantes": "comprobantes fiscales XML faltantes",
        "factura con complemento INE faltante": "factura con complemento INE faltante",
    }
    return replacements.get(str(value), str(value))


def top_conducts_html() -> str:
    data = sanciones.copy()
    if data.empty or "monto_original" not in data.columns:
        return ""
    data["monto_original"] = pd.to_numeric(data["monto_original"], errors="coerce").fillna(0)
    grouped = (
        data[data["monto_original"].gt(0)]
        .groupby("conducta", as_index=False)
        .agg(monto=("monto_original", "sum"), registros=("sancion_id", "count"))
        .sort_values("monto", ascending=False)
        .head(6)
    )
    return "".join(
        '<div class="analysis-row">'
        f'<span>{html.escape(text_label(row["conducta"]))}</span>'
        f'<b>{html.escape(money_compact(row["monto"]))}</b>'
        f'<em>{int(row["registros"])} registro{"s" if int(row["registros"]) != 1 else ""}</em>'
        "</div>"
        for _, row in grouped.iterrows()
    )


def criterion_source_links(source: str) -> str:
    links = []
    for expediente in [part.strip() for part in source.split(";")]:
        url = TEPJF_URLS.get(expediente)
        if url:
            links.append(f'<a href="{html.escape(url)}" target="_blank" rel="noopener">{html.escape(expediente)}</a>')
        else:
            links.append(f'<span>{html.escape(expediente)}</span>')
    return "".join(links)


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
        <a href="#analisis-en-pagina">Análisis</a>
        <a href="#criterios-en-pagina">Criterios</a>
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
          <a href="#analisis-en-pagina">Leer análisis</a>
        </div>
        <div class="home-doc-card">
          <b>Criterios de fiscalización electoral derivados del proceso 2023-2024</b>
          <span>Fichas jurídicas por órgano, expediente, tema, regla, efecto, relevancia y utilidad temporal.</span>
          <a href="#criterios-en-pagina">Explorar criterios</a>
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
        <span>Lee la síntesis dentro de la app, abre criterios y descarga el PDF si necesitas la pieza cerrada.</span>
        <a href="#analisis-en-pagina">Leer en página</a>
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
    f"""
    <section class="analysis-reader" id="analisis-en-pagina">
      <div class="analysis-head">
        <div>
          <div class="label">Análisis en página</div>
          <div class="title">Qué se sancionó</div>
        </div>
        <p>
          El corte reconstruye la cadena entre dictamen del INE, resolución administrativa,
          impugnación y sentencia. No se limita a descargar el PDF: aquí se puede leer la
          síntesis, ubicar las conductas y abrir criterios sin salir de la app.
        </p>
      </div>
      <div class="analysis-grid">
        <article class="analysis-card lead">
          <b>Hallazgo central</b>
          <p>
            En los expedientes revisados, la discusión se concentró en omisiones de reporte,
            soporte documental, comprobantes XML, propaganda en internet y pagos a representantes.
            La justicia electoral no sustituyó la fiscalización: revisó si el INE motivó,
            individualizó y sostuvo cada conclusión.
          </p>
        </article>
        <article class="analysis-card">
          <b>Monto administrativo</b>
          <p>
            El monto original observado asciende a {money_compact(base_stats["monto_original"])}
            y el monto final conocido en este corte es {money_compact(base_stats["monto_final"])}.
            La diferencia importa porque algunas conclusiones quedaron firmes, otras se confirmaron
            parcialmente y otras fueron devueltas para nuevo estudio.
          </p>
        </article>
        <article class="analysis-card">
          <b>Lectura jurisdiccional</b>
          <p>
            Las sentencias distinguen confirmar una sanción, revocar para efectos, modificar una
            conclusión o declarar inoperante un agravio. Esa distinción evita leer toda observación
            como sanción firme o como nulidad automática.
          </p>
        </article>
      </div>
      <div class="analysis-split">
        <div>
          <div class="chart-kicker">Conductas con mayor monto observado</div>
          <div class="analysis-list">{top_conducts_html()}</div>
        </div>
        <div class="analysis-note">
          <b>Cómo leer esta sección</b>
          <span>
            Primero identifica la conducta; después revisa si el monto fue controvertido,
            confirmado, modificado o pendiente. Finalmente conecta la regla jurisdiccional con
            su utilidad antes, durante y después del proceso electoral.
          </span>
        </div>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="criteria-reader" id="criterios-en-pagina">
      <div class="reader-head">
        <div>
          <div class="label">Criterios emitidos</div>
          <div class="title">Fichas navegables</div>
        </div>
        <div class="body">
          Compilación operativa de criterios derivados de Sala Superior y Sala Regional Ciudad
          de México. Cada ficha conserva órgano, expediente, tema, regla, efecto, relevancia
          para dictamen/resolución y utilidad temporal.
        </div>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

criteria_nav = "".join(
    f'<a href="#{item["id"].lower()}"><b>{html.escape(item["id"])}</b><span>{html.escape(item["theme"])}</span></a>'
    for item in CRITERIA
)
st.markdown(f'<div class="criteria-map">{criteria_nav}</div>', unsafe_allow_html=True)

for item in CRITERIA:
    st.markdown(f'<span id="{html.escape(item["id"].lower())}"></span>', unsafe_allow_html=True)
    with st.expander(f'{item["id"]} · {item["title"]}', expanded=item["id"] == "FIS-01"):
        st.markdown(
            f"""
            <div class="criterion-body streamlit-criterion">
              <div class="criterion-field rule"><label>Regla o criterio</label><p>{html.escape(item["rule"])}</p></div>
              <div class="criterion-field"><label>Órgano</label><p>{html.escape(item["organ"])}</p></div>
              <div class="criterion-field"><label>Expediente</label><div class="source-links">{criterion_source_links(item["source"])}</div></div>
              <div class="criterion-field"><label>Tema</label><p>{html.escape(item["theme"])}</p></div>
              <div class="criterion-field"><label>Efecto</label><p>{html.escape(item["effect"])}</p></div>
              <div class="criterion-field"><label>Relevancia para dictamen/resolución</label><p>{html.escape(item["relevance"])}</p></div>
              <div class="criterion-field utility"><label>Utilidad antes, durante y después</label><p>{html.escape(item["utility"])}</p></div>
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
