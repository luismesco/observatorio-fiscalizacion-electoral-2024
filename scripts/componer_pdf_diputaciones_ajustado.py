from __future__ import annotations

from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "exports" / "diputaciones_electas_reporte.pdf"
OUT = ROOT / "exports" / "diputaciones_electas_reporte_ajustado_final.pdf"

W, H = 792, 612
GUINDA = "#6B1531"
DORADO = "#C59A3D"
VERDE = "#1E5B4F"
NEGRO = "#14100D"
TEXTO = "#211816"
GRIS = "#665A52"
CLARO = "#FFFDF8"
LINEA = "#D8CCBD"
FOOTER = "OBSERVATORIO DE FISCALIZACIÓN ELECTORAL - PROCESO FEDERAL 2023-2024 · CORTE: 23 DE JULIO DE 2026"


def overlay_canvas() -> tuple[canvas.Canvas, BytesIO]:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(W, H))
    return c, buffer


def wrap(text: str, max_chars: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        candidate = " ".join(current + [word])
        if len(candidate) <= max_chars:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def draw_wrapped(c: canvas.Canvas, text: str, x: float, y: float, chars: int, size: float, leading: float, color: str = GRIS, font: str = "Helvetica-Bold") -> float:
    c.setFillColor(color)
    c.setFont(font, size)
    for line in wrap(text, chars):
        c.drawString(x, y, line)
        y -= leading
    return y


def footer(c: canvas.Canvas, page: int, total: int = 9) -> None:
    c.setStrokeColor(LINEA)
    c.setLineWidth(0.5)
    c.line(30, 33, W - 30, 33)
    c.setFillColor(GRIS)
    c.setFont("Helvetica-Bold", 6.2)
    c.drawString(30, 19, FOOTER)
    c.drawRightString(W - 30, 19, f"PÁGINA {page} DE {total}")


def page1_page() -> PdfReader:
    c, buffer = overlay_canvas()
    c.setFillColor(CLARO)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(GUINDA)
    c.rect(38, H - 42, 322, 7, stroke=0, fill=1)
    c.setFillColor(DORADO)
    c.rect(360, H - 42, 78, 7, stroke=0, fill=1)
    c.setFillColor(VERDE)
    c.rect(438, H - 42, 104, 7, stroke=0, fill=1)
    c.setFillColor(NEGRO)
    c.rect(542, H - 42, W - 580, 7, stroke=0, fill=1)
    c.setFillColor(GUINDA)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(38, 320, "OBSERVATORIO DE FISCALIZACIÓN ELECTORAL · PROCESO FEDERAL 2023-2024")
    c.setFillColor(NEGRO)
    c.setFont("Helvetica-Bold", 42)
    for y, line in zip([268, 224, 180, 136], ["FISCALIZACIÓN", "DE DIPUTACIONES", "FEDERALES", "2024"]):
        c.drawString(38, y, line)
    draw_wrapped(
        c,
        "Criterios, expedientes y modelo de datos para presentar el corte documental de fiscalización.",
        38,
        86,
        68,
        12.5,
        16,
        GRIS,
    )
    c.setStrokeColor(NEGRO)
    c.setLineWidth(4)
    c.line(452, 270, 754, 270)
    c.setFillColor(GUINDA)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(452, 246, "CORTE DOCUMENTAL DE FISCALIZACIÓN")
    draw_wrapped(
        c,
        "Corte documental al 23 de julio de 2026. El reporte separa casos consultables de montos positivos: la sumatoria cuenta pesos observados por el INE, no número de expedientes.",
        452,
        225,
        68,
        8.8,
        11.5,
        GRIS,
    )
    stats = [("52", "sentencias revisadas en el corpus local"), ("7", "expedientes base con sentencia TEPJF"), ("19", "registros de sanción INE"), ("$20.7 M", "sumatoria de montos positivos observados")]
    for i, (value, label) in enumerate(stats):
        x = 452 + (i % 2) * 155
        y = 118 - (i // 2) * 62
        c.setFillColor(DORADO if i % 2 == 0 else GUINDA)
        c.rect(x, y + 42, 122, 3, stroke=0, fill=1)
        c.setFillColor(GUINDA)
        c.setFont("Helvetica-Bold", 23 if i < 3 else 19)
        c.drawString(x, y + 15, value)
        draw_wrapped(c, label.upper(), x, y, 28, 6.3, 7, GRIS, "Helvetica-Bold")
    footer(c, 1, 9)
    c.save()
    buffer.seek(0)
    return PdfReader(buffer)


def page2_page() -> PdfReader:
    c, buffer = overlay_canvas()
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(GUINDA)
    c.rect(30, H - 42, 304, 7, stroke=0, fill=1)
    c.setFillColor(DORADO)
    c.rect(334, H - 42, 66, 7, stroke=0, fill=1)
    c.setFillColor(NEGRO)
    c.rect(400, H - 42, W - 430, 7, stroke=0, fill=1)
    c.setFillColor(GUINDA)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(30, 524, "GUÍA DE LECTURA")
    c.setFillColor(NEGRO)
    c.setFont("Helvetica-Bold", 44)
    c.drawString(30, 476, "ÍNDICE DEL")
    c.drawString(30, 428, "REPORTE")
    draw_wrapped(
        c,
        "La primera mitad presenta los hallazgos ejecutivos y la ubicación territorial. La segunda conserva los expedientes consultables, el método y el modelo de organización para actualizar la información desde fuentes oficiales.",
        30,
        392,
        58,
        10,
        13,
        GRIS,
    )
    c.setStrokeColor(DORADO)
    c.setLineWidth(3)
    c.line(30, 294, 318, 294)
    c.setFillColor(GUINDA)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(30, 271, "CLAVE METODOLÓGICA")
    draw_wrapped(
        c,
        "Los registros en $0.00 o “No integrado” aparecen porque ubican una controversia, pero no se suman cuando no existe una cantidad económica positiva fijada, confirmada o modificada para agregar al cálculo.",
        30,
        249,
        62,
        8.6,
        11,
        GRIS,
    )
    items = [
        ("01", "QUÉ SE SANCIONÓ", "Causas por monto observado, contexto legislativo y lectura de la sumatoria.", "3"),
        ("02", "MAPA DE INCIDENCIAS", "Entidades y distritos con controversias ubicables en el corte.", "4"),
        ("03", "EXPEDIENTES CONSULTABLES", "Tabla con expediente, sala, entidad, conducta, monto y URL oficial TEPJF.", "5-7"),
        ("04", "MODELO DE TRABAJO", "Organización propuesta para compilar criterios y alimentar la app en tiempo real.", "8"),
        ("05", "FUENTES Y MÉTODO", "Corpus, delimitación, referencias oficiales y alcance del corte.", "9"),
    ]
    x = 392
    y = 505
    c.setStrokeColor(NEGRO)
    c.setLineWidth(4)
    c.line(x, y + 18, W - 30, y + 18)
    for number, title, desc, page in items:
        c.setStrokeColor(LINEA)
        c.setLineWidth(0.7)
        c.line(x, y - 18, W - 30, y - 18)
        c.setFillColor(GUINDA)
        c.setFont("Helvetica-Bold", 15)
        c.drawString(x, y, number)
        c.setFont("Helvetica-Bold", 12.5)
        c.drawString(x + 50, y + 2, title)
        c.setFillColor(GRIS)
        c.setFont("Helvetica-Bold", 7.6)
        c.drawString(x + 50, y - 13, desc)
        c.setFillColor(NEGRO)
        c.setFont("Helvetica-Bold", 15)
        c.drawRightString(W - 30, y + 1, page)
        y -= 48
    footer(c, 2, 9)
    c.setFillColor(GUINDA)
    c.save()
    buffer.seek(0)
    return PdfReader(buffer)


def page3_page() -> PdfReader:
    c, buffer = overlay_canvas()
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(GUINDA)
    c.rect(30, H - 42, 304, 7, stroke=0, fill=1)
    c.setFillColor(DORADO)
    c.rect(334, H - 42, 66, 7, stroke=0, fill=1)
    c.setFillColor(NEGRO)
    c.rect(400, H - 42, W - 430, 7, stroke=0, fill=1)
    c.setFillColor(GUINDA)
    c.setFont("Helvetica-Bold", 8.2)
    c.drawString(30, 518, "OBSERVATORIO DE FISCALIZACIÓN ELECTORAL · PROCESO FEDERAL 2023-2024")
    c.setFillColor(NEGRO)
    c.setFont("Helvetica-Bold", 29)
    for y, line in zip([478, 444, 410, 376], ["QUÉ SE SANCIONÓ EN", "LAS ELECCIONES DE", "DIPUTACIONES", "FEDERALES 2024"]):
        c.drawString(30, y, line)
    draw_wrapped(
        c,
        "Reporte construido desde expedientes, registros de sanción del INE y hallazgos oficiales. Los $20.7 M corresponden a la suma de montos originales observados por el INE en 15 registros cuantificados relacionados con los expedientes base.",
        460,
        482,
        50,
        10.5,
        14,
        GRIS,
    )
    c.setStrokeColor(NEGRO)
    c.setLineWidth(4)
    c.line(30, 338, W - 30, 338)
    metrics = [
        ("7", "expedientes base con sentencia TEPJF", GUINDA),
        ("19", "registros de sanción del INE", DORADO),
        ("$20.7 M", "monto observado por el INE", VERDE),
        ("$19.7 M", "monto firme identificado en este corte", GUINDA),
    ]
    for i, (value, label, color) in enumerate(metrics):
        x = 30 + i * 188
        c.setStrokeColor(color)
        c.setLineWidth(4)
        c.line(x, 310, x, 252)
        c.setFillColor(GUINDA)
        c.setFont("Helvetica-Bold", 22)
        c.drawString(x + 12, 288, value)
        draw_wrapped(c, label.upper(), x + 12, 272, 30, 6.6, 7.4, GRIS, "Helvetica-Bold")
    c.setStrokeColor(NEGRO)
    c.setLineWidth(3)
    c.line(30, 228, 372, 228)
    c.line(404, 228, W - 30, 228)
    c.setFillColor(NEGRO)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(30, 202, "CAUSAS POR MONTO OBSERVADO")
    c.drawString(30, 181, "POR EL INE")
    causes = [
        ("REBASE POR PAGO EN EFECTIVO A REPRESENTANTES DE CASILLA", "$7.5 M", 1.0),
        ("OMISIÓN DE PRESENTAR XML", "$6.3 M", 0.84),
        ("DOCUMENTACIÓN SOPORTE FALTANTE", "$1.4 M", 0.19),
        ("COMPROBANTES FISCALES XML FALTANTES", "$1.3 M", 0.17),
        ("PROPAGANDA EN INTERNET FEDERAL NO REPORTADA", "$1.3 M", 0.17),
    ]
    y = 152
    for label, value, width in causes:
        c.setStrokeColor(LINEA)
        c.setLineWidth(0.6)
        c.line(30, y + 17, 372, y + 17)
        draw_wrapped(c, label, 30, y + 4, 38, 6.9, 7.4, TEXTO, "Helvetica-Bold")
        c.setFillColor("#E8D9C4")
        c.rect(196, y + 3, 112, 7, stroke=0, fill=1)
        c.setFillColor(GUINDA)
        c.rect(196, y + 3, 112 * width, 7, stroke=0, fill=1)
        c.setFillColor(GUINDA)
        c.setFont("Helvetica-Bold", 10)
        c.drawRightString(372, y + 3, value)
        y -= 27
    c.setFillColor(NEGRO)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(404, 202, "CONTEXTO LEGISLATIVO")
    context = [("365", "curules Morena · PVEM · PT", GUINDA), ("107", "curules PAN · PRI", DORADO)]
    for i, (value, label, color) in enumerate(context):
        x = 404 + i * 180
        c.setStrokeColor(color)
        c.setLineWidth(4)
        c.line(x, 174, x, 132)
        c.setFillColor(GUINDA)
        c.setFont("Helvetica-Bold", 24)
        c.drawString(x + 12, 150, value)
        draw_wrapped(c, label.upper(), x + 12, 134, 30, 6.8, 7.4, GRIS, "Helvetica-Bold")
    parties = [("MORENA", 253, GUINDA), ("PAN", 70, "#2B5C8A"), ("PVEM", 63, VERDE), ("PT", 49, DORADO), ("PRI", 37, "#8A1F2D"), ("MC", 28, "#FF6600")]
    y = 110
    for party, seats, color in parties:
        c.setFillColor(TEXTO)
        c.setFont("Helvetica-Bold", 7.8)
        c.drawString(404, y, party)
        c.setFillColor("#E8D9C4")
        c.rect(456, y - 1, 232, 8, stroke=0, fill=1)
        c.setFillColor(color)
        c.rect(456, y - 1, 232 * seats / 253, 8, stroke=0, fill=1)
        c.setFillColor(GUINDA)
        c.setFont("Helvetica-Bold", 10)
        c.drawRightString(742, y - 1, str(seats))
        y -= 16
    footer(c, 3, 9)
    c.save()
    buffer.seek(0)
    return PdfReader(buffer)


def model_page() -> PdfReader:
    c, buffer = overlay_canvas()
    c.setFillColor("white")
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(GUINDA)
    c.rect(30, H - 42, 284, 7, stroke=0, fill=1)
    c.setFillColor(DORADO)
    c.rect(314, H - 42, 62, 7, stroke=0, fill=1)
    c.setFillColor(NEGRO)
    c.rect(376, H - 42, W - 406, 7, stroke=0, fill=1)
    c.setFillColor(NEGRO)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(30, 536, "MODELO DE TRABAJO PARA FISCALIZACIÓN")
    c.setFillColor(GUINDA)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(30, 496, "MODELO INSTITUCIONAL DE ACTUALIZACIÓN")
    c.setFillColor(NEGRO)
    c.setFont("Helvetica-Bold", 32)
    c.drawString(30, 462, "DE LA FUENTE OFICIAL")
    c.drawString(30, 426, "AL CORTE VERIFICABLE")
    draw_wrapped(
        c,
        "El Observatorio puede operar como una cadena documental: cada expediente se incorpora desde una fuente oficial, se contrasta con el dictamen o resolución administrativa y se transforma en un dato verificable antes de alimentar la app, la sumatoria y el PDF. La lógica editorial conserva la distinción entre controversias localizables y cantidades positivas que sí pueden agregarse.",
        392,
        406,
        70,
        9.2,
        12.2,
        GRIS,
    )
    cards = [
        ("1. DICTAMEN Y RESOLUCIÓN", "El punto de entrada son los actos de fiscalización de campaña federal 2023-2024. El modelo conserva la clave administrativa, la conclusión revisada, la conducta observada y el expediente jurisdiccional que confirmó, modificó o revocó el análisis."),
        ("2. CRITERIOS JURISDICCIONALES", "Los criterios se ordenan por órgano, tema y efecto: gasto no reportado, soporte documental, propaganda, rebase, aportaciones prohibidas, competencia y alcance de la revocación. Cada regla se mantiene vinculada a su fuente oficial."),
        ("3. BASE VIVA DE CONSULTA", "La app debe leer una matriz única con expediente, URL oficial, acto de origen, sujeto obligado, candidatura vinculada, entidad, distrito, monto positivo, estado de validación y efecto. Así el reporte se actualiza sin rehacer la narrativa."),
    ]
    for i, (title, body) in enumerate(cards):
        x = 30 + i * 245
        c.setStrokeColor(DORADO)
        c.setLineWidth(4)
        c.line(x, 338, x + 210, 338)
        c.setFillColor(GUINDA)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x, 316, title)
        draw_wrapped(c, body, x, 294, 40, 8.2, 10.6, GRIS, "Helvetica-Bold")
    steps = ["Fuente oficial", "Texto extraído", "Criterio validado", "Matriz normalizada", "App y PDF"]
    for i, step in enumerate(steps):
        x = 30 + i * 148
        c.setStrokeColor(LINEA)
        c.setLineWidth(1)
        c.rect(x, 126, 128, 42, stroke=1, fill=0)
        c.setStrokeColor(GUINDA)
        c.setLineWidth(3)
        c.line(x, 168, x + 128, 168)
        draw_wrapped(c, step.upper(), x + 8, 148, 22, 7.6, 9, GUINDA, "Helvetica-Bold")
    stats = [
        ("11", "sentencias del corpus con marca de fiscalización"),
        ("7", "expedientes base ligados a registros de sanción"),
        ("5", "incidencias ubicables por entidad o distrito"),
        ("$20,700,473.59", "sumatoria exacta de montos positivos observados"),
    ]
    for i, (value, label) in enumerate(stats):
        x = 30 + i * 185
        c.setStrokeColor(LINEA)
        c.setLineWidth(1)
        c.line(x, 89, x + 152, 89)
        c.setFillColor(GUINDA)
        c.setFont("Helvetica-Bold", 14 if i < 3 else 10)
        c.drawString(x, 66, value)
        draw_wrapped(c, label.upper(), x, 52, 28, 6.4, 7, GRIS, "Helvetica-Bold")
    footer(c, 8, 9)
    c.save()
    buffer.seek(0)
    return PdfReader(buffer)


def main() -> None:
    reader = PdfReader(str(BASE))
    writer = PdfWriter()
    overlays = {
    }
    replacement_cover = page1_page().pages[0]
    replacement_index = page2_page().pages[0]
    replacement_summary = page3_page().pages[0]
    replacement_model = model_page().pages[0]
    for idx, page in enumerate(reader.pages):
        if idx == 0:
            writer.add_page(replacement_cover)
            continue
        if idx == 1:
            writer.add_page(replacement_index)
            continue
        if idx == 2:
            writer.add_page(replacement_summary)
            continue
        if idx == 7:
            writer.add_page(replacement_model)
            continue
        if idx in overlays:
            page.merge_page(overlays[idx])
        writer.add_page(page)
    with OUT.open("wb") as f:
        writer.write(f)
    print(OUT)


if __name__ == "__main__":
    main()
