from __future__ import annotations

import base64
import html
import json
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components

from observatorio.data_loader import filtered_cases, load_all
from observatorio.metrics import count_by, kpis
from observatorio.ui import format_money, page_setup


page_setup("Observatorio de Fiscalización")
data = load_all()
casos = data["casos"]
sanciones = data["sanciones"]
agravios = data["agravios"]
hallazgos = data["hallazgos_portal"]
diputados_path = ROOT / "data" / "analysis" / "diputados_lxvi_electos.csv"
diputados = pd.read_csv(diputados_path, keep_default_na=False) if diputados_path.exists() else pd.DataFrame()
base_stats = kpis(casos, sanciones, agravios)

PARTY_COLORS = {
    "MORENA": "#8A1538",
    "Morena": "#8A1538",
    "Coalicion Sigamos Haciendo Historia": "#8A1538",
    "Coalición Sigamos Haciendo Historia": "#8A1538",
    "Movimiento Ciudadano": "#F58220",
    "MC": "#F58220",
    "Partido Accion Nacional": "#0057A8",
    "Partido Acción Nacional": "#0057A8",
    "PAN": "#0057A8",
    "Coalicion Fuerza y Corazon por Mexico": "#0057A8",
    "Coalición Fuerza y Corazón por México": "#0057A8",
    "Fuerza y Corazon por Mexico": "#0057A8",
    "Fuerza y Corazón por México": "#0057A8",
    "Partido del Trabajo": "#D71920",
    "PT": "#D71920",
    "Partido Revolucionario Institucional": "#E30613",
    "PRI": "#E30613",
    "Partido Verde Ecologista de Mexico": "#00A94F",
    "Partido Verde Ecologista de México": "#00A94F",
    "PVEM": "#00A94F",
}

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


def amount_note(amount: float | int | str, states: str, sentido: str) -> str:
    try:
        numeric = float(amount)
    except (TypeError, ValueError):
        numeric = 0
    state_text = str(states or "").lower()
    sentido_text = str(sentido or "").lower()
    if numeric > 0 and "pendiente" in state_text:
        return "Monto original observado; el monto final puede variar por efectos pendientes."
    if numeric > 0:
        return ""
    if "no aplica" in state_text or "sobresee" in sentido_text:
        return "Sin monto determinado: no hubo estudio de fondo o cuantificación económica firme."
    if "pendiente" in state_text or "revoca" in sentido_text:
        return "Sin monto firme: pendiente de determinación, reposición o nueva resolución."
    return "Sin monto determinado en el corte documentado."


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


def anchor_slug(value: object) -> str:
    normalized = unicodedata.normalize("NFKD", str(value or "").lower())
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    return "-".join(part for part in ascii_text.replace("/", " ").split() if part)


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


def subject_sanction_stats(source: pd.DataFrame) -> tuple[dict[str, str], dict[str, str]]:
    if source.empty:
        empty = {"name": "Sin datos", "amount": "$0", "detail": "$0.00"}
        return empty, empty
    data = source.copy()
    data["monto_original"] = pd.to_numeric(data.get("monto_original", 0), errors="coerce").fillna(0)
    grouped = (
        data[data["monto_original"].gt(0)]
        .groupby("sujeto_nombre", as_index=False)
        .agg(monto=("monto_original", "sum"), registros=("sancion_id", "count"))
        .sort_values("monto", ascending=False)
    )
    if grouped.empty:
        empty = {"name": "Sin montos positivos", "amount": "$0", "detail": "$0.00"}
        return empty, empty
    highest = grouped.iloc[0]
    lowest = grouped.iloc[-1]
    return (
        {
            "name": str(highest["sujeto_nombre"]),
            "amount": money_compact(highest["monto"]),
            "detail": f'{format_money(highest["monto"])} · {int(highest["registros"])} registros',
        },
        {
            "name": str(lowest["sujeto_nombre"]),
            "amount": money_compact(lowest["monto"]),
            "detail": f'{format_money(lowest["monto"])} · {int(lowest["registros"])} registros',
        },
    )


def expedient_table_html(source: pd.DataFrame, sanction_source: pd.DataFrame) -> str:
    if source.empty:
        return '<div class="expedient-empty"><strong>Sin expedientes para los filtros seleccionados.</strong></div>'
    amounts = pd.DataFrame(columns=["caso_id", "monto", "estados_monto"])
    if not sanction_source.empty:
        sanctions = sanction_source.copy()
        sanctions["monto_original"] = pd.to_numeric(sanctions["monto_original"], errors="coerce").fillna(0)
        amounts = (
            sanctions.groupby("caso_id", as_index=False)
            .agg(
                monto=("monto_original", "sum"),
                estados_monto=("monto_final_estado", lambda values: ", ".join(sorted({str(v) for v in values if str(v) and str(v) != "nan"}))),
            )
        )
    rows = source.merge(amounts, on="caso_id", how="left")
    rows["monto"] = rows["monto"].fillna(0)
    rows["estados_monto"] = rows["estados_monto"].fillna("")
    body = []
    for _, row in rows.iterrows():
        url = str(row.get("url_sentencia", "")).strip()
        expediente = html.escape(str(row.get("expediente", "")))
        expediente_html = f'<a href="{html.escape(url)}" target="_blank" rel="noopener">{expediente}</a>' if url else expediente
        note = amount_note(row["monto"], row.get("estados_monto", ""), row.get("sentido", ""))
        note_html = f'<span class="money-note">{html.escape(note)}</span>' if note else ""
        body.append(
            "<tr>"
            f'<td class="exp-id">{expediente_html}<span>{html.escape(str(row.get("fecha_sentencia", "")))}</span></td>'
            f'<td>{html.escape(text_label(row.get("partido_principal", "")))}</td>'
            f'<td>{html.escape(text_label(row.get("conducta_principal", "")))}</td>'
            f'<td><span class="status-pill">{html.escape(text_label(row.get("sentido", "")))}</span></td>'
            f'<td class="money-cell">{html.escape(money_compact(row["monto"]))}<span>{html.escape(format_money(row["monto"]))}</span>{note_html}</td>'
            f'<td>{html.escape(text_label(row.get("efectos_resumen", "")))}</td>'
            "</tr>"
        )
    return (
        '<div class="expedient-table-wrap"><table class="expedient-table">'
        "<thead><tr><th>Expediente</th><th>Sujeto</th><th>Conducta</th><th>Sentido</th><th>Monto observado</th><th>Efecto</th></tr></thead>"
        f"<tbody>{''.join(body)}</tbody></table></div>"
    )


def incidence_map_html() -> str:
    if hallazgos.empty or "entidad" not in hallazgos.columns:
        return ""
    map_path = ROOT / "data" / "geo" / "mexico_states_inegi_svg_paths.json"
    if not map_path.exists():
        return ""
    map_asset = json.loads(map_path.read_text(encoding="utf-8"))
    normalized = hallazgos.copy()
    normalized["entidad_label"] = normalized["entidad"].replace(
        {"Ciudad de Mexico": "Ciudad de México", "Michoacan": "Michoacán"}
    )
    counts = normalized.groupby("entidad_label", as_index=False).size().rename(columns={"size": "incidencias"})
    active_counts = {str(row["entidad_label"]): int(row["incidencias"]) for _, row in counts.iterrows()}
    official_aliases = {
        "Coahuila de Zaragoza": "Coahuila",
        "Michoacán de Ocampo": "Michoacán",
        "Veracruz de Ignacio de la Llave": "Veracruz",
    }
    shapes = []
    hotspots = []
    notes = []
    active_slugs = []
    for state in map_asset["states"]:
        official_name = state["name"]
        display_name = official_aliases.get(official_name, official_name)
        count = active_counts.get(display_name, 0)
        slug = anchor_slug(display_name)
        class_name = "state active linked" if count else "state"
        data_attrs = f' data-slug="{html.escape(slug)}" tabindex="0"' if count else ""
        path = f'<path class="{class_name}"{data_attrs} d="{state["path"]}"><title>{html.escape(display_name)}</title></path>'
        if count:
            active_slugs.append(slug)
            shapes.append(path)
            if display_name == "Ciudad de México":
                hotspots.append(
                    f'<g class="map-hotspot" data-slug="{html.escape(slug)}" tabindex="0" '
                    f'role="button" aria-label="Consultar incidencias de {html.escape(display_name)}">'
                    '<circle class="hotspot-target" cx="313.5" cy="233.1" r="14"/>'
                    '<circle class="hotspot-dot" cx="313.5" cy="233.1" r="5"/>'
                    f'<title>Consultar {html.escape(display_name)}</title></g>'
                )
            notes.append(
                f'<button class="map-note" type="button" data-slug="{html.escape(slug)}">'
                f'<strong>{html.escape(display_name)}</strong>'
                f'<span>{count} incidencia{"s" if count != 1 else ""}</span></button>'
            )
        else:
            shapes.append(path)
    cards = []
    first_slug = active_slugs[0] if active_slugs else ""
    for entity, group in normalized.groupby("entidad_label", sort=True):
        slug = anchor_slug(entity)
        entries = []
        for _, row in group.iterrows():
            url = str(row.get("url_oficial", "")).strip()
            link = f'<a href="{html.escape(url)}" target="_blank" rel="noopener">Sentencia oficial</a>' if url else ""
            entries.append(
                '<div class="incidence-card-entry">'
                f'<b>{html.escape(str(row.get("expediente", "")))}</b>'
                f'<span>{html.escape(text_label(row.get("tema", "")))}</span>'
                f'<p>{html.escape(text_label(row.get("razon_prioridad", "")))}</p>'
                f'{link}'
                '</div>'
            )
        cards.append(
            f'<article class="incidence-card" data-card="{html.escape(slug)}">'
            f'<strong>{html.escape(entity)}</strong>'
            f'{"".join(entries)}'
            '</article>'
        )
    return (
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800;900&display=swap');
        :root { --guinda:#6B1531; --guinda-dark:#3b0718; --dorado:#C59A3D; --verde:#1E5B4F; --black:#14100d; --muted:#665a52; --paper:#fffdf8; --pale:#fbf2e5; --line:#d7c7b2; }
        * { box-sizing: border-box; }
        body { margin: 0; background: transparent; color: var(--black); font-family: "Montserrat", sans-serif; overflow-x: hidden; }
        .map-shell { display: grid; grid-template-columns: minmax(0, 1.15fr) minmax(290px, .85fr); gap: 22px; align-items: stretch; }
        .map-column, .incidence-card-panel { border-top: 5px solid var(--guinda); background: #fbf7ef; min-width: 0; }
        .map-column { display: grid; grid-template-rows: auto minmax(0, 1fr); }
        .mexico-map-wrap { min-height: 320px; overflow: hidden; position: relative; }
        .map-svg { width: 100%; height: 320px; display: block; }
        .state { fill: #e8ddcc; stroke: #fffdf8; stroke-width: 2.2; vector-effect: non-scaling-stroke; }
        .state.active { fill: var(--guinda); stroke: #fffdf8; cursor: pointer; transition: fill .18s ease, filter .18s ease, opacity .18s ease; }
        .state.active:hover, .state.active.selected { fill: var(--dorado); filter: drop-shadow(0 5px 8px rgba(107,21,49,.28)); opacity: .98; }
        .map-hotspot { cursor: pointer; outline: none; }
        .hotspot-target { fill: rgba(255,253,248,.9); stroke: var(--guinda); stroke-width: 2; vector-effect: non-scaling-stroke; transition: fill .18s ease, stroke .18s ease, transform .18s ease; transform-box: fill-box; transform-origin: center; }
        .hotspot-dot { fill: var(--guinda); pointer-events: none; transition: fill .18s ease; }
        .map-hotspot:hover .hotspot-target, .map-hotspot.selected .hotspot-target, .map-hotspot:focus-visible .hotspot-target { fill: var(--dorado); stroke: var(--guinda-dark); transform: scale(1.12); }
        .map-hotspot:hover .hotspot-dot, .map-hotspot.selected .hotspot-dot { fill: var(--guinda-dark); }
        .map-notes { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px; padding: 12px; background: #fffdf8; border-bottom: 1px solid rgba(20,16,13,.15); }
        .map-note { appearance: none; background: var(--pale); border: 1px solid rgba(107,21,49,.2); border-left: 4px solid var(--guinda); color: inherit; cursor: pointer; display: block; min-height: 58px; font-family: "Montserrat", sans-serif; padding: 8px 10px; text-align: left; transition: transform .18s ease, border-color .18s ease, background .18s ease, box-shadow .18s ease; }
        .map-note:hover, .map-note.selected, .map-note:focus-visible { background: #fffdf8; border-color: var(--dorado); box-shadow: 0 8px 18px rgba(70,45,25,.1); transform: translateY(-2px); outline: none; }
        .map-note strong { display: block; color: var(--guinda-dark); font-size: .7rem; font-weight: 900; line-height: 1.08; text-transform: uppercase; overflow-wrap: anywhere; }
        .map-note span { display: block; color: var(--muted); font-size: .6rem; font-weight: 900; margin-top: 3px; text-transform: uppercase; }
        .incidence-card-panel { background: linear-gradient(180deg, #fffdf8, #fbf2e5); min-height: 400px; max-height: 400px; overflow-y: auto; }
        .incidence-card { display: none; padding: 18px 18px 20px; animation: focusIn .28s ease both; }
        .incidence-card.selected { display: block; }
        .incidence-card strong { color: var(--black); display: block; font-size: clamp(1.45rem, 3vw, 2.15rem); font-weight: 900; line-height: .95; margin-bottom: 14px; text-transform: uppercase; overflow-wrap: anywhere; }
        .incidence-card-entry { border-top: 1px solid rgba(20,16,13,.18); padding: 12px 0 13px; }
        .incidence-card-entry b { color: var(--guinda-dark); display: block; font-size: .94rem; font-weight: 900; line-height: 1.14; text-transform: uppercase; overflow-wrap: anywhere; }
        .incidence-card-entry span { color: var(--black); display: block; font-size: .82rem; font-weight: 900; line-height: 1.25; margin-top: 6px; overflow-wrap: anywhere; }
        .incidence-card-entry p { color: var(--muted); font-size: .8rem; font-weight: 750; line-height: 1.34; margin: 7px 0 8px; overflow-wrap: anywhere; }
        .incidence-card-entry a { color: var(--guinda); font-size: .72rem; font-weight: 900; text-decoration: none; text-transform: uppercase; border-bottom: 1px solid rgba(107,21,49,.36); }
        @keyframes focusIn { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
        @media (max-width: 760px) {
          .map-shell { grid-template-columns: 1fr; gap: 14px; }
          .map-notes { display: flex; gap: 8px; overflow-x: auto; padding: 10px; scroll-snap-type: x mandatory; }
          .map-note { flex: 0 0 min(72vw, 220px); scroll-snap-align: start; }
          .mexico-map-wrap { min-height: 270px; }
          .map-svg { height: 270px; }
          .incidence-card-panel { min-height: 250px; max-height: none; }
        }
        @media (prefers-reduced-motion: reduce) {
          *, *::before, *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: .01ms !important; }
        }
        </style>
        """
        f'<div class="map-shell" data-default="{html.escape(first_slug)}">'
        '<div class="map-column">'
        f'<div class="map-notes" aria-label="Entidades con incidencias">{"".join(notes)}</div>'
        '<div class="mexico-map-wrap">'
        f'<svg class="map-svg" viewBox="{map_asset["viewBox"]}" role="img" aria-label="Mapa de México con incidencias de fiscalización">'
        '<rect x="0" y="0" width="520" height="330" fill="#fbf7ef"/>'
        f'{"".join(shapes)}'
        f'{"".join(hotspots)}'
        '</svg>'
        '</div>'
        '</div>'
        f'<div class="incidence-card-panel">{"".join(cards)}</div>'
        '</div>'
        """
        <script>
        const shell = document.querySelector('.map-shell');
        const selectEntity = (slug) => {
          document.querySelectorAll('[data-card]').forEach((card) => card.classList.toggle('selected', card.dataset.card === slug));
          document.querySelectorAll('[data-slug]').forEach((item) => item.classList.toggle('selected', item.dataset.slug === slug));
        };
        document.querySelectorAll('[data-slug]').forEach((item) => {
          item.addEventListener('click', () => selectEntity(item.dataset.slug));
          item.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' || event.key === ' ') {
              event.preventDefault();
              selectEntity(item.dataset.slug);
            }
          });
        });
        selectEntity(shell?.dataset.default || '');
        const reportHeight = () => {
          window.parent.postMessage({
            isStreamlitMessage: true,
            type: 'streamlit:setFrameHeight',
            height: Math.ceil(document.documentElement.scrollHeight)
          }, '*');
        };
        new ResizeObserver(reportHeight).observe(document.body);
        window.addEventListener('load', reportHeight);
        reportHeight();
        </script>
        """
    )


def install_scroll_motion() -> None:
    components.html(
        """
        <script>
        (() => {
          const parentWindow = window.parent;
          const parentDocument = parentWindow.document;
          parentWindow.__observatorioMotionCleanup?.();

          const selectors = [
            '.home-section',
            '.analysis-reader',
            '.criteria-reader',
            '.criterion-detail',
            '.data-editorial-head',
            '.responsive-kpi',
            '.viz-section',
            '.filter-band',
            '.chart-kicker',
            '.section-subhead',
            '.executive-reading',
            '.methodology-band',
            '.methodology-grid article',
            '.systematization-band',
            '.systematization-flow li',
            '.home-download-band',
            '.expedient-table-wrap',
            '[data-testid="stPlotlyChart"]',
            'iframe'
          ];
          const targets = [...new Set(
            selectors.flatMap((selector) => [...parentDocument.querySelectorAll(selector)])
          )].filter((element) => element !== window.frameElement);

          parentDocument.documentElement.classList.add('js-scroll-motion');
          const reduceMotion = parentWindow.matchMedia('(prefers-reduced-motion: reduce)').matches;
          targets.forEach((element) => element.classList.add('scroll-reveal'));

          [
            '.responsive-kpi-grid',
            '.methodology-grid',
            '.systematization-flow',
            '.home-doc-grid',
            '.criteria-map'
          ].forEach((selector) => {
            parentDocument.querySelectorAll(selector).forEach((group) => {
              [...group.children].forEach((child, index) => {
                child.style.setProperty('--reveal-delay', `${Math.min(index, 5) * 65}ms`);
              });
            });
          });

          let observer;
          if (reduceMotion || !('IntersectionObserver' in parentWindow)) {
            targets.forEach((element) => element.classList.add('is-visible'));
          } else {
            observer = new parentWindow.IntersectionObserver((entries) => {
              entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target);
              });
            }, {
              root: null,
              rootMargin: '0px 0px -9% 0px',
              threshold: 0.08
            });
            targets.forEach((element) => observer.observe(element));
          }

          const progress = parentDocument.querySelector('.reading-progress span');
          const appView = parentDocument.querySelector('[data-testid="stAppViewContainer"]');
          const mainScroller = parentDocument.querySelector('[data-testid="stMain"]');
          const navLinks = [...parentDocument.querySelectorAll('.site-links a[href^="#"]')];
          const scrollSources = [parentWindow, appView, mainScroller].filter(Boolean);
          let framePending = false;

          const updateReadingState = () => {
            framePending = false;
            const root = parentDocument.documentElement;
            const body = parentDocument.body;
            const scrollTop = Math.max(
              parentWindow.scrollY || 0,
              root.scrollTop || 0,
              body.scrollTop || 0,
              appView?.scrollTop || 0,
              mainScroller?.scrollTop || 0
            );
            const scrollHeight = Math.max(
              root.scrollHeight,
              body.scrollHeight,
              appView?.scrollHeight || 0,
              mainScroller?.scrollHeight || 0
            );
            const viewportHeight = mainScroller?.clientHeight || appView?.clientHeight || parentWindow.innerHeight || 1;
            const ratio = Math.min(1, Math.max(0, scrollTop / Math.max(1, scrollHeight - viewportHeight)));
            progress?.style.setProperty('transform', `scaleX(${ratio})`);

            let activeLink = navLinks[0];
            navLinks.forEach((link) => {
              const anchor = parentDocument.querySelector(link.getAttribute('href'));
              if (anchor && anchor.getBoundingClientRect().top <= Math.min(220, viewportHeight * .28)) {
                activeLink = link;
              }
            });
            navLinks.forEach((link) => {
              const active = link === activeLink;
              link.classList.toggle('active', active);
              if (active) link.setAttribute('aria-current', 'location');
              else link.removeAttribute('aria-current');
            });
          };

          const requestUpdate = () => {
            if (framePending) return;
            framePending = true;
            parentWindow.requestAnimationFrame(updateReadingState);
          };
          scrollSources.forEach((source) => source.addEventListener('scroll', requestUpdate, {passive: true}));
          parentWindow.addEventListener('resize', requestUpdate, {passive: true});
          updateReadingState();

          parentWindow.__observatorioMotionCleanup = () => {
            observer?.disconnect();
            scrollSources.forEach((source) => source.removeEventListener('scroll', requestUpdate));
            parentWindow.removeEventListener('resize', requestUpdate);
          };
        })();
        </script>
        """,
        height=0,
        scrolling=False,
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


def filter_controls(
    *,
    label: str = "Filtros de lectura",
    title: str = "Delimita el corte",
    note: str = "Sin selección activa, la consulta conserva el corpus completo.",
    key_prefix: str = "panel",
    include_party: bool = True,
) -> dict[str, list[str]]:
    st.markdown(
        f"""
        <section class="filter-band">
          <div class="label">{html.escape(label)}</div>
          <div class="title">{html.escape(title)}</div>
          <p>{html.escape(note)}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )
    filters: dict[str, list[str]] = {}
    filter_specs = [
        ("Nivel", "nivel"),
        ("Partido", "partido_principal"),
        ("Conducta", "conducta_principal"),
        ("Sentido", "sentido"),
    ]
    if not include_party:
        filter_specs = [spec for spec in filter_specs if spec[1] != "partido_principal"]
        filters["partido_principal"] = sorted([x for x in casos["partido_principal"].unique() if str(x)])
    cols = st.columns(len(filter_specs))
    for idx, (field_label, column) in enumerate(filter_specs):
        options = sorted([x for x in casos[column].unique() if str(x)]) if column in casos.columns else []
        selected = cols[idx].pills(
            field_label,
            options,
            selection_mode="multi",
            default=[],
            key=f"{key_prefix}_pill_{column}",
        )
        filters[column] = list(selected or options)
    return filters


st.markdown(
    """
    <nav class="site-nav home-nav">
      <div class="reading-progress" aria-hidden="true"><span></span></div>
        <div class="site-brand">Observatorio Electoral</div>
      <div class="site-links">
        <a class="active" href="#inicio">Inicio</a>
        <a href="#publicaciones">Publicaciones</a>
        <a href="#analisis-en-pagina">Análisis</a>
        <a href="#criterios-en-pagina">Criterios</a>
        <a href="#panel-datos">Datos</a>
        <a href="#sistematizacion">Propuesta</a>
        <a href="#descargas">Descargas</a>
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
          Instrumento de consulta sobre sanciones, efectos jurisdiccionales y criterios en materia
          de fiscalización electoral vinculados con diputaciones federales del proceso electoral
          federal 2023-2024.
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
      <span class="dock-label">Documentos PDF</span>
      <a class="pill primary" href="{pdf_data_uri(pdf_options["Qué se sancionó en las elecciones de diputaciones federales 2024"]["path"])}"
         download="{pdf_options["Qué se sancionó en las elecciones de diputaciones federales 2024"]["file_name"]}"
         aria-label="Descargar análisis de fiscalización en PDF"
         title="Descargar análisis de fiscalización en PDF">
        <span class="download-mark" aria-hidden="true">↓</span>
        <span class="download-copy"><b>Descargar</b><small>Fiscalización</small></span>
      </a>
      <a class="pill secondary" href="{pdf_data_uri(pdf_options["Criterios de fiscalización electoral derivados del proceso 2023-2024"]["path"])}"
         download="{pdf_options["Criterios de fiscalización electoral derivados del proceso 2023-2024"]["file_name"]}"
         aria-label="Descargar análisis de criterios en PDF"
         title="Descargar análisis de criterios en PDF">
        <span class="download-mark" aria-hidden="true">↓</span>
        <span class="download-copy"><b>Descargar</b><small>Criterios</small></span>
      </a>
    </div>
    """,
    unsafe_allow_html=True,
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
          El observatorio integra síntesis analítica, fichas de criterios, datos verificables y
          documentos descargables para facilitar la lectura pública del proceso de fiscalización.
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
          <div class="label">Método de consulta</div>
          <div class="title">Del expediente al criterio</div>
        </div>
        <div class="body">
          La lectura organiza expedientes, conductas sancionadas, efectos de sentencia, criterios
          jurisdiccionales, dimensión territorial y composición final de curules.
        </div>
      </div>
      <div class="reading-rail">
        <div><b>01</b><span>Identificar la conducta observada y el sujeto obligado vinculado.</span></div>
        <div><b>02</b><span>Revisar el sentido de la resolución y el efecto jurisdiccional.</span></div>
        <div><b>03</b><span>Contrastar el expediente con criterios, territorio, montos y curules.</span></div>
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
        <span>Consulta la síntesis, los criterios, la tabla de expedientes y los datos derivados del corte.</span>
        <a href="#analisis-en-pagina">Leer en página</a>
      </div>
      <div class="home-doc-card">
        <b>Corpus de sentencias TEPJF</b>
        <span>El corpus se presenta mediante fichas, mapa territorial, gráfica de curules y tabla de expedientes.</span>
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

filters = filter_controls(
    label="Filtros del panel",
    title="Delimita el corte general",
    note="Estos filtros afectan las cifras superiores, curules vinculadas al corte y lectura jurisdiccional del panel.",
    key_prefix="panel",
)
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

most_sanctioned, least_sanctioned = subject_sanction_stats(sanciones_filtradas)
if not diputados.empty:
    party_curules = (
        diputados.groupby("partido_estimado", as_index=False)
        .size()
        .rename(columns={"size": "curules"})
        .sort_values("curules", ascending=True)
    )
    st.markdown(
        f"""
        <section class="viz-section" id="curules">
          <div class="viz-head">
            <div>
              <div class="label">Resultado legislativo</div>
              <div class="title">Curules finales</div>
            </div>
            <p>
              Composición de las 500 diputaciones LXVI conforme al registro integrado.
              Esta lectura permite contrastar fuerza legislativa y sanciones observadas.
            </p>
          </div>
          <div class="sanction-extremes">
            <div><span>Más multado</span><b>{html.escape(most_sanctioned["name"])}</b><strong>{html.escape(most_sanctioned["amount"])}</strong><em>{html.escape(most_sanctioned["detail"])}</em></div>
            <div><span>Menos multado con monto positivo</span><b>{html.escape(least_sanctioned["name"])}</b><strong>{html.escape(least_sanctioned["amount"])}</strong><em>{html.escape(least_sanctioned["detail"])}</em></div>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    fig_curules = px.bar(
        party_curules,
        x="curules",
        y="partido_estimado",
        orientation="h",
        text="curules",
        color="partido_estimado",
        color_discrete_map=PARTY_COLORS,
    )
    fig_curules.update_traces(textposition="outside", cliponaxis=False)
    fig_curules.update_layout(
        height=max(360, 44 * len(party_curules) + 120),
        margin=dict(l=110, r=56, t=10, b=42),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        font=dict(family="Montserrat", size=13),
        xaxis=dict(title="", automargin=True, showgrid=True, gridcolor="rgba(107,21,49,.12)"),
        yaxis=dict(title="", automargin=True),
    )
    st.plotly_chart(fig_curules, width="stretch")

map_html = incidence_map_html()
if map_html:
    st.markdown(
        """
        <section class="viz-section" id="mapa-incidencias">
          <div class="viz-head">
            <div>
              <div class="label">Lectura territorial</div>
              <div class="title">Mapa de incidencias</div>
            </div>
            <p>
              Entidades vinculadas con expedientes o hallazgos documentados en el corte.
              Selecciona una entidad activa para consultar la incidencia y la sentencia oficial.
            </p>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    components.html(map_html, height=450, scrolling=False)

st.markdown('<div class="chart-kicker">Lectura por sujeto obligado</div>', unsafe_allow_html=True)
party_chart_filters = filter_controls(
    label="Filtros de gráfica",
    title="Casos por partido",
    note="Estos filtros afectan únicamente la gráfica de casos por partido y el resultado jurisdiccional inmediato.",
    key_prefix="party_chart",
)
casos_grafica = filtered_cases(
    casos,
    nivel=party_chart_filters["nivel"],
    partido=party_chart_filters["partido_principal"],
    conducta=party_chart_filters["conducta_principal"],
    sentido=party_chart_filters["sentido"],
)
st.subheader("Casos por partido")
chart_df = count_by(casos_grafica, "partido_principal")
if not chart_df.empty:
    fig = px.bar(
        chart_df,
        x="casos",
        y="partido_principal",
        orientation="h",
        color="partido_principal",
        color_discrete_map=PARTY_COLORS,
    )
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
chart_df = count_by(casos_grafica, "sentido")
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

st.markdown('<div class="section-subhead">Tabla de expedientes</div>', unsafe_allow_html=True)
table_filters = filter_controls(
    label="Filtros de tabla",
    title="Expedientes consultables",
    note="Estos filtros afectan únicamente la tabla y la descarga CSV de expedientes.",
    key_prefix="table",
)
casos_tabla = filtered_cases(
    casos,
    nivel=table_filters["nivel"],
    partido=table_filters["partido_principal"],
    conducta=table_filters["conducta_principal"],
    sentido=table_filters["sentido"],
)
table_ids = set(casos_tabla["caso_id"].astype(str)) if not casos_tabla.empty else set()
sanciones_tabla = sanciones[sanciones["caso_id"].astype(str).isin(table_ids)] if table_ids and not sanciones.empty else sanciones.head(0)
st.markdown(expedient_table_html(casos_tabla, sanciones_tabla), unsafe_allow_html=True)
st.download_button("Descargar CSV filtrado", casos_tabla.to_csv(index=False).encode("utf-8"), "casos_filtrados.csv", "text/csv")

st.markdown(
    """
    <section class="executive-reading">
      <div class="section-subhead">Lectura ejecutiva</div>
      <p>
        <strong>El observatorio se concentra en diputaciones federales 2024:</strong>
        distingue sentencias de fondo, revocaciones para efectos, sobreseimientos y asuntos
        de queja en materia de fiscalización, sin presentar el corpus como universo exhaustivo.
      </p>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="methodology-band">
      <div class="home-section-head">
        <div>
          <div class="label">Cierre metodológico</div>
          <div class="title">Relevancia, método y referencias</div>
        </div>
        <div class="body">
          El análisis permite reconstruir la relación entre conducta observada, sujeto obligado,
          monto controvertido, efecto jurisdiccional y criterio aplicable al proceso electoral
          federal 2023-2024.
        </div>
      </div>
      <div class="methodology-grid">
        <article>
          <span class="methodology-index">I</span>
          <b>Relevancia del análisis</b>
          <p>Ofrece una lectura institucional de sanciones, agravios y criterios para consulta pública, archivo, seguimiento de efectos y revisión de dictámenes o resoluciones posteriores. Permite distinguir montos observados, montos firmes, asuntos pendientes y casos sin estudio de fondo.</p>
        </article>
        <article>
          <span class="methodology-index">II</span>
          <b>Metodología</b>
          <p>Se delimitó el corte a diputaciones federales; se normalizaron expedientes, sujetos, conductas, montos, agravios y sentido de resolución; y se contrastaron registros de sanción con sentencias oficiales, fichas de criterios y bases documentales del observatorio.</p>
        </article>
        <article>
          <span class="methodology-index">III</span>
          <b>Referencias</b>
          <p>Las referencias principales son las sentencias oficiales del TEPJF enlazadas en la tabla y el mapa, los registros de fiscalización del INE, la información pública de integración de la Cámara de Diputados y los documentos editoriales descargables.</p>
        </article>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <span class="home-panel-anchor" id="sistematizacion"></span>
    <section class="systematization-band">
      <div class="systematization-head">
        <div>
          <div class="label">Propuesta para futuras actualizaciones</div>
          <div class="title">Sistematización del flujo</div>
        </div>
        <p>
          Para futuras actualizaciones conviene sostener una matriz única por expediente:
          acto de origen, sujeto obligado, conducta, monto observado, monto final, efecto
          jurisdiccional, criterio aplicable, entidad y enlace oficial verificable.
        </p>
      </div>
      <ol class="systematization-flow" aria-label="Etapas de sistematización">
        <li><b>01</b><span>Capturar expediente y fuente oficial.</span></li>
        <li><b>02</b><span>Normalizar sujeto, conducta, monto y sentido.</span></li>
        <li><b>03</b><span>Vincular criterio, efecto y entidad territorial.</span></li>
        <li><b>04</b><span>Validar montos firmes, pendientes o no aplicables.</span></li>
        <li><b>05</b><span>Publicar PDF, datos y ficha navegable.</span></li>
      </ol>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <span class="home-panel-anchor" id="descargas"></span>
    <section class="home-download-band final-download">
      <div class="home-section-head">
        <div>
          <div class="label">Descargas editoriales</div>
          <div class="title">Conserva el análisis</div>
        </div>
        <div class="body">
          Los documentos descargables reúnen la síntesis editorial y las fichas de criterios para
          consulta, archivo y cita posterior.
        </div>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

download_left, download_right = st.columns([.72, .28])
selected_pdf = download_left.selectbox(
    "Análisis disponible",
    list(pdf_options),
    key="home_pdf_analysis_download_final",
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

install_scroll_motion()
