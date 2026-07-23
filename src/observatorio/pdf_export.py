from __future__ import annotations

import html
import json
import re
from pathlib import Path

import pandas as pd

from .paths import export_dir, project_root


REPORT_HTML = "diputaciones_electas_reporte.html"
REPORT_PDF = "diputaciones_electas_reporte.pdf"
REPORT_SCREENSHOT = "captura_diputaciones_pdf.png"

SOURCE_FILES = [
    "data/analysis/diputados_lxvi_electos.csv",
    "data/analysis/tepjf_corpus_resumen.csv",
    "data/processed/sanciones.csv",
    "data/processed/casos.csv",
    "data/processed/hallazgos_portal.csv",
    "data/geo/mexico_states_inegi_svg_paths.json",
    "data/interim/tepjf_diputaciones_2023_2025_exhaustive_manifest.csv",
    "exports/tepjf_bitacora_descarga_exhaustiva_resumen.csv",
]


STATE_POINTS = {
    "Ciudad de Mexico": (19.43, -99.13),
    "Ciudad de México": (19.43, -99.13),
    "Chihuahua": (28.63, -106.07),
    "Michoacan": (19.70, -101.19),
    "Michoacán": (19.70, -101.19),
}


PALETTE = {
    "MORENA": "#6B1531",
    "PVEM": "#1E5B4F",
    "PT": "#C59A3D",
    "PAN": "#2B5C8A",
    "PRI": "#8A1F2D",
    "MC": "#FF6600",
}


def money(value: float | int | str) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        number = 0
    if number >= 1_000_000:
        return f"${number / 1_000_000:.1f} M"
    return f"${number:,.0f}"


def money_exact(value: float | int | str) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        number = 0
    return f"${number:,.2f}"


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
        "campana": "campaña",
        "diputacion": "diputación",
        "resolucion": "resolución",
        "fiscalizacion": "fiscalización",
    }
    text = str(value)
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def state_display(value: str) -> str:
    replacements = {
        "Ciudad de Mexico": "Ciudad de México",
        "Michoacan": "Michoacán",
        "Representacion proporcional": "Representación proporcional",
    }
    return replacements.get(str(value), str(value))


def _read_csv(relative_path: str) -> pd.DataFrame:
    return pd.read_csv(project_root() / relative_path, keep_default_na=False)


def _tag(value: str, class_name: str = "tag") -> str:
    return f'<span class="{class_name}">{html.escape(str(value))}</span>'


def _safe(value: object) -> str:
    return html.escape(str(value))


def _plural(count: int, singular: str, plural: str | None = None) -> str:
    return singular if count == 1 else (plural or f"{singular}s")


def _case_conduct_summary(row: pd.Series, sanctions: pd.DataFrame) -> str:
    case_sanctions = sanctions[sanctions["caso_id"].eq(row["caso_id"])].copy()
    subjects = sorted({text_label(value) for value in case_sanctions["sujeto_nombre"].astype(str) if value})
    conductas = sorted({text_label(value) for value in case_sanctions["conducta"].astype(str) if value})
    subject_text = "; ".join(subjects[:3]) or text_label(row["partido_principal"])
    if len(subjects) > 3:
        subject_text += f"; y {len(subjects) - 3} más"
    conduct_text = "; ".join(conductas[:4]) or text_label(row["conducta_principal"])
    if len(conductas) > 4:
        conduct_text += f"; y {len(conductas) - 4} más"
    candidate = str(row.get("persona_candidata", "")).strip()
    candidate_text = f", con referencia a la candidatura de {text_label(candidate)}" if candidate and candidate.lower() != "nan" else ""
    return (
        f"El expediente revisa conductas atribuidas a {subject_text}, identificado en el registro como "
        f"{text_label(row['partido_principal'])}{candidate_text}. La controversia se concentró en "
        f"{conduct_text}. El TEPJF resolvió en sentido de {text_label(row['sentido'])} y estableció como "
        f"efecto principal: {text_label(row['efectos_resumen'])}."
    )


def _incidence_detail_summary(row: pd.Series) -> str:
    return (
        f"La sentencia de {row['fecha']} vincula a {text_label(row['candidatura'])}, de "
        f"{text_label(row['partido_o_coalicion'])}, con {text_label(row['tema'])}. "
        f"El asunto se tramitó por vía {row['tipo_medio']} ante {row['organo']} y se incorporó al corte "
        f"por su relación con {text_label(row['razon_prioridad']).lower()}."
    )


REPORT_FOOTER = "Observatorio de Fiscalización Electoral - Proceso Federal 2023-2024 · Corte: 23 de julio de 2026"
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


def _exp_key(value: str) -> str:
    text = str(value).upper().replace("/", "-")
    text = text.replace(" Y ACUMULADO", "").replace(" Y ACUMULADOS", "")
    match = re.search(r"([A-Z]+-[A-Z]+-\d{1,4}-\d{4}(?:-ACUERDO\d+)?)", text)
    if not match:
        return text.strip()
    parts = match.group(1).split("-")
    if len(parts) >= 4 and parts[2].isdigit():
        parts[2] = str(int(parts[2]))
    return "-".join(parts)


def _case_location(row: pd.Series, hallazgo_lookup: dict[str, tuple[str, str]]) -> tuple[str, str]:
    if row["caso_id"] in CASE_LOCATION_OVERRIDES:
        return CASE_LOCATION_OVERRIDES[row["caso_id"]]
    return hallazgo_lookup.get(_exp_key(row["expediente"]), ("Sin entidad estatal", "Alcance nacional"))


def _display_entity_and_scope(entidad: str, distrito: str) -> tuple[str, str]:
    if entidad in {"Representacion proporcional", "Representación proporcional"}:
        return "Sin entidad estatal", f"Representación proporcional · {text_label(distrito)}"
    if entidad == "Nacional":
        return "Sin entidad estatal", "Alcance nacional"
    return f"Mapa: {state_display(entidad)}", text_label(distrito)


def _hallazgo_row_summary(row: pd.Series) -> str:
    return _incidence_detail_summary(row)


def _chunks(values: list[str], size: int) -> list[list[str]]:
    return [values[index : index + size] for index in range(0, len(values), size)]


def _map_svg(incidence_counts: pd.DataFrame) -> str:
    map_asset = json.loads((project_root() / "data/geo/mexico_states_inegi_svg_paths.json").read_text(encoding="utf-8"))
    active_counts = {
        str(row["entidad_label"]): int(row["incidencias"]) for _, row in incidence_counts.iterrows()
    }
    official_aliases = {
        "Coahuila de Zaragoza": "Coahuila",
        "México": "México",
        "Michoacán de Ocampo": "Michoacán",
        "Veracruz de Ignacio de la Llave": "Veracruz",
    }
    state_shapes = []
    labels = []
    for state in map_asset["states"]:
        official_name = state["name"]
        display_name = official_aliases.get(official_name, official_name)
        count = active_counts.get(display_name, 0)
        active = count > 0
        class_name = "state active" if active else "state"
        state_shapes.append(f'<path class="{class_name}" d="{state["path"]}"><title>{_safe(display_name)}</title></path>')
        if active:
            labels.append(
                '<div class="map-note">'
                f'<strong>{_safe(display_name)}</strong>'
                f'<span>{count} {_plural(count, "incidencia")}</span>'
                '</div>'
            )
    return (
        '<div class="mexico-map-wrap">'
        f'<svg class="map-svg" viewBox="{map_asset["viewBox"]}" role="img" aria-label="Mapa de México con estados con incidencias en color">'
        '<rect x="0" y="0" width="520" height="330" fill="#fbf7ef"/>'
        f'{"".join(state_shapes)}'
        '</svg>'
        f'<div class="map-notes">{"".join(labels)}</div>'
        '</div>'
    )


def diputaciones_map_svg(incidence_counts: pd.DataFrame) -> str:
    return _map_svg(incidence_counts)


def _legacy_point_map_svg(incidence_counts: pd.DataFrame) -> str:
    min_lat, max_lat = 14.0, 33.0
    min_lon, max_lon = -118.0, -86.0
    width, height = 520, 330
    dots = []
    max_count = max(int(incidence_counts["incidencias"].max()), 1) if not incidence_counts.empty else 1
    for _, row in incidence_counts.iterrows():
        x = (float(row["lon"]) - min_lon) / (max_lon - min_lon) * width
        y = height - (float(row["lat"]) - min_lat) / (max_lat - min_lat) * height
        radius = 12 + (float(row["incidencias"]) / max_count) * 24
        label = _safe(row["entidad_label"])
        count = int(row["incidencias"])
        dots.append(
            f"""
            <g>
              <circle cx="{x:.1f}" cy="{y:.1f}" r="{radius:.1f}" fill="#6B1531" fill-opacity=".18"/>
              <circle cx="{x:.1f}" cy="{y:.1f}" r="{max(radius * .42, 7):.1f}" fill="#6B1531"/>
              <text x="{x + radius + 8:.1f}" y="{y - 3:.1f}" class="map-label">{label}</text>
              <text x="{x + radius + 8:.1f}" y="{y + 13:.1f}" class="map-meta">{count} {_plural(count, "incidencia")}</text>
            </g>
            """
        )
    return f"""
    <svg class="map-svg" viewBox="0 0 {width} {height}" role="img" aria-label="Mapa de incidencias por entidad">
      <rect x="0" y="0" width="{width}" height="{height}" fill="#fbf7ef"/>
      <path d="M74 56 L170 32 L282 72 L397 118 L466 203 L421 285 L302 286 L210 245 L122 260 L54 188 Z"
            fill="#efe4d3" stroke="#211816" stroke-width="1.1" stroke-opacity=".38"/>
      <path d="M307 96 L362 115 L420 178 L395 196 L336 174 Z" fill="#e6d7bf" stroke="#211816" stroke-opacity=".22"/>
      <path d="M118 265 L164 286 L244 296 L221 317 L138 309 Z" fill="#e6d7bf" stroke="#211816" stroke-opacity=".18"/>
      {''.join(dots)}
    </svg>
    """


def build_diputaciones_report_html() -> str:
    root = project_root()
    diputados = _read_csv("data/analysis/diputados_lxvi_electos.csv")
    resumen = _read_csv("data/analysis/tepjf_corpus_resumen.csv")
    sanciones = _read_csv("data/processed/sanciones.csv")
    casos = _read_csv("data/processed/casos.csv")
    hallazgos = _read_csv("data/processed/hallazgos_portal.csv")
    audit_path = root / "data/interim/tepjf_diputaciones_2023_2025_exhaustive_manifest.csv"
    audit = pd.read_csv(audit_path) if audit_path.exists() else pd.DataFrame()
    audit_total = len(audit)
    audit_downloaded = int(audit["status"].astype(str).str.startswith("descargado").sum()) if not audit.empty else 0
    audit_pending = audit_total - audit_downloaded

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
    casos_vinculados["sanciones"] = casos_vinculados["sanciones"].fillna(0)

    party_counts = diputados.groupby("partido_estimado", as_index=False).size().rename(columns={"size": "diputaciones"})
    party_counts = party_counts.sort_values("diputaciones", ascending=False)
    party_lookup = dict(zip(party_counts["partido_estimado"], party_counts["diputaciones"]))
    bloque_morena = sum(party_lookup.get(x, 0) for x in ["MORENA", "PVEM", "PT"])
    bloque_pan_pri = sum(party_lookup.get(x, 0) for x in ["PAN", "PRI"])

    incidencias_estatales = hallazgos[hallazgos["entidad"].isin(STATE_POINTS)].copy()
    incidencias_estatales["entidad_label"] = incidencias_estatales["entidad"].map(state_display)
    incidence_counts = (
        incidencias_estatales.groupby(["entidad", "entidad_label"], as_index=False)
        .agg(incidencias=("expediente", "count"), expedientes=("expediente", lambda values: ", ".join(values)))
        .sort_values("incidencias", ascending=False)
    )
    incidence_counts["lat"] = incidence_counts["entidad"].map(lambda value: STATE_POINTS.get(value, (None, None))[0])
    incidence_counts["lon"] = incidence_counts["entidad"].map(lambda value: STATE_POINTS.get(value, (None, None))[1])
    incidencias_nacionales = len(hallazgos) - len(incidencias_estatales)

    max_party = max(int(party_counts["diputaciones"].max()), 1)
    party_rows = []
    for _, row in party_counts.iterrows():
        width = int((int(row["diputaciones"]) / max_party) * 100)
        color = PALETTE.get(str(row["partido_estimado"]), "#31363b")
        party_rows.append(
            f"""
            <div class="party-row">
              <div class="party">{_safe(row["partido_estimado"])}</div>
              <div class="bar"><span style="width:{width}%; background:{color}"></span></div>
              <div class="value">{int(row["diputaciones"])}</div>
            </div>
            """
        )

    cause_rows = []
    max_cause = max(float(top_causas["monto"].max()), 1)
    for _, row in top_causas.iterrows():
        width = int((float(row["monto"]) / max_cause) * 100)
        cause_rows.append(
            f"""
            <div class="cause-row">
              <div>
                <strong>{_safe(text_label(row["conducta"]))}</strong>
                <span>{int(row["registros"])} {_plural(int(row["registros"]), "registro")} del INE</span>
              </div>
              <div class="cause-bar"><i style="width:{width}%"></i></div>
              <b>{money(row["monto"])}</b>
            </div>
            """
        )

    hallazgo_lookup = {
        _exp_key(row["expediente"]): (row["entidad"], row["distrito"])
        for _, row in hallazgos.iterrows()
    }
    consultable_records = []
    seen_urls = set()
    seen_exps = set()
    for _, row in casos_vinculados.iterrows():
        entidad, distrito = _case_location(row, hallazgo_lookup)
        url = str(row["url_sentencia"])
        seen_urls.add(url)
        seen_exps.add(_exp_key(row["expediente"]))
        monto_observado = float(row["monto_observado"])
        sancion_count = int(row["sanciones"])
        if monto_observado > 0:
            monto_label = money_exact(monto_observado)
            monto_note = f'Observado por el INE · {sancion_count} {_plural(sancion_count, "registro")} {_plural(sancion_count, "monetario")}'
            row_summary = _case_conduct_summary(row, sanciones)
        else:
            monto_label = "$0.00"
            monto_note = "No se suma: no hay cantidad económica."
            row_summary = (
                _case_conduct_summary(row, sanciones)
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
                "entidad": entidad,
                "distrito": distrito,
                "resumen": row_summary,
                "monto": monto_label,
                "monto_nota": monto_note,
                "url": url,
            }
        )
    for _, row in hallazgos.iterrows():
        url = str(row["url_oficial"])
        exp_key = _exp_key(row["expediente"])
        if url in seen_urls or exp_key in seen_exps:
            continue
        consultable_records.append(
            {
                "expediente": row["expediente"],
                "fecha": row["fecha"],
                "sala": row["organo"],
                "entidad": row["entidad"],
                "distrito": row["distrito"],
                "resumen": _hallazgo_row_summary(row) + " El caso aparece en el mapa porque permite ubicar una controversia vinculada con esa entidad o distrito. No se integra monto porque este registro no contiene una cantidad económica positiva que pueda agregarse al cálculo.",
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

    case_rows = []
    for row in consultable_records:
        display_entidad, display_distrito = _display_entity_and_scope(row["entidad"], row["distrito"])
        case_rows.append(
            f"""
            <tr>
              <td><strong>{_safe(row["expediente"])}</strong><br><span>{_safe(row["fecha"])} · {_safe(row["sala"])}</span></td>
              <td>{_safe(display_entidad)}</td>
              <td>{_safe(display_distrito)}</td>
              <td>{_safe(row["resumen"])}</td>
              <td>{_safe(row["monto"])}<br><span>{_safe(row["monto_nota"])}</span></td>
              <td><a href="{_safe(row["url"])}">{_safe(row["url"])}</a></td>
            </tr>
            """
        )
    case_row_pages = _chunks(case_rows, 4)
    total_pages = len(case_row_pages) + 6
    summary_page_number = 3
    map_page_number = 4
    cases_start_page = 5
    cases_end_page = cases_start_page + len(case_row_pages) - 1
    model_page_number = cases_end_page + 1
    sources_page_number = total_pages
    cases_page_label = (
        str(cases_start_page)
        if cases_start_page == cases_end_page
        else f"{cases_start_page}-{cases_end_page}"
    )
    case_sections = []
    for index, rows in enumerate(case_row_pages, start=1):
        page_number = index + 4
        amount_note = ""
        if index == len(case_row_pages):
            amount_note = f"""
    <div class="method-note">
      <strong>Procedencia de cifras</strong>
      <p>La búsqueda en el portal del TEPJF delimitó 52 sentencias revisadas; de ellas se seleccionaron 7 expedientes base por su relación directa con fiscalización de diputaciones federales.</p>
      <div class="method-grid">
        <div><b>{money_exact(total_sancionado)}</b><span>Suma exacta de 15 registros monetarios originalmente observados por el INE en cuatro sentencias. En portada se abrevia como {money(total_sancionado)}.</span></div>
        <div><b>Sentencias que alimentan el monto</b><span>SUP-RAP-342/2024: Movimiento Ciudadano, $7,303,754.15. SUP-RAP-352/2024: PAN, $10,312,470.58. SUP-RAP-357/2024: PT, $2,638,887.56. SUP-RAP-413/2024: Morena, $445,361.30.</span></div>
        <div><b>Causas principales</b><span>Agrupan esos 15 registros por conducta y suman el monto original observado por el INE.</span></div>
        <div><b>Qué no se añade a la sumatoria</b><span>{registros_no_cuantificados} registros aparecen en el mapa o en la tabla porque son expedientes localizados por entidad, distrito o conducta. No se agregan a los {money_exact(total_sancionado)} porque el total no cuenta expedientes: cuenta únicamente cantidades económicas positivas observadas en registros de sanción. Cuando un expediente está en $0.00 o no integrado, se informa como caso consultable, pero no modifica la suma de pesos porque no hay monto que agregar. El monto firme de {money(total_firme)} suma solo registros con monto_final firme.</span></div>
      </div>
    </div>
            """
        case_sections.append(
            f"""
  <section class="page">
    <div class="top-rule"></div>
    <h2>Expedientes consultables{f' · {index}' if len(case_row_pages) > 1 else ''}</h2>
    <table>
      <thead><tr><th style="width:15%">Expediente</th><th style="width:10%">Entidad mapa</th><th style="width:11%">Distrito/ámbito</th><th style="width:34%">Conducta y efectos</th><th style="width:10%">Monto observado por el INE</th><th style="width:20%">URL oficial</th></tr></thead>
      <tbody>{''.join(rows)}</tbody>
    </table>
    {amount_note}
    <div class="footer"><span>{REPORT_FOOTER}</span><span>Página {page_number} de {total_pages}</span></div>
  </section>
            """
        )

    incidence_items = []
    for _, entity_label in MAP_ENTITY_COLUMNS:
        entity_rows = incidencias_estatales[incidencias_estatales["entidad_label"].eq(entity_label)].sort_values(["fecha", "expediente"])
        count = len(entity_rows)
        entry_items = []
        for _, row in entity_rows.iterrows():
            entry_items.append(
                f"""
                <div class="incidence-entry">
                  <b>{_safe(row["expediente"])} · {_safe(text_label(row["distrito"]))}</b>
                  <em>{_safe(_incidence_detail_summary(row))}</em>
                </div>
                """
            )
        incidence_items.append(
            f"""
            <div class="incidence-card">
              <strong>{_safe(entity_label)}</strong>
              <span>{REPORT_CUT_LABEL} · {count} {_plural(count, "expediente")}</span>
              {''.join(entry_items)}
            </div>
            """
        )

    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Observatorio de Fiscalización Electoral | Diputaciones electas</title>
<style>
@page {{ size: letter landscape; margin: 0; }}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  background: #fff;
  color: #211816;
  font-family: Montserrat, Avenir, Helvetica, Arial, sans-serif;
}}
.page {{
  width: 11in;
  height: 8.5in;
  padding: .38in .42in;
  page-break-after: always;
  overflow: hidden;
  position: relative;
}}
.page:last-child {{ page-break-after: auto; }}
.top-rule {{ height: 7px; background: linear-gradient(90deg, #6B1531 0 38%, #C59A3D 38% 46%, #14100d 46%); margin-bottom: 18px; }}
.kicker, .section-kicker {{ color: #6B1531; font-size: 10px; font-weight: 900; text-transform: uppercase; }}
.kicker {{ margin-bottom: 18px; }}
h1 {{ margin: 0 0 12px; font-size: 51px; line-height: .92; text-transform: uppercase; letter-spacing: 0; max-width: 7.3in; }}
h2 {{ margin: 0 0 13px; border-top: 6px solid #14100d; padding-top: 10px; font-size: 23px; line-height: 1; text-transform: uppercase; }}
p {{ margin: 0; color: #665a52; font-size: 13px; line-height: 1.45; font-weight: 600; }}
.cover-page {{ background: #fffdf8; padding: .46in .52in; }}
.cover-rule {{ height: 9px; background: linear-gradient(90deg, #6B1531 0 44%, #C59A3D 44% 54%, #1E5B4F 54% 68%, #14100d 68%); margin-bottom: 34px; }}
.cover-layout {{ display: grid; grid-template-columns: 1.08fr .92fr; gap: 38px; min-height: 6.35in; align-items: end; }}
.cover-kicker {{ color: #6B1531; font-size: 12px; font-weight: 900; text-transform: uppercase; margin-bottom: 18px; }}
.cover-title {{ color: #14100d; font-size: 58px; line-height: .88; font-weight: 900; text-transform: uppercase; max-width: 6.4in; }}
.cover-subtitle {{ margin-top: 22px; max-width: 5.2in; color: #665a52; font-size: 15px; line-height: 1.42; font-weight: 700; }}
.cover-meta {{ border-top: 5px solid #14100d; padding-top: 14px; }}
.cover-meta strong {{ display: block; color: #3b0718; font-size: 14px; line-height: 1.1; text-transform: uppercase; }}
.cover-meta p {{ margin-top: 8px; font-size: 10.5px; line-height: 1.36; }}
.cover-stats {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin-top: 28px; }}
.cover-stat {{ border-top: 4px solid #C59A3D; padding-top: 10px; min-height: 74px; }}
.cover-stat:nth-child(2), .cover-stat:nth-child(4) {{ border-color: #6B1531; }}
.cover-stat b {{ display: block; color: #3b0718; font-size: 29px; line-height: .9; }}
.cover-stat span {{ display: block; margin-top: 8px; color: #665a52; font-size: 8.8px; font-weight: 900; line-height: 1.16; text-transform: uppercase; }}
.toc-layout {{ display: grid; grid-template-columns: .82fr 1.18fr; gap: 32px; align-items: start; }}
.toc-title {{ color: #14100d; font-size: 49px; font-weight: 900; line-height: .9; text-transform: uppercase; margin-top: 6px; }}
.toc-copy {{ margin-top: 16px; font-size: 12px; line-height: 1.42; }}
.toc-list {{ border-top: 6px solid #14100d; }}
.toc-item {{ display: grid; grid-template-columns: 54px 1fr 60px; gap: 14px; align-items: start; border-bottom: 1px solid rgba(20,16,13,.24); padding: 14px 0; }}
.toc-item b {{ color: #6B1531; font-size: 18px; line-height: 1; }}
.toc-item strong {{ display: block; color: #3b0718; font-size: 15px; line-height: 1.08; text-transform: uppercase; }}
.toc-item span {{ display: block; margin-top: 4px; color: #665a52; font-size: 9.5px; font-weight: 700; line-height: 1.26; }}
.toc-page {{ color: #14100d; font-size: 17px; font-weight: 900; text-align: right; }}
.reading-note {{ margin-top: 28px; border-top: 4px solid #C59A3D; padding-top: 11px; }}
.reading-note strong {{ display: block; color: #3b0718; font-size: 12px; text-transform: uppercase; }}
.reading-note p {{ margin-top: 7px; font-size: 10.2px; line-height: 1.34; }}
.hero-grid {{ display: grid; grid-template-columns: 1.18fr .82fr; gap: 32px; align-items: end; }}
.hero-copy {{ max-width: 3.3in; font-size: 17px; }}
.metric-board {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; margin-top: 28px; border-top: 6px solid #14100d; padding-top: 16px; }}
.metric {{ border-left: 6px solid #6B1531; padding-left: 12px; min-height: 92px; }}
.metric:nth-child(2) {{ border-color: #C59A3D; }}
.metric:nth-child(3) {{ border-color: #1E5B4F; }}
.metric strong {{ display: block; color: #3b0718; font-size: 36px; line-height: .9; font-weight: 900; }}
.metric span {{ display: block; margin-top: 8px; color: #665a52; font-size: 10px; font-weight: 900; text-transform: uppercase; line-height: 1.12; }}
.split {{ display: grid; grid-template-columns: 1fr 1fr; gap: 26px; }}
.cause-row {{ display: grid; grid-template-columns: 1.4fr 1fr .65fr; gap: 12px; align-items: center; border-top: 1px solid rgba(20,16,13,.2); padding: 7px 0; }}
.cause-row strong {{ display: block; font-size: 10.2px; text-transform: uppercase; line-height: 1.12; }}
.cause-row span, td span {{ color: #665a52; font-size: 9px; font-weight: 700; }}
.cause-row b {{ color: #3b0718; font-size: 16px; text-align: right; }}
.cause-bar {{ height: 11px; background: #e8d9c4; }}
.cause-bar i {{ display: block; height: 100%; background: #6B1531; }}
.method-note {{ border-top: 4px solid #14100d; border-bottom: 1px solid rgba(20,16,13,.22); padding: 8px 0 9px; margin: 11px 0 0; }}
.method-note strong {{ display: block; color: #3b0718; font-size: 9px; font-weight: 900; text-transform: uppercase; margin-bottom: 4px; }}
.method-note p {{ color: #665a52; font-size: 7.7px; font-weight: 650; line-height: 1.22; margin: 0 0 6px; }}
.method-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 9px 18px; }}
.method-grid div {{ border-top: 2px solid #C59A3D; padding-top: 5px; }}
.method-grid b {{ display: block; color: #3b0718; font-size: 8.1px; line-height: 1.15; }}
.method-grid span {{ display: block; color: #665a52; font-size: 7.4px; font-weight: 650; line-height: 1.22; margin-top: 3px; }}
.party-row {{ display: grid; grid-template-columns: 58px 1fr 36px; gap: 10px; align-items: center; margin: 8px 0; }}
.party {{ font-size: 11px; font-weight: 900; }}
.bar {{ height: 12px; background: #e8d9c4; }}
.bar span {{ display: block; height: 100%; }}
.value {{ color: #3b0718; font-weight: 900; text-align: right; }}
.map-layout {{ display: grid; grid-template-columns: .78fr 1.22fr; gap: 28px; }}
.mexico-map-wrap {{ position: relative; border-top: 4px solid #6B1531; border-bottom: 1px solid rgba(20,16,13,.25); background: #fbf7ef; }}
.map-svg {{ width: 100%; height: 332px; display: block; }}
.state {{ fill: #e8ddcc; stroke: #fffdf8; stroke-width: 2.2; vector-effect: non-scaling-stroke; }}
.state.active {{ fill: #6B1531; stroke: #fffdf8; }}
.map-notes {{ position: absolute; right: 16px; top: 18px; display: grid; gap: 7px; width: 154px; }}
.map-note {{ background: rgba(255,253,248,.88); border-left: 4px solid #6B1531; padding: 6px 8px; }}
.map-note strong {{ display: block; color: #3b0718; font-size: 10px; text-transform: uppercase; }}
.map-note span {{ display: block; color: #665a52; font-size: 8px; font-weight: 900; text-transform: uppercase; margin-top: 2px; }}
.map-label {{ font: 900 12px Montserrat, Arial, sans-serif; fill: #211816; }}
.map-meta {{ font: 700 9px Montserrat, Arial, sans-serif; fill: #665a52; }}
.tag-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 18px; }}
.tag {{ display: block; border-top: 4px solid #C59A3D; padding-top: 8px; color: #665a52; font-size: 9px; font-weight: 900; text-transform: uppercase; }}
.tag b {{ display: block; color: #3b0718; font-size: 30px; line-height: .9; margin-bottom: 6px; }}
.meeting-lede {{ display: grid; grid-template-columns: .76fr 1.24fr; gap: 28px; align-items: start; margin-top: 4px; }}
.meeting-lede .label {{ color: #6B1531; font-size: 10px; font-weight: 900; text-transform: uppercase; }}
.meeting-lede .title {{ color: #14100d; font-size: 39px; font-weight: 900; line-height: .9; text-transform: uppercase; margin-top: 8px; }}
.meeting-lede p {{ font-size: 12px; line-height: 1.42; margin-top: 10px; }}
.meeting-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 26px; }}
.meeting-card {{ border-top: 5px solid #C59A3D; padding-top: 10px; min-height: 154px; }}
.meeting-card strong {{ display: block; color: #3b0718; font-size: 13px; line-height: 1.12; text-transform: uppercase; }}
.meeting-card p {{ margin-top: 8px; font-size: 10.2px; line-height: 1.36; }}
.flow-grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin-top: 28px; }}
.flow-grid span {{ border: 1px solid #d7c7b2; border-top: 4px solid #6B1531; padding: 11px 9px; color: #3b0718; font-size: 10px; font-weight: 900; text-transform: uppercase; text-align: center; min-height: 48px; }}
.criteria-strip {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 13px; margin-top: 24px; }}
.criteria-strip div {{ border-top: 1px solid rgba(20,16,13,.28); padding-top: 8px; }}
.criteria-strip b {{ display: block; color: #3b0718; font-size: 20px; line-height: .95; }}
.criteria-strip span {{ display: block; margin-top: 5px; color: #665a52; font-size: 9px; font-weight: 900; text-transform: uppercase; line-height: 1.12; }}
.incidence-list {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 14px; }}
.incidence-card {{ border-top: 1px solid rgba(20,16,13,.23); padding-top: 8px; min-height: 170px; }}
.incidence-card strong {{ display: block; color: #3b0718; font-size: 11px; text-transform: uppercase; }}
.incidence-card span {{ display: block; margin: 4px 0; font-size: 9px; font-weight: 900; }}
.incidence-entry {{ margin-top: 8px; }}
.incidence-entry b {{ display: block; color: #211816; font-size: 8.4px; line-height: 1.15; }}
.incidence-entry em {{ display: block; color: #665a52; font-size: 7.7px; font-style: normal; font-weight: 650; line-height: 1.2; margin-top: 3px; }}
table {{ width: 100%; border-collapse: collapse; table-layout: fixed; }}
th {{ border-top: 5px solid #14100d; border-bottom: 1px solid #211816; padding: 8px 6px; color: #6B1531; font-size: 9px; text-align: left; text-transform: uppercase; }}
td {{ border-bottom: 1px solid rgba(20,16,13,.18); padding: 7px 6px; vertical-align: top; font-size: 8.1px; line-height: 1.22; word-break: break-word; }}
td strong {{ color: #3b0718; }}
a {{ color: #6B1531; font-weight: 900; text-decoration: none; }}
.sources {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 18px; }}
.source-box {{ border-top: 4px solid #C59A3D; padding-top: 10px; }}
.source-box.full {{ grid-column: 1 / -1; }}
.source-box strong {{ color: #3b0718; font-size: 12px; text-transform: uppercase; }}
.source-box p {{ margin-top: 7px; font-size: 10px; }}
.apa-list {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px 18px; margin-top: 10px; }}
.apa-item {{ font-size: 8.4px; line-height: 1.28; color: #3d342e; }}
.apa-item strong {{ display: inline; font-size: 8.4px; text-transform: none; }}
.footer {{ position: absolute; left: .42in; right: .42in; bottom: .24in; display: flex; justify-content: space-between; border-top: 1px solid rgba(20,16,13,.28); padding-top: 7px; color: #665a52; font-size: 8px; font-weight: 800; text-transform: uppercase; }}
</style>
</head>
<body>
  <section class="page cover-page">
    <div class="cover-rule"></div>
    <div class="cover-layout">
      <div>
        <div class="cover-kicker">Observatorio de Fiscalización Electoral · Proceso federal 2023-2024</div>
        <div class="cover-title">Fiscalización de diputaciones federales 2024</div>
        <p class="cover-subtitle">Criterios, expedientes y modelo de datos para presentar el corte documental de fiscalización ante mesa de trabajo.</p>
      </div>
      <div>
        <div class="cover-meta">
          <strong>Reporte ejecutivo para reunión</strong>
          <p>Corte documental al 23 de julio de 2026. El reporte separa casos consultables de montos positivos: la sumatoria cuenta pesos observados por el INE, no número de expedientes.</p>
        </div>
        <div class="cover-stats">
          <div class="cover-stat"><b>{len(resumen)}</b><span>sentencias revisadas en el corpus local</span></div>
          <div class="cover-stat"><b>{len(casos)}</b><span>expedientes base con sentencia TEPJF</span></div>
          <div class="cover-stat"><b>{len(sanciones)}</b><span>registros de sanción INE</span></div>
          <div class="cover-stat"><b>{money(total_sancionado)}</b><span>sumatoria de montos positivos observados</span></div>
        </div>
      </div>
    </div>
    <div class="footer"><span>{REPORT_FOOTER}</span><span>Página 1 de {total_pages}</span></div>
  </section>

  <section class="page">
    <div class="top-rule"></div>
    <div class="toc-layout">
      <div>
        <div class="section-kicker">Guía de lectura</div>
        <div class="toc-title">Índice del reporte</div>
        <p class="toc-copy">La primera mitad presenta los hallazgos ejecutivos y la ubicación territorial. La segunda conserva los expedientes consultables, el método y el modelo de organización para actualizar la información desde fuentes oficiales.</p>
        <div class="reading-note">
          <strong>Clave metodológica</strong>
          <p>Los registros en $0.00 o “No integrado” aparecen porque ubican una controversia, pero no se suman cuando no existe una cantidad económica positiva fijada, confirmada o modificada para agregar al cálculo.</p>
        </div>
      </div>
      <div class="toc-list">
        <div class="toc-item"><b>01</b><div><strong>Síntesis ejecutiva</strong><span>Causas por monto observado, contexto legislativo y lectura de la sumatoria.</span></div><div class="toc-page">{summary_page_number}</div></div>
        <div class="toc-item"><b>02</b><div><strong>Mapa de incidencias</strong><span>Entidades y distritos con controversias ubicables en el corte.</span></div><div class="toc-page">{map_page_number}</div></div>
        <div class="toc-item"><b>03</b><div><strong>Expedientes consultables</strong><span>Tabla con expediente, sala, entidad, conducta, monto y URL oficial TEPJF.</span></div><div class="toc-page">{cases_page_label}</div></div>
        <div class="toc-item"><b>04</b><div><strong>Modelo de trabajo</strong><span>Organización propuesta para compilar criterios y alimentar la app en tiempo real.</span></div><div class="toc-page">{model_page_number}</div></div>
        <div class="toc-item"><b>05</b><div><strong>Fuentes y método</strong><span>Corpus, delimitación, referencias oficiales y alcance del corte.</span></div><div class="toc-page">{sources_page_number}</div></div>
      </div>
    </div>
    <div class="footer"><span>{REPORT_FOOTER}</span><span>Página 2 de {total_pages}</span></div>
  </section>

  <section class="page">
    <div class="top-rule"></div>
    <div class="hero-grid">
      <div>
        <div class="kicker">Observatorio de Fiscalización Electoral · Proceso federal 2023-2024</div>
        <h1>Síntesis ejecutiva de diputaciones federales 2024</h1>
      </div>
      <p class="hero-copy">Reporte ejecutivo construido desde expedientes, registros de sanción del INE y hallazgos oficiales. Los {money(total_sancionado)} corresponden a la suma de montos originales observados por el INE en {registros_cuantificados} registros cuantificados relacionados con los expedientes base.</p>
    </div>
    <div class="metric-board">
      <div class="metric"><strong>{len(casos)}</strong><span>expedientes base con sentencia TEPJF</span></div>
      <div class="metric"><strong>{len(sanciones)}</strong><span>registros de sanción del INE</span></div>
      <div class="metric"><strong>{money(total_sancionado)}</strong><span>monto observado por el INE</span></div>
      <div class="metric"><strong>{money(total_firme)}</strong><span>monto firme identificado en este corte</span></div>
    </div>
    <div class="split" style="margin-top:32px;">
      <div>
        <h2>Causas por monto observado por el INE</h2>
        {''.join(cause_rows)}
      </div>
      <div>
        <h2>Contexto legislativo</h2>
        <div class="metric-board" style="grid-template-columns:repeat(2,1fr); margin-top:0; border-top:0; padding-top:0;">
          <div class="metric"><strong>{bloque_morena}</strong><span>curules Morena · PVEM · PT</span></div>
          <div class="metric"><strong>{bloque_pan_pri}</strong><span>curules PAN · PRI</span></div>
        </div>
        <div style="margin-top:16px;">{''.join(party_rows)}</div>
      </div>
    </div>
    <div class="footer"><span>{REPORT_FOOTER}</span><span>Página {summary_page_number} de {total_pages}</span></div>
  </section>

  <section class="page">
    <div class="top-rule"></div>
    <div class="map-layout">
      <div>
        <h2>Mapa de incidencias</h2>
        <p>El mapa muestra México por entidad federativa: todos los estados permanecen en gris editorial y solo las entidades con incidencia territorial identificada aparecen en color guinda.</p>
        <div class="tag-grid">
          <span class="tag"><b>{len(incidencias_estatales)}</b>incidencias estatales</span>
          <span class="tag"><b>{incidence_counts["entidad"].nunique()}</b>entidades marcadas</span>
          <span class="tag"><b>{incidencias_nacionales}</b>alcance nacional o RP</span>
        </div>
      </div>
      <div>{_map_svg(incidence_counts)}</div>
    </div>
    <div class="incidence-list">{''.join(incidence_items)}</div>
    <div class="footer"><span>{REPORT_FOOTER}</span><span>Página {map_page_number} de {total_pages}</span></div>
  </section>

  {''.join(case_sections)}

  <section class="page">
    <div class="top-rule"></div>
    <h2>Modelo de trabajo para fiscalización</h2>
    <div class="meeting-lede">
      <div>
        <div class="label">Prioridad fiscalización · reunión de trabajo</div>
        <div class="title">Del expediente al dato actualizable</div>
      </div>
      <p>La propuesta es convertir el corte actual en una mesa de trabajo permanente: cada hallazgo entra por fuente oficial, se clasifica jurídicamente, se valida contra el dictamen o resolución administrativa y solo después alimenta la app, la sumatoria y el PDF. Así se conserva la diferencia entre controversias localizables y montos positivos que sí pueden agregarse.</p>
    </div>
    <div class="meeting-grid">
      <div class="meeting-card"><strong>1. Dictamen y resolución de diputaciones</strong><p>Compilar los criterios de fiscalización derivados del dictamen y resolución de campaña para diputaciones federales 2024. Punto de partida operativo: INE/CG1928/2024, INE/CG1929/2024 y resoluciones relacionadas con expedientes RAP, quejas de fiscalización y efectos posteriores.</p></div>
      <div class="meeting-card"><strong>2. Criterios de Sala Superior y SCM</strong><p>Separar criterios por órgano jurisdiccional y tipo de asunto: gasto no reportado, soporte documental, propaganda, rebase de tope, aportaciones prohibidas, competencia, confirmación, revocación, modificación y efectos para nueva resolución.</p></div>
      <div class="meeting-card"><strong>3. Organización para datos en tiempo real</strong><p>Usar una matriz viva con expediente, URL oficial, acto de origen, conducta, sujeto obligado, candidatura vinculada, entidad, distrito, monto positivo, estado de validación y efecto de sentencia. La app debe leer esa matriz sin reescribir manualmente el reporte.</p></div>
    </div>
    <div class="flow-grid">
      <span>Fuente oficial</span><span>Extracción de texto</span><span>Validación jurídica</span><span>Matriz normalizada</span><span>App y PDF</span>
    </div>
    <div class="criteria-strip">
      <div><b>{int(resumen["fiscalizacion"].sum())}</b><span>sentencias del corpus con marca de fiscalización</span></div>
      <div><b>{len(casos)}</b><span>expedientes base ligados a registros de sanción</span></div>
      <div><b>{len(incidencias_estatales)}</b><span>incidencias ubicables por entidad o distrito</span></div>
      <div><b>{money_exact(total_sancionado)}</b><span>sumatoria exacta de montos positivos observados</span></div>
    </div>
    <div class="footer"><span>{REPORT_FOOTER}</span><span>Página {model_page_number} de {total_pages}</span></div>
  </section>

  <section class="page">
    <div class="top-rule"></div>
    <h2>Fuentes y método</h2>
    <div class="sources">
      <div class="source-box full"><strong>Procedimiento de búsqueda y delimitación</strong><p>Se realizó una búsqueda documental en el portal de sentencias públicas del Tribunal Electoral del Poder Judicial de la Federación (TEPJF), disponible en la sección de sentencias públicas y en el buscador institucional. La bitácora del corte registra consultas por proceso electoral federal 2023-2024, diputaciones, fiscalización, propaganda, representación proporcional y constancia de mayoría. El corpus base analizado conserva {len(resumen)} sentencias descargadas en versión pública, extraídas a texto local y revisadas por sentido de la resolución, autoridad responsable, cargo de elección y pertinencia temática. Como ampliación, se identificó un universo candidato adicional de {audit_total} expedientes 2023-2025; {audit_downloaded} cuentan con texto descargado o integrado y {audit_pending} permanecen pendientes de descarga completa antes de su incorporación sustantiva.</p></div>
      <div class="source-box"><strong>Corpus TEPJF</strong><p>El corpus validado contiene {len(resumen)} sentencias revisadas: {int(resumen["fiscalizacion"].sum())} incluyen fiscalización, {int(resumen["propaganda"].sum())} abordan propaganda y {int(resumen["constancia_mayoria"].sum())} tratan constancia de mayoría. La matriz de análisis conserva expediente, año, órgano jurisdiccional, medio de impugnación, fragmentos relevantes y marcas temáticas.</p></div>
      <div class="source-box"><strong>Criterios de análisis</strong><p>La revisión clasificó cada resolución según fiscalización, propaganda, representación proporcional, nulidad, inelegibilidad, rebase de tope de gastos y efectos jurídicos. Los {money(total_sancionado)} se obtienen de sumar la columna de monto original de {registros_cuantificados} registros de sanción del INE con importe mayor a cero. Los {registros_no_cuantificados} registros en cero o no integrados se muestran como expedientes consultables porque permiten ubicar una controversia por entidad, distrito o conducta; sin embargo, no se añaden a la sumatoria porque el total no cuenta expedientes, sino pesos. Cuando un registro no tiene una cantidad económica positiva fijada, confirmada o modificada, no hay monto que agregar al cálculo. Las sentencias no siempre reproducen ese acumulado por causa. No se incorporaron inferencias personales ni territoriales si el expediente no las establece expresamente.</p></div>
      <div class="source-box"><strong>Datos legislativos y geográficos</strong><p>La contextualización usa {len(diputados)} diputaciones electas de la LXVI Legislatura y geometría estatal oficial del Marco Geoestadístico de INEGI. El mapa colorea únicamente entidades con incidencia territorial documentada.</p></div>
      <div class="source-box"><strong>Alcance</strong><p>El reporte parte de un corte documental y no sustituye el universo completo de resoluciones administrativas del INE, sentencias del TEPJF ni determinaciones posteriores vinculadas con el proceso electoral federal 2023-2024. La información se presenta como una sistematización analítica de expedientes públicos disponibles, sujeta a actualización conforme se incorporen nuevas versiones oficiales y se concluya la validación jurídica de expedientes relacionados.</p></div>
      <div class="source-box full"><strong>Referencias en formato APA</strong>
        <div class="apa-list">
          <div class="apa-item"><strong>Tribunal Electoral del Poder Judicial de la Federación. (s. f.).</strong> <em>Sentencias públicas</em>. https://www.te.gob.mx/sentenciasHTML/convertir/expediente/</div>
          <div class="apa-item"><strong>Instituto Nacional Electoral. (2024).</strong> <em>Dictámenes consolidados y resoluciones de fiscalización del proceso electoral federal 2023-2024</em>. https://www.ine.mx/</div>
          <div class="apa-item"><strong>Cámara de Diputados. (s. f.).</strong> <em>Sistema de Información Legislativa: LXVI Legislatura</em>. https://sitl.diputados.gob.mx/</div>
          <div class="apa-item"><strong>Instituto Nacional de Estadística y Geografía. (s. f.).</strong> <em>Marco Geoestadístico: entidades federativas, servicio GeoJSON</em>. https://gaia.inegi.org.mx/wscatgeo/v2/geo/mgee/</div>
        </div>
      </div>
    </div>
    <div class="footer"><span>{REPORT_FOOTER}</span><span>Página {sources_page_number} de {total_pages}</span></div>
  </section>
</body>
</html>"""


def export_diputaciones_report_pdf(
    output_pdf: Path | None = None,
    output_html: Path | None = None,
    screenshot_path: Path | None = None,
) -> Path:
    output_dir = export_dir()
    pdf_path = output_pdf or output_dir / REPORT_PDF
    html_path = output_html or output_dir / REPORT_HTML
    shot_path = screenshot_path or output_dir / REPORT_SCREENSHOT
    html_text = build_diputaciones_report_html()
    html_path.write_text(html_text, encoding="utf-8")

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Playwright no está instalado; instala playwright para generar el PDF.") from exc

    browser_candidates = [
        Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
        Path("/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"),
        Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
    ]
    executable_path = next((str(path) for path in browser_candidates if path.exists()), None)

    with sync_playwright() as playwright:
        launch_kwargs = {"headless": True}
        if executable_path:
            launch_kwargs["executable_path"] = executable_path
        browser = playwright.chromium.launch(**launch_kwargs)
        page = browser.new_page(viewport={"width": 1056, "height": 816}, device_scale_factor=1)
        page.set_content(html_text, wait_until="networkidle")
        page.pdf(
            path=str(pdf_path),
            format="Letter",
            landscape=True,
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            prefer_css_page_size=True,
        )
        page.screenshot(path=str(shot_path), full_page=False)
        browser.close()
    return pdf_path


def get_diputaciones_report_pdf_bytes() -> bytes:
    pdf_path = export_dir() / REPORT_PDF
    if pdf_path.exists():
        newest_source = max((project_root() / path).stat().st_mtime for path in SOURCE_FILES)
        if pdf_path.stat().st_mtime >= newest_source:
            return pdf_path.read_bytes()
    pdf_path = export_diputaciones_report_pdf()
    return pdf_path.read_bytes()
