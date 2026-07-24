from __future__ import annotations

import textwrap
from pathlib import Path

from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
EXPORTS = ROOT / "exports"
PDF_PATH = EXPORTS / "criterios_fiscalizacion_diputaciones_2024.pdf"
PNG_PREFIX = EXPORTS / "captura_criterios_fiscalizacion"

W, H = landscape(letter)
M = 36

GUINDA = "#6B1531"
DORADO = "#C59A3D"
VERDE = "#1E5B4F"
NEGRO = "#14100D"
TEXTO = "#211816"
GRIS = "#665A52"
CLARO = "#FFFDF8"
LINEA = "#D8CCBD"

FOOTER = "Observatorio de Fiscalización Electoral - Proceso Federal 2023-2024 · Corte: 23 de julio de 2026"

TEPJF_URLS = {
    "SUP-RAP-342/2024": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-RAP-0342-2024-",
    "SUP-RAP-352/2024": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-RAP-0352-2024-",
    "SUP-RAP-357/2024": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-RAP-0357-2024-",
    "SUP-RAP-413/2024": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-RAP-0413-2024-",
    "SCM-RAP-47/2024": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SCM-RAP-0047-2024-",
    "ST-RAP-50/2024": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/ST-RAP-0050-2024-",
    "ST-RAP-74/2024": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/ST-RAP-0074-2024-",
    "SG-JIN-114/2024": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SG-JIN-0114-2024-",
    "SUP-REC-764/2024": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-REC-0764-2024-",
    "SUP-RAP-414/2024": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-RAP-0414-2024-",
    "SUP-RAP-415/2024": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-RAP-0415-2024-",
}


CRITERIA = [
    {
        "id": "FIS-01",
        "title": "Exhaustividad del dictamen, anexos y conclusiones",
        "theme": "Dictamen y resolución",
        "source": "SUP-RAP-342/2024; SCM-RAP-47/2024",
        "rule": "La autoridad debe permitir reconstruir la relación entre hallazgo, anexo, conclusión y sanción. Si la motivación no explica el paso del hecho observado a la consecuencia, procede revisar el acto.",
        "burden": "Señalar conclusión, anexo, conducta y omisión concreta de valoración; no basta una inconformidad general.",
        "effect": "Revocación para efectos, revocación parcial o confirmación.",
    },
    {
        "id": "FIS-02",
        "title": "Fallas del Sistema Integral de Fiscalización",
        "theme": "SIF",
        "source": "SUP-RAP-342/2024; SUP-RAP-357/2024; SUP-RAP-413/2024",
        "rule": "La referencia genérica a fallas del SIF no desvirtúa una infracción si no se acredita cómo impidió cumplir una obligación concreta.",
        "burden": "Precisar fecha, módulo, operación, evidencia técnica y obligación afectada.",
        "effect": "Confirmación cuando el agravio es genérico; posible revocación parcial si incide en una conclusión específica.",
    },
    {
        "id": "FIS-03",
        "title": "Documentación soporte y comprobación fiscal",
        "theme": "Comprobación de gasto",
        "source": "SUP-RAP-352/2024; SUP-RAP-357/2024",
        "rule": "La falta de soporte fiscal, contractual o contable idóneo puede sostener sanciones si el sujeto obligado no desvirtúa la observación.",
        "burden": "Aportar documentación completa y explicar su correspondencia con la operación observada.",
        "effect": "Confirmación de conclusiones o sanciones cuando no se acredita el soporte.",
    },
    {
        "id": "FIS-04",
        "title": "Comprobantes electrónicos de pago",
        "theme": "CEP, XML y soporte",
        "source": "SUP-RAP-352/2024; SUP-RAP-357/2024; SUP-RAP-413/2024",
        "rule": "La defensa sobre comprobantes electrónicos debe individualizar cada operación y explicar por qué no actualiza infracción.",
        "burden": "Precisar comprobante, modificación, gratuidad, imposibilidad de firma o razón jurídica concreta.",
        "effect": "Confirmación cuando falta explicación específica.",
    },
    {
        "id": "FIS-05",
        "title": "Registro oportuno y duplicidad de consecuencias",
        "theme": "Registro en tiempo real",
        "source": "SUP-RAP-357/2024",
        "rule": "La autoridad debe distinguir registro inexistente, extemporáneo o duplicado, y ajustar la consecuencia a esa diferencia.",
        "burden": "Acreditar fecha de operación, fecha de registro, soporte cargado y posible duplicidad.",
        "effect": "Revocación parcial cuando hay error de individualización; confirmación si la observación subsiste.",
    },
    {
        "id": "FIS-06",
        "title": "Prorrateo y candidaturas beneficiadas",
        "theme": "Beneficio electoral",
        "source": "SUP-RAP-413/2024",
        "rule": "El prorrateo debe reflejar gasto, propaganda, candidatura beneficiada, ámbito territorial y regla de distribución aplicable.",
        "burden": "Vincular pieza propagandística, sujeto obligado, candidatura, distrito, entidad y beneficio.",
        "effect": "Revocación parcial o confirmación según la precisión del análisis.",
    },
    {
        "id": "FIS-07",
        "title": "Omisión de reportar propaganda, eventos o gastos",
        "theme": "Gasto no reportado",
        "source": "SUP-RAP-342/2024; SUP-RAP-357/2024; SUP-RAP-413/2024; SCM-RAP-47/2024; ST-RAP-50/2024",
        "rule": "La omisión se analiza por existencia del gasto o propaganda, beneficio electoral, obligación de reporte y suficiencia del soporte.",
        "burden": "Identificar material, evento, proveedor, valor, candidatura beneficiada, temporalidad y deslinde.",
        "effect": "Confirmación, revocación para efectos o revocación parcial.",
    },
    {
        "id": "FIS-08",
        "title": "Aportaciones prohibidas",
        "theme": "Quejas de fiscalización",
        "source": "SCM-RAP-47/2024",
        "rule": "La autoridad debe valorar hechos, fuente de aportación, bien o servicio, beneficiario y relación con campaña.",
        "burden": "Precisar aportante, valor, conducta, candidatura, evento o propaganda y soporte probatorio.",
        "effect": "Revocación para nueva resolución si el estudio administrativo fue insuficiente.",
    },
    {
        "id": "FIS-09",
        "title": "Deslinde eficaz",
        "theme": "Responsabilidad frente a terceros",
        "source": "ST-RAP-50/2024",
        "rule": "Un deslinde genérico o tardío no elimina por sí mismo la responsabilidad frente a propaganda o actos de terceros.",
        "burden": "Probar fecha, medio, solicitud de retiro, comunicación a autoridad y eficacia material.",
        "effect": "Confirmación o revocación según valoración probatoria.",
    },
    {
        "id": "FIS-10",
        "title": "Rebase de tope y nulidad",
        "theme": "Validez de elección",
        "source": "SCM-JIN-27/2024; SG-JIN-114/2024; SUP-REC-764/2024; SUP-RAP-352/2024; SUP-RAP-357/2024; SUP-RAP-413/2024",
        "rule": "La sanción administrativa aislada no equivale por sí misma a nulidad; se requiere monto, acumulación al tope, determinancia y vínculo con la elección.",
        "burden": "Probar impacto cuantitativo o cualitativo y relación con el resultado electoral.",
        "effect": "En el corpus de nulidad, infracciones aisladas no bastan por sí solas para anular.",
    },
    {
        "id": "FIS-11",
        "title": "Competencia por cargo, principio y territorio",
        "theme": "Competencia",
        "source": "SUP-RAP-414/2024; SUP-RAP-415/2024",
        "rule": "La competencia depende de tipo de elección, principio, cargo, entidad, distrito y vínculo con la candidatura o elección impugnada.",
        "burden": "Precisar acto reclamado, candidatura, cargo, principio y territorio.",
        "effect": "Acuerdos de competencia o remisión a sala regional.",
    },
    {
        "id": "FIS-12",
        "title": "Efectos de revocación",
        "theme": "Efectos",
        "source": "SUP-RAP-342/2024; SUP-RAP-357/2024; SUP-RAP-413/2024; SCM-RAP-47/2024; ST-RAP-50/2024",
        "rule": "El sentido de una sentencia puede confirmar una parte, revocar otra o exigir un nuevo pronunciamiento de la autoridad.",
        "burden": "Identificar conclusión afectada, agravio fundado, alcance de revocación y obligación posterior.",
        "effect": "Confirmación parcial, revocación para efectos, recálculo o nueva resolución.",
    },
]


def set_color(c: canvas.Canvas, color: str) -> None:
    c.setFillColor(color)
    c.setStrokeColor(color)


def text_lines(text: str, width: int) -> list[str]:
    return textwrap.wrap(text, width=width, break_long_words=False)


def draw_top_rule(c: canvas.Canvas) -> None:
    c.setFillColor(GUINDA)
    c.rect(M, H - 42, 360, 7, stroke=0, fill=1)
    c.setFillColor(DORADO)
    c.rect(M + 360, H - 42, 80, 7, stroke=0, fill=1)
    c.setFillColor(VERDE)
    c.rect(M + 440, H - 42, 120, 7, stroke=0, fill=1)
    c.setFillColor(NEGRO)
    c.rect(M + 560, H - 42, W - M * 2 - 560, 7, stroke=0, fill=1)


def footer(c: canvas.Canvas, page: int, total: int) -> None:
    c.setStrokeColor(LINEA)
    c.setLineWidth(0.6)
    c.line(M, 31, W - M, 31)
    c.setFillColor(GRIS)
    c.setFont("Helvetica-Bold", 6.8)
    c.drawString(M, 18, FOOTER)
    c.drawRightString(W - M, 18, f"PÁGINA {page} DE {total}")


def draw_wrapped(c: canvas.Canvas, text: str, x: float, y: float, width_chars: int, size: float = 9.2, leading: float = 12, color: str = GRIS, font: str = "Helvetica-Bold") -> float:
    c.setFillColor(color)
    c.setFont(font, size)
    for line in text_lines(text, width_chars):
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_label(c: canvas.Canvas, label: str, x: float, y: float, color: str = GUINDA) -> None:
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(x, y, label.upper())


def source_links(c: canvas.Canvas, source: str, x: float, y: float) -> None:
    c.setFont("Helvetica-Bold", 7.2)
    cursor = x
    for part in [p.strip() for p in source.split(";")]:
        url = TEPJF_URLS.get(part)
        label = part
        if cursor + c.stringWidth(label, "Helvetica-Bold", 7.2) > W - M:
            y -= 10
            cursor = x
        c.setFillColor(GUINDA if url else GRIS)
        c.drawString(cursor, y, label)
        if url:
            w = c.stringWidth(label, "Helvetica-Bold", 7.2)
            c.linkURL(url, (cursor, y - 1, cursor + w, y + 8), relative=0)
            cursor += w + 8
        else:
            cursor += c.stringWidth(label, "Helvetica-Bold", 7.2) + 8


def page_cover(c: canvas.Canvas, total: int) -> None:
    c.setFillColor(CLARO)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    draw_top_rule(c)
    c.setFillColor(GUINDA)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(M, 392, "OBSERVATORIO DE FISCALIZACIÓN ELECTORAL · PROCESO FEDERAL 2023-2024")
    c.setFillColor(NEGRO)
    c.setFont("Helvetica-Bold", 42)
    for i, line in enumerate(["COMPILACIÓN", "DE CRITERIOS", "DE FISCALIZACIÓN"]):
        c.drawString(M, 336 - i * 46, line)
    draw_wrapped(
        c,
        "Diputaciones federales 2024: criterios emanados del dictamen, resoluciones administrativas del INE y sentencias del TEPJF.",
        M,
        178,
        70,
        size=13,
        leading=17,
    )
    c.setStrokeColor(NEGRO)
    c.setLineWidth(4)
    c.line(470, 294, W - M, 294)
    draw_label(c, "Versión para reunión", 470, 274)
    draw_wrapped(
        c,
        "Documento ejecutivo construido a partir del corte local del Observatorio. Sirve para discutir criterios, cargas probatorias, efectos y un modelo de organización de datos actualizable.",
        470,
        252,
        56,
        size=9.5,
        leading=13,
    )
    stats = [("52", "sentencias revisadas"), ("12", "criterios sistematizados"), ("7", "expedientes base"), ("$20.7 M", "sumatoria de montos positivos")]
    for idx, (value, label) in enumerate(stats):
        x = 470 + (idx % 2) * 155
        y = 166 - (idx // 2) * 70
        c.setFillColor(DORADO if idx % 2 == 0 else GUINDA)
        c.rect(x, y + 38, 125, 3, stroke=0, fill=1)
        c.setFillColor(GUINDA)
        c.setFont("Helvetica-Bold", 24)
        c.drawString(x, y + 10, value)
        c.setFillColor(GRIS)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(x, y, label.upper())
    footer(c, 1, total)
    c.showPage()


def page_index(c: canvas.Canvas, total: int) -> None:
    draw_top_rule(c)
    draw_label(c, "Guía de lectura", M, H - 76)
    c.setFillColor(NEGRO)
    c.setFont("Helvetica-Bold", 34)
    c.drawString(M, H - 116, "ÍNDICE")
    draw_wrapped(
        c,
        "El documento separa hallazgos ejecutivos, criterios por tema, fichas jurídicas y modelo de datos para que la compilación pueda vivir en la app.",
        M,
        H - 150,
        55,
        size=10.5,
        leading=14,
    )
    items = [
        ("01", "Universo y actos de origen", "3"),
        ("02", "Matriz ejecutiva de criterios", "4"),
        ("03", "Fichas FIS-01 a FIS-04", "5"),
        ("04", "Fichas FIS-05 a FIS-08", "6"),
        ("05", "Fichas FIS-09 a FIS-12", "7"),
        ("06", "Lectura por órgano y montos", "8"),
        ("07", "Modelo de organización de datos", "9"),
    ]
    y = H - 90
    x = 380
    c.setStrokeColor(NEGRO)
    c.setLineWidth(4)
    c.line(x, y + 18, W - M, y + 18)
    for number, title, page in items:
        c.setStrokeColor(LINEA)
        c.line(x, y - 18, W - M, y - 18)
        c.setFillColor(GUINDA)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(x, y, number)
        c.setFillColor(GUINDA)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(x + 58, y + 2, title.upper())
        c.setFillColor(NEGRO)
        c.setFont("Helvetica-Bold", 15)
        c.drawRightString(W - M, y + 1, page)
        y -= 46
    c.setStrokeColor(DORADO)
    c.setLineWidth(3)
    c.line(M, 210, 330, 210)
    draw_label(c, "Clave metodológica", M, 186)
    draw_wrapped(
        c,
        "Los registros en $0.00 o No integrado aparecen como casos consultables porque ubican una controversia, pero no se suman si no hay una cantidad económica positiva fijada, confirmada o modificada.",
        M,
        166,
        62,
        size=9.4,
        leading=12.5,
    )
    footer(c, 2, total)
    c.showPage()


def page_universe(c: canvas.Canvas, total: int) -> None:
    draw_top_rule(c)
    draw_label(c, "Universo documental", M, H - 76)
    c.setFillColor(NEGRO)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(M, H - 106, "CORTE Y ACTOS DE ORIGEN")
    stats = [("52", "sentencias TEPJF revisadas"), ("11", "expedientes con marca de fiscalización"), ("19", "registros de sanción INE"), ("15", "registros con monto positivo")]
    for idx, (value, label) in enumerate(stats):
        x = M + idx * 180
        c.setFillColor(GUINDA if idx != 1 else DORADO)
        c.rect(x, H - 154, 132, 4, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 25)
        c.drawString(x, H - 184, value)
        c.setFillColor(GRIS)
        c.setFont("Helvetica-Bold", 7.6)
        c.drawString(x, H - 198, label.upper())
    rows = [
        ("INE/CG1928/2024 e INE/CG1929/2024", "Dictamen y resolución de campaña federal", "SUP-RAP-342/2024; SUP-RAP-413/2024"),
        ("INE/CG1929/2024 e INE/CG1930/2024", "Revisión de informes de campaña federal", "SUP-RAP-352/2024"),
        ("INE/CG1955/2024", "Fiscalización de campaña federal y concurrente", "SUP-RAP-357/2024"),
        ("INE/CG1501/2024", "Queja por eventos no reportados y aportaciones prohibidas", "SCM-RAP-47/2024"),
        ("INE/CG1098/2024", "Queja por gastos y subvaluación", "ST-RAP-74/2024"),
        ("INE/CG838/2024", "Precampaña, gasto no reportado y deslinde", "ST-RAP-50/2024"),
    ]
    y = H - 250
    c.setFillColor(GUINDA)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(M, y, "ACTO INE")
    c.drawString(250, y, "RELACIÓN CON DIPUTACIONES FEDERALES")
    c.drawString(530, y, "EXPEDIENTES TEPJF")
    y -= 18
    for act, desc, src in rows:
        c.setStrokeColor(LINEA)
        c.line(M, y + 10, W - M, y + 10)
        c.setFillColor(TEXTO)
        c.setFont("Helvetica-Bold", 8.4)
        c.drawString(M, y, act)
        draw_wrapped(c, desc, 250, y, 43, size=8.2, leading=10, color=GRIS)
        source_links(c, src, 530, y)
        y -= 42
    footer(c, 3, total)
    c.showPage()


def page_matrix(c: canvas.Canvas, total: int) -> None:
    draw_top_rule(c)
    draw_label(c, "Matriz ejecutiva", M, H - 76)
    c.setFillColor(NEGRO)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(M, H - 106, "12 CRITERIOS PARA DISCUSIÓN")
    y = H - 138
    cols = [(M, 48), (91, 214), (314, 132), (456, 118), (584, 190)]
    headers = ["CLAVE", "CRITERIO", "TEMA", "ÓRGANO", "UTILIDAD"]
    c.setFillColor(GUINDA)
    c.setFont("Helvetica-Bold", 7.8)
    for (x, _), h in zip(cols, headers):
        c.drawString(x, y, h)
    y -= 14
    for item in CRITERIA:
        c.setStrokeColor(LINEA)
        c.line(M, y + 8, W - M, y + 8)
        c.setFillColor(GUINDA)
        c.setFont("Helvetica-Bold", 8.2)
        c.drawString(cols[0][0], y, item["id"])
        draw_wrapped(c, item["title"], cols[1][0], y, 35, size=7.5, leading=8.7, color=TEXTO)
        draw_wrapped(c, item["theme"], cols[2][0], y, 22, size=7.5, leading=8.7, color=GRIS)
        organ = "Sala Superior / SCM" if item["id"] in {"FIS-01", "FIS-07"} else ("SCM" if item["id"] == "FIS-08" else ("ST" if item["id"] == "FIS-09" else "Sala Superior"))
        draw_wrapped(c, organ, cols[3][0], y, 19, size=7.5, leading=8.7, color=GRIS)
        draw_wrapped(c, item["rule"], cols[4][0], y, 45, size=7.1, leading=8.3, color=GRIS)
        y -= 34
    footer(c, 4, total)
    c.showPage()


def criterion_card(c: canvas.Canvas, item: dict[str, str], x: float, y: float, width_chars: int = 50) -> float:
    c.setStrokeColor(DORADO if item["id"] in {"FIS-03", "FIS-06", "FIS-09", "FIS-12"} else GUINDA)
    c.setLineWidth(3)
    c.line(x, y, x + 300, y)
    y -= 16
    c.setFillColor(GUINDA)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x, y, item["id"])
    c.setFillColor(NEGRO)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x + 48, y, item["title"][:58])
    y -= 15
    draw_label(c, "Criterio jurídico", x, y, GUINDA)
    y = draw_wrapped(c, item["rule"], x, y - 12, width_chars, size=7.8, leading=9.6, color=TEXTO, font="Helvetica")
    draw_label(c, "Carga probatoria", x, y - 3, DORADO)
    y = draw_wrapped(c, item["burden"], x, y - 15, width_chars, size=7.6, leading=9.4, color=GRIS, font="Helvetica")
    draw_label(c, "Efecto observado", x, y - 3, VERDE)
    y = draw_wrapped(c, item["effect"], x, y - 15, width_chars, size=7.6, leading=9.4, color=GRIS, font="Helvetica")
    draw_label(c, "Fuente", x, y - 3, GUINDA)
    source_links(c, item["source"], x, y - 15)
    return y - 28


def page_cards(c: canvas.Canvas, total: int, page: int, title: str, items: list[dict[str, str]]) -> None:
    draw_top_rule(c)
    draw_label(c, "Fichas de criterio", M, H - 76)
    c.setFillColor(NEGRO)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(M, H - 104, title.upper())
    positions = [(M, H - 140), (420, H - 140), (M, H - 350), (420, H - 350)]
    for item, (x, y) in zip(items, positions):
        criterion_card(c, item, x, y, 53)
    footer(c, page, total)
    c.showPage()


def page_organs(c: canvas.Canvas, total: int) -> None:
    draw_top_rule(c)
    draw_label(c, "Lectura por órgano y montos", M, H - 76)
    c.setFillColor(NEGRO)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(M, H - 106, "SALA SUPERIOR Y SALA REGIONAL CIUDAD DE MÉXICO")
    blocks = [
        ("Sala Superior", "Concentra los expedientes base cuantificados: SUP-RAP-342/2024, SUP-RAP-352/2024, SUP-RAP-357/2024 y SUP-RAP-413/2024. De ellos sale la sumatoria exacta de $20,700,473.59 en montos originales observados por el INE."),
        ("Sala Regional Ciudad de México", "El asunto SCM-RAP-47/2024, vinculado con INE/CG1501/2024, ordena revisar la suficiencia del estudio de queja por eventos presuntamente no reportados y aportaciones prohibidas."),
        ("Salas regionales auxiliares", "ST-RAP-50/2024 y ST-RAP-74/2024 permiten completar criterios sobre deslinde, gasto no reportado, procedencia y efectos procesales."),
    ]
    y = H - 152
    for title, body in blocks:
        c.setStrokeColor(DORADO if "Ciudad" in title else GUINDA)
        c.setLineWidth(4)
        c.line(M, y, W - M, y)
        c.setFillColor(GUINDA)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(M, y - 24, title.upper())
        draw_wrapped(c, body, M, y - 46, 115, size=10, leading=14, color=GRIS)
        y -= 118
    c.setStrokeColor(NEGRO)
    c.setLineWidth(4)
    c.line(M, 128, W - M, 128)
    draw_label(c, "Lectura de montos", M, 104)
    draw_wrapped(
        c,
        "La sumatoria no cuenta expedientes; cuenta pesos. Solo se agregan registros con monto original positivo observado por el INE. Los casos en $0.00 o No integrado se conservan porque ubican controversias, pero no modifican el cálculo.",
        M,
        84,
        128,
        size=9.4,
        leading=12.5,
    )
    footer(c, 8, total)
    c.showPage()


def page_model(c: canvas.Canvas, total: int) -> None:
    draw_top_rule(c)
    draw_label(c, "Modelo de organización", M, H - 76)
    c.setFillColor(NEGRO)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(M, H - 106, "DE LA SENTENCIA AL DATO ACTUALIZABLE")
    steps = ["Fuente oficial", "Extracción de texto", "Clasificación jurídica", "Validación", "Matriz normalizada", "App y PDF"]
    x = M
    y = H - 176
    for step in steps:
        c.setStrokeColor(GUINDA)
        c.setLineWidth(3)
        c.rect(x, y, 112, 48, stroke=1, fill=0)
        draw_wrapped(c, step.upper(), x + 10, y + 29, 18, size=7.5, leading=9, color=GUINDA)
        x += 122
    fields = [
        "expediente", "órgano", "tipo de medio", "acto de origen", "clave administrativa", "tema",
        "criterio", "carga probatoria", "efecto", "monto positivo", "territorio", "URL oficial",
        "estado de validación", "observaciones",
    ]
    y = H - 262
    c.setFillColor(GUINDA)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(M, y, "CAMPOS MÍNIMOS PARA LA APP")
    y -= 24
    for idx, field in enumerate(fields):
        cx = M + (idx % 4) * 185
        cy = y - (idx // 4) * 38
        c.setStrokeColor(LINEA)
        c.line(cx, cy + 14, cx + 145, cy + 14)
        c.setFillColor(TEXTO)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(cx, cy, field)
    c.setStrokeColor(DORADO)
    c.setLineWidth(4)
    c.line(M, 126, W - M, 126)
    draw_label(c, "Cierre para reunión", M, 102)
    draw_wrapped(
        c,
        "El modelo permite presentar lo existente, justificar el corte metodológico y proponer una compilación en tiempo real apoyada en experiencia acumulada de fiscalización de procesos electorales federales.",
        M,
        82,
        126,
        size=9.4,
        leading=12.5,
    )
    footer(c, 9, total)
    c.showPage()


def export() -> Path:
    EXPORTS.mkdir(parents=True, exist_ok=True)
    total = 9
    c = canvas.Canvas(str(PDF_PATH), pagesize=landscape(letter))
    c.setTitle("Compilación de criterios de fiscalización electoral - Diputaciones federales 2024")
    c.setAuthor("Observatorio de Fiscalización Electoral")
    page_cover(c, total)
    page_index(c, total)
    page_universe(c, total)
    page_matrix(c, total)
    page_cards(c, total, 5, "FIS-01 a FIS-04", CRITERIA[:4])
    page_cards(c, total, 6, "FIS-05 a FIS-08", CRITERIA[4:8])
    page_cards(c, total, 7, "FIS-09 a FIS-12", CRITERIA[8:])
    page_organs(c, total)
    page_model(c, total)
    c.save()
    return PDF_PATH


if __name__ == "__main__":
    print(export())
