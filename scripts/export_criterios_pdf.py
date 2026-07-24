from __future__ import annotations

import html
import base64
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPORTS = ROOT / "exports"
HTML_PATH = EXPORTS / "criterios_fiscalizacion_diputaciones_2024.html"
PDF_PATH = EXPORTS / "criterios_fiscalizacion_diputaciones_2024.pdf"
SCREENSHOT_PATH = EXPORTS / "captura_criterios_fiscalizacion_p1.png"
FONT_PATH = Path.home() / "Library/Fonts/Montserrat-VariableFont_wght.ttf"

FOOTER = "Observatorio de Fiscalización Electoral - Proceso Federal 2023-2024 · Corte: 23 de julio de 2026"

TEPJF_URLS = {
    "SUP-RAP-342/2024": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-RAP-0342-2024-",
    "SUP-RAP-352/2024": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-RAP-0352-2024-",
    "SUP-RAP-357/2024": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-RAP-0357-2024-",
    "SUP-RAP-413/2024": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-RAP-0413-2024-",
    "SUP-RAP-414/2024": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-RAP-0414-2024-",
    "SUP-RAP-415/2024": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-RAP-0415-2024-",
    "SUP-REC-764/2024": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-REC-0764-2024-",
    "SCM-RAP-47/2024": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SCM-RAP-0047-2024-",
    "SCM-JIN-27/2024": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SCM-JIN-0027-2024-",
    "SCM-JIN-30/2024": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SCM-JIN-0030-2024-",
    "SCM-JIN-56/2024": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SCM-JIN-0056-2024-",
    "SCM-JIN-103/2024": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SCM-JIN-0103-2024-",
}

CRITERIA = [
    {
        "id": "FIS-01",
        "title": "Exhaustividad del dictamen, anexos y conclusiones",
        "theme": "Dictamen y resolución",
        "organ": "Sala Superior / Sala Regional Ciudad de México",
        "source": "SUP-RAP-342/2024; SCM-RAP-47/2024",
        "rule": "La autoridad debe permitir reconstruir la relación entre hallazgo, anexo, conclusión y sanción. Si la motivación no explica el paso del hecho observado a la consecuencia, procede revisar el acto.",
        "relevance": "Ordena que la lectura del dictamen no se reduzca al monto: exige identificar conclusión, soporte y respuesta administrativa.",
        "effect": "Revocación para efectos, revocación parcial o confirmación.",
        "utility": "Antes: diseñar matrices de observaciones. Durante: ubicar el anexo y la conclusión afectados. Después: documentar qué parte quedó firme y qué debe rehacerse.",
    },
    {
        "id": "FIS-02",
        "title": "Fallas del Sistema Integral de Fiscalización",
        "theme": "SIF",
        "organ": "Sala Superior",
        "source": "SUP-RAP-342/2024; SUP-RAP-357/2024; SUP-RAP-413/2024",
        "rule": "La referencia genérica a fallas del SIF no desvirtúa una infracción si no se acredita cómo impidió cumplir una obligación concreta.",
        "relevance": "Sirve para distinguir problemas técnicos documentados de defensas abstractas frente a registros extemporáneos u omisiones.",
        "effect": "Confirmación cuando el agravio es genérico; posible revocación parcial si incide en una conclusión específica.",
        "utility": "Antes: preparar bitácoras técnicas. Durante: conservar evidencia de carga, módulo y operación. Después: vincular la falla con una conclusión concreta.",
    },
    {
        "id": "FIS-03",
        "title": "Documentación soporte y comprobación fiscal",
        "theme": "Comprobación de gasto",
        "organ": "Sala Superior",
        "source": "SUP-RAP-352/2024; SUP-RAP-357/2024",
        "rule": "La falta de soporte fiscal, contractual o contable idóneo puede sostener sanciones si el sujeto obligado no desvirtúa la observación.",
        "relevance": "Da un estándar práctico para revisar facturas, contratos, muestras y correspondencia entre operación, proveedor y campaña.",
        "effect": "Confirmación de conclusiones o sanciones cuando no se acredita el soporte.",
        "utility": "Antes: definir expedientes digitales mínimos. Durante: revisar soporte por operación. Después: depurar registros firmes y pendientes de aclaración.",
    },
    {
        "id": "FIS-04",
        "title": "Comprobantes electrónicos de pago",
        "theme": "CEP, XML y soporte",
        "organ": "Sala Superior",
        "source": "SUP-RAP-352/2024; SUP-RAP-357/2024; SUP-RAP-413/2024",
        "rule": "La defensa sobre comprobantes electrónicos debe individualizar cada operación y explicar por qué no actualiza infracción.",
        "relevance": "Evita revisar los comprobantes como bloques generales y obliga a enlazar documento, póliza, operación y observación.",
        "effect": "Confirmación cuando falta explicación específica.",
        "utility": "Antes: homogeneizar campos de CEP y XML. Durante: revisar correspondencia por póliza. Después: registrar causas de confirmación o revocación.",
    },
    {
        "id": "FIS-05",
        "title": "Registro oportuno y duplicidad de consecuencias",
        "theme": "Registro en tiempo real",
        "organ": "Sala Superior",
        "source": "SUP-RAP-357/2024",
        "rule": "La autoridad debe distinguir registro inexistente, extemporáneo o duplicado, y ajustar la consecuencia a esa diferencia.",
        "relevance": "Permite separar errores de captura, registros tardíos y omisiones reales para evitar consecuencias duplicadas.",
        "effect": "Revocación parcial cuando hay error de individualización; confirmación si la observación subsiste.",
        "utility": "Antes: calendarizar obligaciones. Durante: comparar fecha de operación y registro. Después: identificar recálculos o conclusiones subsistentes.",
    },
    {
        "id": "FIS-06",
        "title": "Prorrateo y candidaturas beneficiadas",
        "theme": "Beneficio electoral",
        "organ": "Sala Superior",
        "source": "SUP-RAP-413/2024",
        "rule": "El prorrateo debe reflejar gasto, propaganda, candidatura beneficiada, ámbito territorial y regla de distribución aplicable.",
        "relevance": "Conecta la cuantificación con el beneficio real de campaña y con el territorio de la diputación federal.",
        "effect": "Revocación parcial o confirmación según la precisión del análisis.",
        "utility": "Antes: definir criterios de beneficio. Durante: codificar piezas por candidatura y distrito. Después: explicar ajustes al monto observado.",
    },
    {
        "id": "FIS-07",
        "title": "Omisión de reportar propaganda, eventos o gastos",
        "theme": "Gasto no reportado",
        "organ": "Sala Superior / Sala Regional Ciudad de México",
        "source": "SUP-RAP-342/2024; SUP-RAP-357/2024; SUP-RAP-413/2024; SCM-RAP-47/2024",
        "rule": "La omisión se analiza por existencia del gasto o propaganda, beneficio electoral, obligación de reporte y suficiencia del soporte.",
        "relevance": "Es el criterio base para ordenar observaciones de propaganda, eventos y gastos que no aparecen en la contabilidad ordinaria.",
        "effect": "Confirmación, revocación para efectos o revocación parcial.",
        "utility": "Antes: crear catálogos de conducta. Durante: vincular evidencia con evento o pieza. Después: separar omisiones firmes de estudios rehechos.",
    },
    {
        "id": "FIS-08",
        "title": "Aportaciones prohibidas",
        "theme": "Quejas de fiscalización",
        "organ": "Sala Regional Ciudad de México",
        "source": "SCM-RAP-47/2024",
        "rule": "La autoridad debe valorar hechos, fuente de aportación, bien o servicio, beneficiario y relación con campaña.",
        "relevance": "Ayuda a construir fichas de queja que separen hecho denunciado, aportante, beneficio y estándar de prueba.",
        "effect": "Revocación para nueva resolución si el estudio administrativo fue insuficiente.",
        "utility": "Antes: definir campos de queja. Durante: documentar aportante, valor y beneficio. Después: controlar cumplimiento de nueva resolución.",
    },
    {
        "id": "FIS-09",
        "title": "Fiscalización y nulidad de elección",
        "theme": "Rebase de tope y determinancia",
        "organ": "Sala Superior / Sala Regional Ciudad de México",
        "source": "SCM-JIN-27/2024; SUP-REC-764/2024; SUP-RAP-352/2024; SUP-RAP-357/2024; SUP-RAP-413/2024",
        "rule": "La sanción administrativa aislada no equivale por sí misma a nulidad; se requiere monto, acumulación al tope, determinancia y vínculo con la elección.",
        "relevance": "Separa la lectura administrativa de fiscalización de la consecuencia jurisdiccional sobre validez de la elección.",
        "effect": "Confirmación de validez o análisis de nulidad sólo si se acredita el impacto exigido.",
        "utility": "Antes: ubicar topes y umbrales. Durante: monitorear acumulación de gastos. Después: distinguir sanción, rebase y nulidad.",
    },
    {
        "id": "FIS-10",
        "title": "Precisión del acto y principio impugnado",
        "theme": "Juicio de inconformidad",
        "organ": "Sala Regional Ciudad de México",
        "source": "SCM-JIN-27/2024; SCM-JIN-30/2024; SCM-JIN-56/2024; SCM-JIN-103/2024",
        "rule": "En diputaciones federales, la impugnación debe leerse conforme al acto, principio, distrito, agravios y viabilidad jurídica del planteamiento.",
        "relevance": "Permite organizar expedientes que mezclan mayoría relativa, representación proporcional, cómputo distrital y nulidad.",
        "effect": "Confirmación, modificación del cómputo, acumulación o estudio delimitado del acto impugnado.",
        "utility": "Antes: preparar fichas por distrito y principio. Durante: revisar escritos y agravios. Después: actualizar cómputos y efectos.",
    },
    {
        "id": "FIS-11",
        "title": "Competencia por cargo, principio y territorio",
        "theme": "Competencia",
        "organ": "Sala Superior",
        "source": "SUP-RAP-414/2024; SUP-RAP-415/2024",
        "rule": "La competencia depende de tipo de elección, principio, cargo, entidad, distrito y vínculo con la candidatura o elección impugnada.",
        "relevance": "Es un control de entrada para evitar mezclar asuntos federales, locales, de candidatura y de cómputo.",
        "effect": "Acuerdos de competencia o remisión a sala regional.",
        "utility": "Antes: etiquetar órgano probable. Durante: verificar cargo y territorio. Después: registrar remisión o reasignación del asunto.",
    },
    {
        "id": "FIS-12",
        "title": "Efectos de revocación",
        "theme": "Efectos",
        "organ": "Sala Superior / Sala Regional Ciudad de México",
        "source": "SUP-RAP-342/2024; SUP-RAP-357/2024; SUP-RAP-413/2024; SCM-RAP-47/2024",
        "rule": "El sentido de una sentencia puede confirmar una parte, revocar otra o exigir un nuevo pronunciamiento de la autoridad.",
        "relevance": "Permite que dictamen, resolución y sentencia queden en una misma cadena editorial sin usar lenguaje técnico innecesario.",
        "effect": "Confirmación parcial, revocación para efectos, recálculo o nueva resolución.",
        "utility": "Antes: prever salidas posibles. Durante: capturar puntos resolutivos. Después: dar seguimiento a recálculos, reposiciones y montos firmes.",
    },
]


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def link_expediente(expediente: str) -> str:
    url = TEPJF_URLS.get(expediente.strip())
    label = esc(expediente.strip())
    if not url:
        return f"<span>{label}</span>"
    return f'<a href="{esc(url)}">{label}</a>'


def link_list(source: str) -> str:
    return "".join(link_expediente(part) for part in source.split(";"))


def card(item: dict[str, str], page: int, total: int) -> str:
    return f"""
    <section class="page criterion-page">
      <div class="top-rule"></div>
      <div class="eyebrow">Fichas de criterio</div>
      <h2>{esc(item["id"])}</h2>
      <article class="criterion-card">
        <header>
          <span>{esc(item["id"])}</span>
          <h3>{esc(item["title"])}</h3>
        </header>
        <dl>
          <dt>Criterio jurídico</dt>
          <dd class="criterion-rule"><em>{esc(item["rule"])}</em></dd>
          <dt>Órgano</dt>
          <dd>{esc(item["organ"])}</dd>
          <dt>Expediente</dt>
          <dd class="links">{link_list(item["source"])}</dd>
          <dt>Tema</dt>
          <dd>{esc(item["theme"])}</dd>
          <dt>Efecto</dt>
          <dd>{esc(item["effect"])}</dd>
          <dt>Relevancia para dictamen/resolución</dt>
          <dd>{esc(item["relevance"])}</dd>
          <dt>Utilidad antes, durante y después</dt>
          <dd>{esc(item["utility"])}</dd>
        </dl>
      </article>
      {footer(page, total)}
    </section>
    """


def footer(page: int, total: int) -> str:
    return f'<footer><span>{esc(FOOTER)}</span><span>Página {page} de {total}</span></footer>'


def build_html() -> str:
    total = 18
    font_face = ""
    if FONT_PATH.exists():
        font_data = base64.b64encode(FONT_PATH.read_bytes()).decode("ascii")
        font_face = f"""
        @font-face {{
          font-family: 'Montserrat';
          src: url('data:font/ttf;base64,{font_data}') format('truetype');
          font-weight: 100 900;
          font-style: normal;
        }}
        """

    matrix_rows = "\n".join(
        f"""
        <tr>
          <td>{esc(item["id"])}</td>
          <td>{esc(item["title"])}</td>
          <td>{esc(item["theme"])}</td>
          <td>{esc(item["organ"])}</td>
          <td>{esc(item["effect"])}</td>
        </tr>
        """
        for item in CRITERIA
    )
    index_rows = [
        ("01", "Metodología y corpus", "3"),
        ("02", "Matriz ejecutiva de criterios", "4"),
        ("03", "Fichas de criterios", "5-16"),
        ("04", "Lectura por órgano y montos", "17"),
        ("05", "Modelo de organización de datos", "18"),
    ]
    index_html = "".join(
        f"<div><b>{num}</b><span>{esc(title)}</span><em>{page}</em></div>"
        for num, title, page in index_rows
    )
    criterion_pages = "\n".join(card(item, page, total) for page, item in enumerate(CRITERIA, start=5))

    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Compilación de criterios de fiscalización electoral - Diputaciones federales 2024</title>
<style>
{font_face}
@page {{ size: letter landscape; margin: 0; }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; background: #fff; color: #211816; font-family: Montserrat, Avenir, Helvetica, Arial, sans-serif; }}
body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.page {{ width: 11in; height: 8.5in; position: relative; overflow: hidden; page-break-after: always; background: #fffdf8; padding: .38in .42in; }}
.page:last-child {{ page-break-after: auto; }}
.top-rule {{ height: 7px; background: linear-gradient(90deg, #6B1531 0 38%, #C59A3D 38% 46%, #1E5B4F 46% 56%, #14100d 56%); margin-bottom: 18px; }}
footer {{ position: absolute; left: .42in; right: .42in; bottom: .24in; display: flex; justify-content: space-between; border-top: 1px solid rgba(20,16,13,.28); padding-top: 7px; color: #665a52; font-size: 8px; font-weight: 800; text-transform: uppercase; }}
.eyebrow {{ color: #6B1531; text-transform: uppercase; font-size: 10px; font-weight: 900; letter-spacing: 0; margin-bottom: 18px; }}
h1, h2, h3, p {{ margin: 0; letter-spacing: 0; }}
h1 {{ color: #14100d; font-size: 58px; line-height: .88; font-weight: 900; text-transform: uppercase; max-width: 6.4in; }}
h2 {{ margin: 0 0 13px; border-top: 6px solid #14100d; padding-top: 10px; color: #14100d; font-size: 23px; line-height: 1; font-weight: 900; text-transform: uppercase; }}
h3 {{ color: #14100d; font-size: 23px; line-height: 1.05; font-weight: 900; text-transform: uppercase; }}
p {{ color: #665a52; font-size: 13px; line-height: 1.45; font-weight: 600; }}
.cover {{ display: grid; grid-template-columns: 1.08fr .92fr; gap: 38px; padding: .46in .52in; }}
.cover .top-rule {{ grid-column: 1 / -1; height: 9px; background: linear-gradient(90deg, #6B1531 0 44%, #C59A3D 44% 54%, #1E5B4F 54% 68%, #14100d 68%); margin-bottom: 34px; }}
.cover-copy {{ align-self: end; padding-bottom: .94in; }}
.cover-copy p {{ margin-top: 22px; max-width: 5.8in; color: #665a52; font-size: 15px; line-height: 1.42; font-weight: 700; }}
.cover-panel {{ align-self: end; padding-bottom: .94in; border-top: 5px solid #14100d; padding-top: 14px; }}
.cover-panel p {{ margin-top: 8px; font-size: 10.5px; line-height: 1.36; font-weight: 700; }}
.stats {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin-top: 28px; }}
.stat {{ border-top: 4px solid #C59A3D; padding-top: 10px; min-height: 74px; }}
.stat:nth-child(2), .stat:nth-child(4) {{ border-color: #6B1531; }}
.stat b {{ display: block; color: #3b0718; font-size: 29px; line-height: .9; font-weight: 900; }}
.stat span {{ display: block; margin-top: 8px; color: #665a52; text-transform: uppercase; font-size: 8.8px; font-weight: 900; line-height: 1.16; }}
.index-grid {{ margin-top: 24px; margin-left: 3.1in; border-top: 6px solid #14100d; }}
.index-grid div {{ display: grid; grid-template-columns: 54px 1fr 60px; gap: 14px; align-items: start; border-bottom: 1px solid rgba(20,16,13,.24); padding: 14px 0; }}
.index-grid b {{ color: #6B1531; font-size: 18px; line-height: 1; }}
.index-grid span {{ color: #3b0718; text-transform: uppercase; font-size: 15px; line-height: 1.08; font-weight: 900; }}
.index-grid em {{ color: #14100d; font-style: normal; font-size: 17px; font-weight: 900; text-align: right; }}
.note {{ position: absolute; left: .42in; bottom: 1.05in; width: 3.45in; border-top: 4px solid #C59A3D; padding-top: 11px; color: #665a52; font-size: 10.2px; font-weight: 700; line-height: 1.34; }}
.note b {{ display: block; color: #3b0718; font-size: 12px; font-weight: 900; text-transform: uppercase; margin-bottom: 7px; }}
.method-copy {{ margin-top: 16px; max-width: 7.9in; color: #665a52; font-size: 12px; line-height: 1.42; font-weight: 700; }}
.metric-strip {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; margin-top: 28px; border-top: 6px solid #14100d; padding-top: 16px; }}
.metric {{ border-left: 6px solid #6B1531; padding-left: 12px; min-height: 82px; }}
.metric:nth-child(2) {{ border-color: #C59A3D; }}
.metric:nth-child(3) {{ border-color: #1E5B4F; }}
.metric b {{ display: block; color: #3b0718; font-size: 34px; line-height: .9; font-weight: 900; }}
.metric span {{ display: block; margin-top: 8px; color: #665a52; text-transform: uppercase; font-size: 9px; font-weight: 900; line-height: 1.12; }}
table {{ width: 100%; border-collapse: collapse; table-layout: fixed; margin-top: 18px; font-size: 8.1px; line-height: 1.22; }}
th {{ border-top: 5px solid #14100d; border-bottom: 1px solid #211816; padding: 8px 6px; color: #6B1531; text-align: left; text-transform: uppercase; font-size: 9px; font-weight: 900; }}
td {{ vertical-align: top; border-bottom: 1px solid rgba(20,16,13,.18); padding: 7px 6px; word-break: break-word; }}
td:first-child {{ color: #3b0718; font-weight: 900; }}
a {{ color: #6B1531; font-weight: 900; text-decoration: none; border-bottom: 1px solid rgba(107,21,49,.45); }}
.matrix table {{ font-size: 7.7px; }}
.criterion-page h2 {{ width: 100%; max-width: none; margin-top: 0; }}
.criterion-card {{ margin-top: 26px; border-top: 5px solid #6B1531; padding-top: 12px; }}
.criterion-card header {{ display: grid; grid-template-columns: .76in 1fr; gap: 28px; align-items: start; margin-bottom: 26px; }}
.criterion-card header span {{ color: #6B1531; font-size: 13px; line-height: 1.12; font-weight: 900; text-transform: uppercase; }}
.criterion-card header h3 {{ font-size: 28px; line-height: 1.02; text-transform: none; font-weight: 800; }}
dl {{ display: grid; grid-template-columns: 2.55in 1fr; column-gap: .42in; row-gap: 15px; margin: 0; }}
dt {{ color: #9B2F4A; text-transform: uppercase; font-size: 10.2px; line-height: 1.16; font-weight: 900; }}
dd {{ margin: 0; color: #3d342e; font-size: 12.4px; line-height: 1.42; font-weight: 600; }}
.criterion-rule em {{ font-style: italic; text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 3px; font-weight: 700; }}
dd.links {{ display: flex; flex-wrap: wrap; gap: 8px 18px; }}
.organ-blocks {{ margin-top: 24px; display: grid; gap: 18px; }}
.organ-block {{ border-top: 5px solid #6B1531; padding-top: 10px; min-height: 88px; }}
.organ-block:nth-child(2) {{ border-color: #C59A3D; }}
.organ-block:nth-child(3) {{ border-color: #1E5B4F; }}
.organ-block h3 {{ color: #3b0718; text-transform: uppercase; font-size: 13px; line-height: 1.12; font-weight: 900; }}
.organ-block p {{ margin-top: 8px; max-width: 8.9in; color: #665a52; font-size: 10.8px; line-height: 1.36; font-weight: 700; }}
.workflow {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 9px; margin-top: 26px; }}
.workflow div {{ border-top: 4px solid #6B1531; border-bottom: 1px solid #d7c7b2; min-height: 68px; padding: 8px 6px 7px; color: #3b0718; text-transform: uppercase; text-align: center; font-size: 8.4px; line-height: 1.12; font-weight: 900; }}
.workflow div:nth-child(2), .workflow div:nth-child(5) {{ border-top-color: #C59A3D; }}
.fields {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px 28px; margin-top: 38px; }}
.fields span {{ border-top: 1px solid rgba(20,16,13,.28); padding-top: 8px; color: #3b0718; font-size: 10px; line-height: 1.1; font-weight: 900; text-transform: uppercase; }}
</style>
</head>
<body>
  <section class="page cover">
    <div class="top-rule"></div>
    <div class="cover-copy">
      <div class="eyebrow">Observatorio de Fiscalización Electoral · Proceso Federal 2023-2024</div>
      <h1>Compilación<br>de criterios<br>de fiscalización</h1>
      <p>Diputaciones federales 2024: criterios derivados del dictamen, resoluciones administrativas del INE y sentencias del TEPJF.</p>
    </div>
    <aside class="cover-panel">
      <div class="eyebrow">Documento de criterios</div>
      <p>Documento institucional construido a partir del corte local del Observatorio. Ordena criterios, efectos y usos operativos para dictamen, resolución y seguimiento.</p>
      <div class="stats">
        <div class="stat"><b>52</b><span>sentencias revisadas</span></div>
        <div class="stat"><b>12</b><span>criterios sistematizados</span></div>
        <div class="stat"><b>12</b><span>expedientes base</span></div>
        <div class="stat"><b>$20.7 M</b><span>sumatoria de montos positivos</span></div>
      </div>
    </aside>
    {footer(1, total)}
  </section>

  <section class="page">
    <div class="top-rule"></div>
    <div class="eyebrow">Guía de lectura</div>
    <h2>Índice</h2>
    <p class="method-copy">El documento traduce el modelo formal de compilación jurídica a un instrumento de fiscalización electoral: corpus, matriz de criterios, fichas sustantivas, lectura por órgano y modelo de organización de datos.</p>
    <div class="index-grid">{index_html}</div>
    <div class="note"><b>Clave metodológica</b><br>Los registros en $0.00 o No integrado aparecen como casos consultables porque ubican una controversia, pero no se suman si no hay una cantidad económica positiva fijada, confirmada o modificada.</div>
    {footer(2, total)}
  </section>

  <section class="page">
    <div class="top-rule"></div>
    <div class="eyebrow">Metodología y corpus</div>
    <h2>Criterios derivados de diputaciones federales</h2>
    <p class="method-copy">La selección parte del corpus local del Observatorio, del dictamen y resoluciones de fiscalización del INE, y de sentencias oficiales del TEPJF vinculadas con campaña, quejas, cómputo distrital, rebase de tope, competencia y efectos. El foco se limita a Sala Superior y Sala Regional Ciudad de México.</p>
    <div class="metric-strip">
      <div class="metric"><b>52</b><span>sentencias TEPJF revisadas</span></div>
      <div class="metric"><b>12</b><span>expedientes base</span></div>
      <div class="metric"><b>19</b><span>registros de sanción INE</span></div>
      <div class="metric"><b>15</b><span>registros con monto positivo</span></div>
    </div>
    <table>
      <thead><tr><th>Acto o fuente</th><th>Relación con diputaciones federales</th><th>Expedientes TEPJF</th></tr></thead>
      <tbody>
        <tr><td>INE/CG1928/2024 e INE/CG1929/2024</td><td>Dictamen y resolución de campaña federal.</td><td class="links">{link_list("SUP-RAP-342/2024; SUP-RAP-413/2024")}</td></tr>
        <tr><td>INE/CG1929/2024 e INE/CG1930/2024</td><td>Revisión de informes de campaña federal.</td><td class="links">{link_list("SUP-RAP-352/2024")}</td></tr>
        <tr><td>INE/CG1955/2024</td><td>Fiscalización de campaña federal y concurrente.</td><td class="links">{link_list("SUP-RAP-357/2024")}</td></tr>
        <tr><td>INE/CG1501/2024</td><td>Queja por eventos no reportados y aportaciones prohibidas.</td><td class="links">{link_list("SCM-RAP-47/2024")}</td></tr>
        <tr><td>Cómputos distritales 2024</td><td>Juicios de inconformidad de diputaciones federales en la cuarta circunscripción.</td><td class="links">{link_list("SCM-JIN-27/2024; SCM-JIN-30/2024; SCM-JIN-56/2024; SCM-JIN-103/2024")}</td></tr>
        <tr><td>Acuerdos de competencia</td><td>Delimitación por cargo, principio, candidatura y territorio.</td><td class="links">{link_list("SUP-RAP-414/2024; SUP-RAP-415/2024")}</td></tr>
      </tbody>
    </table>
    {footer(3, total)}
  </section>

  <section class="page matrix">
    <div class="top-rule"></div>
    <div class="eyebrow">Matriz ejecutiva</div>
    <h2>12 criterios sistematizados</h2>
    <table>
      <thead><tr><th>Clave</th><th>Criterio</th><th>Tema</th><th>Órgano</th><th>Efecto</th></tr></thead>
      <tbody>{matrix_rows}</tbody>
    </table>
    {footer(4, total)}
  </section>

  {criterion_pages}

  <section class="page">
    <div class="top-rule"></div>
    <div class="eyebrow">Lectura por órgano y montos</div>
    <h2>Sala Superior y Sala Regional Ciudad de México</h2>
    <div class="organ-blocks">
      <div class="organ-block"><h3>Sala Superior</h3><p>Concentra los expedientes base cuantificados: SUP-RAP-342/2024, SUP-RAP-352/2024, SUP-RAP-357/2024 y SUP-RAP-413/2024. De ellos sale la sumatoria exacta de $20,700,473.59 en montos originales observados por el INE.</p></div>
      <div class="organ-block"><h3>Sala Regional Ciudad de México</h3><p>El asunto SCM-RAP-47/2024, vinculado con INE/CG1501/2024, ordena revisar la suficiencia del estudio de queja por eventos presuntamente no reportados y aportaciones prohibidas.</p></div>
      <div class="organ-block"><h3>Corpus complementario SCM</h3><p>SCM-JIN-27/2024, SCM-JIN-30/2024, SCM-JIN-56/2024 y SCM-JIN-103/2024 aportan lectura de cómputo distrital, nulidad, principio impugnado y efectos de modificación o confirmación.</p></div>
      <div class="organ-block"><h3>Lectura de montos</h3><p>La sumatoria no cuenta expedientes; cuenta pesos. Solo se agregan registros con monto original positivo observado por el INE. Los casos en $0.00 o No integrado se conservan porque ubican controversias, pero no modifican el cálculo.</p></div>
    </div>
    {footer(17, total)}
  </section>

  <section class="page">
    <div class="top-rule"></div>
    <div class="eyebrow">Modelo de organización</div>
    <h2>De la sentencia al dato actualizable</h2>
    <div class="workflow">
      <div>Fuente oficial</div><div>Extracción de texto</div><div>Clasificación jurídica</div><div>Validación</div><div>Matriz normalizada</div><div>App y PDF</div>
    </div>
    <div class="fields">
      <span>expediente</span><span>órgano</span><span>tipo de medio</span><span>acto de origen</span>
      <span>clave administrativa</span><span>tema</span><span>criterio</span><span>carga probatoria</span>
      <span>efecto</span><span>monto positivo</span><span>territorio</span><span>URL oficial</span>
      <span>estado de validación</span><span>observaciones</span><span>utilidad temporal</span><span>versión de corte</span>
    </div>
    <div class="note" style="width:9.5in; bottom:1.05in;"><b>Cierre metodológico</b><br>El modelo permite presentar lo existente, justificar el corte metodológico y proponer una compilación en tiempo real apoyada en experiencia acumulada de fiscalización de procesos electorales federales.</div>
    {footer(18, total)}
  </section>
</body>
</html>
"""


def export_html() -> Path:
    EXPORTS.mkdir(parents=True, exist_ok=True)
    HTML_PATH.write_text(build_html(), encoding="utf-8")
    return HTML_PATH


def export_pdf() -> Path:
    html_path = export_html()
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Playwright no está instalado; instala playwright para generar el PDF.") from exc

    with sync_playwright() as playwright:
        browser_candidates = [
            Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
            Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
        ]
        executable_path = next((str(path) for path in browser_candidates if path.exists()), None)
        launch_kwargs = {"executable_path": executable_path} if executable_path else {}
        browser = playwright.chromium.launch(**launch_kwargs)
        page = browser.new_page(viewport={"width": 1584, "height": 1224}, device_scale_factor=1)
        page.goto(html_path.as_uri(), wait_until="networkidle")
        page.pdf(
            path=str(PDF_PATH),
            format="Letter",
            landscape=True,
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            prefer_css_page_size=True,
        )
        page.screenshot(path=str(SCREENSHOT_PATH), full_page=False)
        browser.close()
    return PDF_PATH


def export() -> tuple[Path, Path]:
    return export_html(), export_pdf()


if __name__ == "__main__":
    html_path, pdf_path = export()
    print(html_path)
    print(pdf_path)
