from __future__ import annotations

import base64
import html
import re
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from observatorio.pdf_export import diputaciones_map_svg, get_diputaciones_report_pdf_bytes
from observatorio.ui import page_setup


page_setup("Diputaciones electas")

st.markdown(
    """
    <nav class="site-nav">
      <div class="site-brand">Observatorio Electoral</div>
      <div class="site-links">
        <a class="active" href="/Diputaciones_electas">Diputaciones</a>
        <a href="/Infografia_editorial">Infografía</a>
        <a href="/Analisis_corpus_TEPJF">Sentencias</a>
        <a href="/TFJA_FISEL_verificacion">Verificación</a>
      </div>
    </nav>
    """,
    unsafe_allow_html=True,
)

analysis = ROOT / "data" / "analysis"
processed = ROOT / "data" / "processed"
df = pd.read_csv(analysis / "diputados_lxvi_electos.csv", keep_default_na=False)
resumen = pd.read_csv(analysis / "tepjf_corpus_resumen.csv", keep_default_na=False)
sanciones = pd.read_csv(processed / "sanciones.csv", keep_default_na=False)
casos = pd.read_csv(processed / "casos.csv", keep_default_na=False)
hallazgos = pd.read_csv(processed / "hallazgos_portal.csv", keep_default_na=False)


@st.cache_data(show_spinner=False)
def cached_pdf_report() -> bytes:
    return get_diputaciones_report_pdf_bytes()

party_all = df.groupby("partido_estimado", as_index=False).size().rename(columns={"size": "diputaciones"})
party_counts = dict(zip(party_all["partido_estimado"], party_all["diputaciones"]))
bloque_morena = sum(party_counts.get(x, 0) for x in ["MORENA", "PVEM", "PT"])
bloque_pan_pri = sum(party_counts.get(x, 0) for x in ["PAN", "PRI"])
mc_total = party_counts.get("MC", 0)


def money(value: float) -> str:
    if value >= 1_000_000:
        return f"${value / 1_000_000:.1f} M"
    return f"${value:,.0f}"


def money_exact(value: float) -> str:
    return f"${value:,.2f}"


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
    }
    return replacements.get(value, value)


def display_text(value: str) -> str:
    replacements = {
        "Accion": "Acción",
        "Coalicion": "Coalición",
        "Revolucion": "Revolución",
        "campana": "campaña",
        "diputacion": "diputación",
        "resolucion": "resolución",
        "Revoca": "Revoca",
    }
    text = value
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def state_display(value: str) -> str:
    replacements = {
        "Ciudad de Mexico": "Ciudad de México",
        "Michoacan": "Michoacán",
        "Representacion proporcional": "Representación proporcional",
    }
    return replacements.get(value, value)


def plural(count: int, singular: str, plural_value: str | None = None) -> str:
    return singular if count == 1 else (plural_value or f"{singular}s")


def case_conduct_summary(row: pd.Series, sanctions: pd.DataFrame) -> str:
    case_sanctions = sanctions[sanctions["caso_id"].eq(row["caso_id"])].copy()
    subjects = sorted({display_text(text_label(value)) for value in case_sanctions["sujeto_nombre"].astype(str) if value})
    conductas = sorted({display_text(text_label(value)) for value in case_sanctions["conducta"].astype(str) if value})
    subject_text = "; ".join(subjects[:3]) or display_text(text_label(row["partido_principal"]))
    if len(subjects) > 3:
        subject_text += f"; y {len(subjects) - 3} más"
    conduct_text = "; ".join(conductas[:4]) or display_text(text_label(row["conducta_principal"]))
    if len(conductas) > 4:
        conduct_text += f"; y {len(conductas) - 4} más"
    candidate = str(row.get("persona_candidata", "")).strip()
    candidate_text = f", con referencia a la candidatura de {display_text(text_label(candidate))}" if candidate and candidate.lower() != "nan" else ""
    return (
        f"El expediente revisa conductas atribuidas a {subject_text}, identificado en el registro como "
        f"{display_text(text_label(row['partido_principal']))}{candidate_text}. La controversia se concentró en "
        f"{conduct_text}. El TEPJF resolvió en sentido de {display_text(text_label(row['sentido']))} y estableció como "
        f"efecto principal: {display_text(text_label(row['efectos_resumen']))}."
    )


def incidence_detail_summary(row: pd.Series) -> str:
    return (
        f"La sentencia de {row['fecha']} vincula a {display_text(text_label(row['candidatura']))}, de "
        f"{display_text(text_label(row['partido_o_coalicion']))}, con {display_text(text_label(row['tema']))}. "
        f"El asunto se tramitó por vía {row['tipo_medio']} ante {row['organo']} y se incorporó al corte "
        f"por su relación con {display_text(text_label(row['razon_prioridad'])).lower()}."
    )


REPORT_CUT_LABEL = "Corte documental al 23 de julio de 2026"
MAP_ENTITY_COLUMNS = [
    ("Chihuahua", "Chihuahua"),
    ("Ciudad de Mexico", "Ciudad de México"),
    ("Michoacan", "Michoacán"),
]
ENTITY_ORDER = {
    "Chihuahua": 0,
    "Ciudad de Mexico": 1,
    "Ciudad de México": 1,
    "Michoacan": 2,
    "Michoacán": 2,
    "Representacion proporcional": 3,
    "Representación proporcional": 3,
    "Sin entidad estatal": 3,
    "Nacional": 4,
}
CASE_LOCATION_OVERRIDES = {
    "REAL-FED-005": ("Ciudad de Mexico", "Distrito 7"),
    "REAL-FED-006": ("Michoacan", "Distrito 10 Morelia"),
    "REAL-FED-007": ("Michoacan", "Distrito 06"),
}


def exp_key(value: str) -> str:
    text = str(value).upper().replace("/", "-")
    text = text.replace(" Y ACUMULADO", "").replace(" Y ACUMULADOS", "")
    match = re.search(r"([A-Z]+-[A-Z]+-\d{1,4}-\d{4}(?:-ACUERDO\d+)?)", text)
    if not match:
        return text.strip()
    parts = match.group(1).split("-")
    if len(parts) >= 4 and parts[2].isdigit():
        parts[2] = str(int(parts[2]))
    return "-".join(parts)


def case_location(row: pd.Series, hallazgo_lookup: dict[str, tuple[str, str]]) -> tuple[str, str]:
    if row["caso_id"] in CASE_LOCATION_OVERRIDES:
        return CASE_LOCATION_OVERRIDES[row["caso_id"]]
    return hallazgo_lookup.get(exp_key(row["expediente"]), ("Sin entidad estatal", "Alcance nacional"))


def display_entity_and_scope(entidad: str, distrito: str) -> tuple[str, str]:
    if entidad in {"Representacion proporcional", "Representación proporcional"}:
        return "Sin entidad estatal", f"Representación proporcional · {display_text(text_label(distrito))}"
    if entidad == "Nacional":
        return "Sin entidad estatal", "Alcance nacional"
    return f"Mapa: {state_display(entidad)}", display_text(text_label(distrito))


sanciones["monto_original"] = pd.to_numeric(sanciones["monto_original"], errors="coerce").fillna(0)
sanciones["monto_final"] = pd.to_numeric(sanciones["monto_final"], errors="coerce").fillna(0)
sanciones_cuantificadas = sanciones[sanciones["monto_original"].gt(0)].copy()
registros_cuantificados = len(sanciones_cuantificadas)
registros_no_cuantificados = len(sanciones) - registros_cuantificados
total_sancionado = float(sanciones_cuantificadas["monto_original"].sum())
total_firme = float(sanciones.loc[sanciones["monto_final_estado"].eq("firme"), "monto_final"].sum())
causas = (
    sanciones_cuantificadas.groupby("conducta", as_index=False)
    .agg(monto=("monto_original", "sum"), registros=("sancion_id", "count"))
    .sort_values("monto", ascending=False)
)
top_causas = causas.head(5)
sanciones_por_caso = sanciones.groupby("caso_id", as_index=False).agg(
    monto_observado=("monto_original", "sum"),
    sanciones=("sancion_id", "count"),
)
casos_vinculados = casos.merge(sanciones_por_caso, on="caso_id", how="left")
casos_vinculados["monto_observado"] = casos_vinculados["monto_observado"].fillna(0)

state_points = {
    "Aguascalientes": (21.88, -102.30),
    "Baja California": (30.84, -115.28),
    "Baja California Sur": (25.84, -111.97),
    "Campeche": (19.83, -90.53),
    "Chiapas": (16.75, -93.12),
    "Chihuahua": (28.63, -106.07),
    "Ciudad de Mexico": (19.43, -99.13),
    "Ciudad de México": (19.43, -99.13),
    "Coahuila": (27.06, -101.71),
    "Colima": (19.24, -103.72),
    "Durango": (24.03, -104.67),
    "Guanajuato": (21.02, -101.26),
    "Guerrero": (17.55, -99.50),
    "Hidalgo": (20.09, -98.76),
    "Jalisco": (20.67, -103.35),
    "Mexico": (19.35, -99.63),
    "México": (19.35, -99.63),
    "Michoacan": (19.70, -101.19),
    "Michoacán": (19.70, -101.19),
    "Morelos": (18.92, -99.23),
    "Nayarit": (21.75, -104.89),
    "Nuevo Leon": (25.69, -100.32),
    "Nuevo León": (25.69, -100.32),
    "Oaxaca": (17.07, -96.72),
    "Puebla": (19.04, -98.20),
    "Queretaro": (20.59, -100.39),
    "Querétaro": (20.59, -100.39),
    "Quintana Roo": (19.18, -88.48),
    "San Luis Potosi": (22.15, -100.98),
    "San Luis Potosí": (22.15, -100.98),
    "Sinaloa": (24.80, -107.39),
    "Sonora": (29.07, -110.96),
    "Tabasco": (17.99, -92.93),
    "Tamaulipas": (23.74, -99.14),
    "Tlaxcala": (19.31, -98.24),
    "Veracruz": (19.17, -96.13),
    "Yucatan": (20.97, -89.62),
    "Yucatán": (20.97, -89.62),
    "Zacatecas": (22.77, -102.58),
}

st.markdown(
    """
    <section class="intro-lede">
      <div>
        <div class="intro-kicker">Observatorio de Fiscalización Electoral</div>
        <div class="intro-title"><span>Qué se</span><span>sancionó</span><span>en la elección</span></div>
      </div>
      <div class="intro-copy">
        Se analizaron 7 expedientes base, 19 registros de sanción del INE y 52 sentencias localizadas
        para explicar qué conducta originó cada observación, qué monto administrativo estuvo en controversia
        y qué resolvió la justicia electoral durante el proceso federal 2023-2024.
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.download_button(
    "Descargar PDF",
    data=cached_pdf_report(),
    file_name="observatorio_diputaciones_electas_2023_2024.pdf",
    mime="application/pdf",
)

st.markdown(
    '<section class="sanction-board">'
    '<div class="sanction-total">'
    '<div class="label">Monto observado por el INE</div>'
    f'<div class="amount">{money(total_sancionado)}</div>'
    f'<div class="note">Los {money(total_sancionado)} resultan de sumar los montos originales de {registros_cuantificados} registros de sanción del INE con importe mayor a cero, relacionados con {casos["expediente"].nunique()} expedientes base. Otros {registros_no_cuantificados} registros permanecen en cero o no integrados. Monto firme identificado en este corte: {money(total_firme)}.</div>'
    '</div>'
    '<div class="cause-list">'
    + "".join(
        '<div class="cause-row">'
        f'<div class="cause">{text_label(row["conducta"])}</div>'
        f'<div class="money">{money(float(row["monto"]))}</div>'
        '</div>'
        for _, row in top_causas.iterrows()
    )
    + '</div>'
    '</section>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="plain-steps">
      <div class="plain-step"><strong>1. La causa</strong><span>Gastos no reportados, XML faltantes, propaganda o documentación insuficiente generan observaciones.</span></div>
      <div class="plain-step"><strong>2. La sanción</strong><span>El INE fija montos y consecuencias; los partidos o candidaturas pueden impugnar.</span></div>
      <div class="plain-step"><strong>3. La sentencia</strong><span>El TEPJF confirma, modifica o revoca y define que queda vigente en el expediente.</span></div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <section class="meeting-brief">
      <div class="meeting-copy">
        <div class="label">Modelo de actualización y seguimiento</div>
        <div class="title">De la fuente oficial a la base viva</div>
        <p>
          El corte actual convierte sentencias, dictámenes, resoluciones y registros de sanción en una matriz
          verificable. La lectura se limita a diputaciones federales 2024 y separa con claridad controversias
          consultables, criterios jurisdiccionales y montos positivos que sí pueden incorporarse a la sumatoria.
        </p>
      </div>
      <div class="meeting-grid">
        <div>
          <b>1. Fuente y extracción</b>
          <span>Registrar URL oficial, expediente, acto de origen, conducta, órgano resolutor, candidatura, entidad, distrito y monto observado cuando exista una cantidad económica positiva.</span>
        </div>
        <div>
          <b>2. Criterio y efecto</b>
          <span>Clasificar la regla aplicable, la carga probatoria, el alcance de la confirmación, modificación o revocación, y el efecto práctico sobre sujetos obligados, campañas o resultados.</span>
        </div>
        <div>
          <b>3. Seguimiento activo</b>
          <span>Actualizar la app, fichas y PDF desde una base común para observar riesgos antes del proceso, monitorear incidencias durante la campaña y explicar resultados después de la fiscalización.</span>
        </div>
      </div>
      <div class="meeting-flow">
        <span>Fuente oficial</span><i></i><span>Extracción</span><i></i><span>Criterio validado</span><i></i><span>Matriz viva</span><i></i><span>App y PDF</span>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

left_intro, right_intro = st.columns([1.05, .95])
with left_intro:
    st.subheader("Causas por monto observado por el INE")
    st.caption("Las barras agrupan únicamente registros con monto original positivo observado por el INE. Los expedientes visibles en el mapa o la tabla también sirven para ubicar sentencias y conductas territoriales; si el registro está en cero o no integrado, no se añade a esta sumatoria porque no incorpora una sanción monetaria cuantificable.")
    chart_causas = top_causas.sort_values("monto", ascending=True).copy()
    chart_causas["conducta_label"] = chart_causas["conducta"].map(text_label)
    fig = px.bar(chart_causas, x="monto", y="conducta_label", orientation="h", text=chart_causas["monto"].map(money))
    fig.update_traces(marker_color="#6B1531", textposition="outside")
    fig.update_layout(
        showlegend=False,
        margin=dict(l=0, r=40, t=4, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Montserrat", color="#211816"),
        xaxis=dict(title="", showgrid=True, gridcolor="rgba(107,21,49,.13)", zeroline=False),
        yaxis=dict(title=""),
    )
    st.plotly_chart(fig, use_container_width=True)

with right_intro:
    st.subheader("Estado de los montos")
    estado = sanciones.groupby("monto_final_estado", as_index=False).agg(monto=("monto_original", "sum"), registros=("sancion_id", "count"))
    fig = px.bar(estado, x="monto_final_estado", y="monto", text=estado["monto"].map(money), color="monto_final_estado", color_discrete_sequence=["#6B1531", "#C59A3D", "#1E5B4F"])
    fig.update_traces(textposition="outside")
    fig.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=4, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Montserrat", color="#211816"),
        xaxis=dict(title=""),
        yaxis=dict(title="", showgrid=True, gridcolor="rgba(107,21,49,.13)", zeroline=False),
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Sentencias y expedientes consultables")
st.caption("Enlaces directos al expediente localizado en el portal del TEPJF.")
hallazgo_lookup = {
    exp_key(row["expediente"]): (row["entidad"], row["distrito"])
    for _, row in hallazgos.iterrows()
}
consultable_records = []
seen_urls = set()
seen_exps = set()
for _, row in casos_vinculados.iterrows():
    entidad_row, distrito_row = case_location(row, hallazgo_lookup)
    url = str(row["url_sentencia"])
    seen_urls.add(url)
    seen_exps.add(exp_key(row["expediente"]))
    monto_observado = float(row["monto_observado"])
    sancion_count = int(row["sanciones"]) if pd.notna(row["sanciones"]) else 0
    if monto_observado > 0:
        monto_label = money_exact(monto_observado)
        monto_note = f'Observado por el INE · {sancion_count} {plural(sancion_count, "registro")} {plural(sancion_count, "monetario")}'
        row_summary = case_conduct_summary(row, sanciones)
    else:
        monto_label = "$0.00"
        monto_note = "No se suma: no hay cantidad económica."
        row_summary = (
            case_conduct_summary(row, sanciones)
            + " El caso aparece en el mapa porque permite ubicar una controversia vinculada "
            + "con esa entidad o distrito. No se suma al total porque la sumatoria no cuenta "
            + "expedientes, sino pesos: en este registro no hay una cantidad económica positiva "
            + "fijada, confirmada o modificada para agregar al cálculo."
        )
    consultable_records.append(
        {
            "expediente": row["expediente"],
            "fecha": row["fecha_sentencia"],
            "sala": row["sala"],
            "entidad": entidad_row,
            "distrito": distrito_row,
            "resumen": row_summary,
            "monto": monto_label,
            "monto_nota": monto_note,
            "url": url,
        }
    )
for _, row in hallazgos.iterrows():
    url = str(row["url_oficial"])
    key = exp_key(row["expediente"])
    if url in seen_urls or key in seen_exps:
        continue
    consultable_records.append(
        {
            "expediente": row["expediente"],
            "fecha": row["fecha"],
            "sala": row["organo"],
            "entidad": row["entidad"],
            "distrito": row["distrito"],
            "resumen": incidence_detail_summary(row) + " El caso aparece en el mapa porque permite ubicar una controversia vinculada con esa entidad o distrito. No se integra monto porque este registro no contiene una cantidad económica positiva que pueda agregarse al cálculo.",
            "monto": "No integrado",
            "monto_nota": "No se suma: no hay cantidad económica.",
            "url": url,
        }
    )
consultable_records = sorted(
    consultable_records,
    key=lambda row: (
        ENTITY_ORDER.get(row["entidad"], 9),
        state_display(row["entidad"]),
        row["distrito"],
        row["fecha"],
        row["expediente"],
    ),
)
link_rows = []
for row in consultable_records:
    display_entidad, display_distrito = display_entity_and_scope(row["entidad"], row["distrito"])
    link_rows.append(
        '<div class="link-item">'
        f'<div class="case-id">{html.escape(row["expediente"])}<br><span class="small-muted">{html.escape(row["fecha"])} · {html.escape(row["sala"])}</span></div>'
        f'<div class="case-geo"><strong>{html.escape(display_entidad)}</strong><span>{html.escape(display_distrito)}</span></div>'
        f'<div class="case-text">{html.escape(row["resumen"])}<br><strong>Monto cuantificado: {html.escape(row["monto"])}</strong><br><span class="small-muted">{html.escape(row["monto_nota"])}</span></div>'
        f'<a href="{html.escape(row["url"])}" target="_blank" rel="noopener">{html.escape(row["url"])}</a>'
        '</div>'
    )
st.markdown('<div class="link-list">' + "".join(link_rows) + '</div>', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="method-separator">
      <strong>Procedencia de cifras</strong>
      <p>La búsqueda en el portal del TEPJF delimitó 52 sentencias revisadas; de ellas se seleccionaron 7 expedientes base por su relación directa con fiscalización de diputaciones federales.</p>
      <div class="method-grid">
        <div><b>{money_exact(total_sancionado)}</b><span>Suma exacta de 15 registros monetarios originalmente observados por el INE en cuatro sentencias. En portada se abrevia como {money(total_sancionado)}.</span></div>
        <div><b>Sentencias que alimentan el monto</b><span>SUP-RAP-342/2024: Movimiento Ciudadano, $7,303,754.15. SUP-RAP-352/2024: PAN, $10,312,470.58. SUP-RAP-357/2024: PT, $2,638,887.56. SUP-RAP-413/2024: Morena, $445,361.30.</span></div>
        <div><b>Causas principales</b><span>Agrupan esos 15 registros por conducta y suman el monto original observado por el INE.</span></div>
        <div><b>Qué no se añade a la sumatoria</b><span>{registros_no_cuantificados} registros aparecen en el mapa o en la tabla porque son expedientes localizados por entidad, distrito o conducta. No se agregan a los {money_exact(total_sancionado)} porque el total no cuenta expedientes: cuenta únicamente cantidades económicas positivas observadas en registros de sanción. Cuando un expediente está en $0.00 o no integrado, se informa como caso consultable, pero no modifica la suma de pesos porque no hay monto que agregar. El monto firme de {money(total_firme)} suma solo registros con monto_final firme.</span></div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="newspaper-shell">
      <div class="masthead">
        <div class="kicker">Cámara de Diputados · LXVI Legislatura</div>
        <div class="headline">500 curules como contexto</div>
        <div class="deck">
          La integración de la Cámara permite ubicar a partidos, candidaturas y bloques políticos
          dentro del mismo proceso electoral en el que surgieron observaciones, multas e impugnaciones.
        </div>
      </div>
      <div class="folio-row">
        <span>300 distritos</span><span>200 listas</span><span>6 grupos parlamentarios</span><span>52 sentencias revisadas</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="story-hero">'
    '<div class="story-card majority">'
    '<div class="story-label">Bloque Morena · PVEM · PT</div>'
    f'<div class="story-number">{bloque_morena}</div>'
    '<div class="story-note">curules articulan la mayoría legislativa que define el punto de partida de la LXVI Legislatura.</div>'
    '</div>'
    '<div class="story-split">'
    '<div class="story-card">'
    '<div class="story-label">PAN · PRI</div>'
    f'<div class="story-number">{bloque_pan_pri}</div>'
    '<div class="story-note">curules integran el principal bloque opositor tradicional.</div>'
    '</div>'
    '<div class="story-card">'
    '<div class="story-label">Movimiento Ciudadano</div>'
    f'<div class="story-number">{mc_total}</div>'
    '<div class="story-note">curules completan la tercera vía parlamentaria.</div>'
    '</div>'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)

view = df.copy()
st.markdown(
    '<div class="case-ribbon">'
    f'<div><strong>{len(resumen)}</strong><span>sentencias TEPJF revisadas</span></div>'
    f'<div><strong>{int(resumen["constancia_mayoria"].sum())}</strong><span>tocan constancia de mayoría</span></div>'
    f'<div><strong>{int(resumen["fiscalizacion"].sum())}</strong><span>incluyen fiscalización</span></div>'
    f'<div><strong>{int(resumen["propaganda"].sum())}</strong><span>abordan propaganda</span></div>'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="dataviz-band"><div class="section-label">Explorar la integración</div>', unsafe_allow_html=True)
filters = st.columns([1, 1, 1])
partido = filters[0].selectbox("Grupo parlamentario", ["Todos"] + sorted(df["partido_estimado"].unique()))
principio = filters[1].selectbox("Vía de acceso", ["Todos"] + sorted(df["principio_estimado"].unique()))
entidad = filters[2].selectbox("Entidad", ["Todas"] + sorted(df["entidad"].unique()))
st.markdown("</div>", unsafe_allow_html=True)

if partido != "Todos":
    view = view[view["partido_estimado"].eq(partido)]
if principio != "Todos":
    view = view[view["principio_estimado"].eq(principio)]
if entidad != "Todas":
    view = view[view["entidad"].eq(entidad)]

incidencias = hallazgos.copy()
if entidad != "Todas":
    entidad_ascii = {
        "Ciudad de México": "Ciudad de Mexico",
        "Michoacán": "Michoacan",
    }.get(entidad, entidad)
    incidencias = incidencias[incidencias["entidad"].isin([entidad, entidad_ascii])]
incidencias_estatales = incidencias[incidencias["entidad"].isin(state_points)].copy()
incidencias_estatales["entidad_label"] = incidencias_estatales["entidad"].map(state_display)
incidence_counts = (
    incidencias_estatales.groupby(["entidad", "entidad_label"], as_index=False)
    .agg(incidencias=("expediente", "count"), expedientes=("expediente", lambda values: ", ".join(values)))
    .sort_values("incidencias", ascending=False)
)
incidence_counts["lat"] = incidence_counts["entidad"].map(lambda value: state_points.get(value, (None, None))[0])
incidence_counts["lon"] = incidence_counts["entidad"].map(lambda value: state_points.get(value, (None, None))[1])
incidence_counts = incidence_counts.dropna(subset=["lat", "lon"])
incidencias_nacionales = len(incidencias) - len(incidencias_estatales)
incidence_items = []
for _, entity_label in MAP_ENTITY_COLUMNS:
    entity_rows = incidencias_estatales[incidencias_estatales["entidad_label"].eq(entity_label)].sort_values(["fecha", "expediente"])
    count = len(entity_rows)
    entries = []
    for _, row in entity_rows.iterrows():
        entries.append(
            '<div class="incidence-entry">'
            f'<b>{html.escape(row["expediente"])} · {html.escape(display_text(text_label(row["distrito"])))}</b>'
            f'<em>{html.escape(incidence_detail_summary(row))}</em>'
            '</div>'
        )
    incidence_items.append(
        '<div class="incidence-item">'
        f'<strong>{html.escape(entity_label)}</strong>'
        f'<span>{html.escape(REPORT_CUT_LABEL)} · {count} {plural(count, "expediente")}</span>'
        + "".join(entries)
        + '</div>'
    )
st.markdown(
    f"""
    <section class="map-deck">
      <div class="map-copy">
        <div class="label">Mapa de incidencias</div>
        <div class="title">Estados marcados por expediente</div>
        <div class="body">
          El mapa muestra México por entidad federativa: los estados sin incidencia permanecen en gris editorial
          y solo las entidades con incidencia territorial identificada aparecen en color guinda. Los asuntos de
          alcance nacional o representación proporcional se separan para no forzar una ubicación estatal.
        </div>
        <div class="incidence-strip">
          <div><strong>{len(incidencias_estatales)}</strong><span>incidencias estatales</span></div>
          <div><strong>{incidence_counts["entidad"].nunique()}</strong><span>entidades marcadas</span></div>
          <div><strong>{incidencias_nacionales}</strong><span>alcance nacional o RP</span></div>
        </div>
      </div>
      <div>
    """,
    unsafe_allow_html=True,
)
st.markdown(diputaciones_map_svg(incidence_counts), unsafe_allow_html=True)
st.markdown("</div></section>", unsafe_allow_html=True)
st.markdown('<div class="incidence-list">' + "".join(incidence_items) + "</div>", unsafe_allow_html=True)

metrics = [
    ("Curules visibles", len(view)),
    ("Distritos", int(view["principio_estimado"].eq("Mayoria Relativa").sum())),
    ("Listas", int(view["principio_estimado"].eq("Representacion Proporcional").sum())),
    ("Grupos", view["partido_estimado"].nunique()),
    ("Fichas públicas", int(view["perfil_url"].astype(bool).sum())),
]
st.markdown(
    '<div class="kpi-grid">'
    + "".join(
        f'<div class="kpi-tile"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div></div>'
        for label, value in metrics
    )
    + "</div>",
    unsafe_allow_html=True,
)

palette = {"MORENA": "#6B1531", "PVEM": "#1E5B4F", "PT": "#C59A3D", "PAN": "#2B5C8A", "PRI": "#8A1F2D", "MC": "#FF6600"}
party = view.groupby("partido_estimado", as_index=False).size().rename(columns={"size": "diputaciones"})
party = party.sort_values("diputaciones", ascending=False)
max_party = max(party["diputaciones"].max(), 1) if not party.empty else 1
party_rows = []
for _, row in party.iterrows():
    width = int((row["diputaciones"] / max_party) * 100)
    color = palette.get(row["partido_estimado"], "#31363b")
    party_rows.append(
        '<div class="party-row">'
        f'<div class="party">{row["partido_estimado"]}</div>'
        f'<div class="bar"><div class="fill" style="width:{width}%; background:{color};"></div></div>'
        f'<div class="value">{row["diputaciones"]}</div>'
        "</div>"
    )

principle_counts = view["principio_estimado"].value_counts().to_dict()
st.markdown(
    '<div class="summary-strip">'
    '<div class="composition-card">'
    '<div class="composition-title">Bloques parlamentarios</div>'
    + "".join(party_rows)
    + "</div>"
    '<div class="composition-card">'
    '<div class="composition-title">La historia territorial</div>'
    f'<div class="databox"><strong>{principle_counts.get("Mayoria Relativa", 0)}</strong> Mayoría relativa</div>'
    '<div class="rule"></div>'
    f'<div class="databox"><strong>{principle_counts.get("Representacion Proporcional", 0)}</strong> Representación proporcional</div>'
    '<div class="rule"></div>'
    f'<div class="small-muted">Fuente: fichas públicas de Cámara de Diputados LXVI. Vista filtrada: {len(view)} curules.</div>'
    "</div>"
    "</div>",
    unsafe_allow_html=True,
)

left, right = st.columns([1.05, .95])
with left:
    st.subheader("Composición por grupo parlamentario")
    order = party.sort_values("diputaciones", ascending=True)
    fig = px.bar(order, x="diputaciones", y="partido_estimado", orientation="h", text="diputaciones")
    fig.update_traces(marker_color=[palette.get(x, "#31363b") for x in order["partido_estimado"]], textposition="outside")
    fig.update_layout(
        showlegend=False,
        margin=dict(l=0, r=24, t=4, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Montserrat", color="#211816"),
        xaxis=dict(showgrid=True, gridcolor="rgba(107,21,49,.13)", zeroline=False),
        yaxis=dict(title=""),
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Principio de elección")
    principle = view.groupby(["partido_estimado", "principio_estimado"], as_index=False).size().rename(columns={"size": "diputaciones"})
    fig = px.bar(principle, x="partido_estimado", y="diputaciones", color="principio_estimado", barmode="stack", color_discrete_sequence=["#17130f", "#B88A2A"])
    fig.update_layout(
        legend_title_text="",
        margin=dict(l=0, r=0, t=4, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Montserrat", color="#211816"),
        yaxis=dict(showgrid=True, gridcolor="rgba(107,21,49,.13)", zeroline=False),
        xaxis=dict(title=""),
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Rostros de la legislatura")
st.caption("Muestra filtrada de fichas públicas de la Cámara de Diputados.")
gallery = view.head(24)
html = ['<div class="tight-grid">']
for _, row in gallery.iterrows():
    img_path = ROOT / row["foto_png_bn"]
    html.append(
        '<div class="mini-portrait">'
        f'<img src="data:image/png;base64,{base64.b64encode(img_path.read_bytes()).decode("ascii")}" alt="{row["nombre_listado"]}">'
        f'<div class="mini-name">{row["nombre_listado"]}</div>'
        f'<div class="mini-meta">{row["partido_estimado"]} &middot; {row["entidad"]} &middot; {row["distrito_circunscripcion"]}</div>'
        "</div>"
    )
html.append("</div>")
st.markdown("".join(html), unsafe_allow_html=True)

st.subheader("Registro de curules")
cols_table = [
    "nombre_listado",
    "partido_estimado",
    "principio_estimado",
    "entidad",
    "distrito_circunscripcion",
    "curul",
    "suplente",
    "licencia_en_listado",
    "perfil_url",
]
st.dataframe(view[cols_table], use_container_width=True, hide_index=True)
st.download_button(
    "Descargar diputaciones electas CSV",
    view.to_csv(index=False).encode("utf-8"),
    "diputaciones_electas_lxvi.csv",
    "text/csv",
)
