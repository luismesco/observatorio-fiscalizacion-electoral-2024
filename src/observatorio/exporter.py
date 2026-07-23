from __future__ import annotations

from pathlib import Path

import pandas as pd
from openpyxl.styles import Font, PatternFill

from .data_loader import load_all
from .paths import export_dir, project_root


EXTRA_EXPORTS = {
    "tepjf_descargas": "data/interim/tepjf_diputaciones_2023_2024_manifest.csv",
    "tepjf_resumen": "data/analysis/tepjf_corpus_resumen.csv",
    "tepjf_fragmentos": "data/analysis/tepjf_corpus_fragmentos.csv",
    "tepjf_personas": "data/analysis/tepjf_personas_detectadas.csv",
    "ganadores_constancia": "data/analysis/ganadores_constancia.csv",
    "diputaciones_lxvi": "data/analysis/diputados_lxvi_electos.csv",
    "tfja_fisel": "data/analysis/tfja_fisel_screening.csv",
}


def export_excel(output_path: Path | None = None) -> Path:
    tables = load_all()
    path = output_path or export_dir() / "observatorio_mvp.xlsx"
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        pd.DataFrame(
            {
                "campo": ["advertencia", "uso", "revision"],
                "valor": [
                    "Corte de trabajo con fuentes oficiales y trazabilidad documental.",
                    "Usar las hojas de sentencias, diputaciones LXVI y verificacion nominal como base del observatorio.",
                    "Todo dato publicado debe conservar fuente, fragmento y estado de revision.",
                ],
            }
        ).to_excel(writer, sheet_name="LEEME", index=False)
        for name, df in tables.items():
            sheet = name[:31]
            df.to_excel(writer, sheet_name=sheet, index=False)
        for name, relative_path in EXTRA_EXPORTS.items():
            path_extra = project_root() / relative_path
            if path_extra.exists():
                pd.read_csv(path_extra, keep_default_na=False).to_excel(writer, sheet_name=name[:31], index=False)

        for sheet in writer.book.worksheets:
            sheet.freeze_panes = "A2"
            for cell in sheet[1]:
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = PatternFill("solid", fgColor="163A3F")
            for column_cells in sheet.columns:
                max_length = max(len(str(cell.value or "")) for cell in column_cells)
                sheet.column_dimensions[column_cells[0].column_letter].width = min(max(max_length + 2, 12), 55)
    return path
