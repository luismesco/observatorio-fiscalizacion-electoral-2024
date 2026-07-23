from __future__ import annotations

import csv
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SEARCH_LOG = ROOT / "exports" / "tepjf_bitacora_busquedas_chrome.json"
HTML_DIR = ROOT / "documents" / "diputaciones_2023_2025" / "tepjf_html"
TEXT_DIR = ROOT / "data" / "interim" / "diputaciones_2023_2025_text"
PREVIOUS_TEXT_DIRS = [
    ROOT / "data" / "interim" / "tepjf_revision_2025_text",
]
MANIFEST = ROOT / "data" / "interim" / "tepjf_diputaciones_2023_2025_exhaustive_manifest.csv"
SUMMARY = ROOT / "exports" / "tepjf_bitacora_descarga_exhaustiva_resumen.csv"


STATIC_CANDIDATES = [
    ("SM-RAP-0046-2024-", "busqueda indexada fiscalizacion precampana"),
    ("SG-RAP-0028-2024-", "busqueda indexada fiscalizacion precampana"),
    ("SCM-RAP-0099-2024-", "busqueda indexada fiscalizacion campana"),
    ("SUP-RAP-0088-2024-", "busqueda indexada fiscalizacion precampana"),
    ("SX-RAP-0064-2024-", "busqueda indexada fiscalizacion precampana"),
    ("ST-RAP-0016-2024-", "busqueda indexada fiscalizacion precampana"),
    ("SUP-RAP-0455-2024", "busqueda indexada fiscalizacion SIF"),
    ("SRE-PSD-0043-2024-", "busqueda indexada propaganda candidato diputado federal"),
    ("SRE-PSC-0492-2024-", "busqueda indexada propaganda federal"),
    ("SRE-PSD-0088-2024-", "busqueda indexada propaganda candidato diputado federal"),
    ("SRE-PSL-0062-2024-", "busqueda indexada propaganda diputado federal"),
    ("SX-JDC-0167-2024-", "busqueda indexada registro diputacion federal"),
    ("SM-JDC-0093-2024-", "busqueda indexada registro diputacion federal"),
    ("SM-JIN-0091-2024-Acuerdo1", "busqueda indexada computo distrital"),
    ("SUP-RAP-0104-2025-", "busqueda indexada cumplimiento fiscalizacion 2025"),
    ("SUP-RAP-0018-2025-", "candidato 2025 fiscalizacion"),
    ("SUP-RAP-0108-2025-", "candidato 2025 fiscalizacion"),
]


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in {"script", "style"}:
            self.skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style"} and self.skip_depth:
            self.skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        clean = data.replace("\xa0", " ").strip()
        if clean:
            self.parts.append(clean)


def html_to_text(raw: str) -> str:
    parser = TextExtractor()
    parser.feed(raw)
    text = "\n".join(parser.parts)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def expediente_from_slug(slug: str) -> str:
    clean = slug.removesuffix("-")
    return re.sub(
        r"^(.*)-(\d{4})-(\d{4})(.*)$",
        lambda m: f"{m.group(1)}-{int(m.group(2))}/{m.group(3)}{m.group(4)}",
        clean,
    )


def candidate_from_slug(slug: str, source: str, query: str) -> dict[str, str | int]:
    year = int(re.findall(r"\d{4}", slug)[-1])
    return {
        "expediente": expediente_from_slug(slug),
        "year": year,
        "url": f"https://www.te.gob.mx/sentenciasHTML/convertir/expediente/{slug}",
        "discovery_source": source,
        "query": query,
    }


def search_candidates() -> list[dict[str, str | int]]:
    candidates: list[dict[str, str | int]] = []
    if SEARCH_LOG.exists():
        log = json.loads(SEARCH_LOG.read_text(encoding="utf-8"))
        for run in log.get("runs", []):
            for row in run.get("rows", []):
                match = re.match(r"^([A-Z]+-[A-Z]+-\d{4}-\d{4}(?:-Acuerdo\d+)?)", row)
                if match:
                    candidates.append(candidate_from_slug(match.group(1) + "-", "TEPJF buscador", run["query"]))
    for slug, source in STATIC_CANDIDATES:
        candidates.append(candidate_from_slug(slug, source, source))

    deduped: dict[str, dict[str, str | int]] = {}
    for candidate in candidates:
        deduped.setdefault(str(candidate["url"]), candidate)
    return list(deduped.values())


def status_for(html: str) -> str:
    head = html[:5000].lower()
    if "radware bot manager captcha" in head or "captcha page" in head or "h-captcha" in head:
        return "captcha_portal"
    if "falta número de expediente" in head or "falta numero de expediente" in head:
        return "expediente_no_resuelto"
    if len(html.strip()) < 1500:
        return "descarga_sospechosa"
    return "descargado_chrome"


def previous_text_for(slug: str) -> str:
    stem = slug.removesuffix("-")
    candidates = [stem, stem.replace("-0", "-")]
    for directory in PREVIOUS_TEXT_DIRS:
        for candidate in candidates:
            path = directory / f"{candidate}.txt"
            if path.exists():
                return path.read_text(encoding="utf-8", errors="ignore")
    return ""


def main() -> None:
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for candidate in search_candidates():
        slug = Path(str(candidate["url"])).name
        filename = HTML_DIR / f"{slug}.html"
        html = filename.read_text(encoding="utf-8", errors="ignore") if filename.exists() else ""
        text = html_to_text(html) if html else ""
        status = status_for(html) if html else "pendiente_descarga_portal"
        if not html:
            previous_text = previous_text_for(slug)
            if previous_text:
                text = previous_text
                status = "descargado_texto_previo"
        if status.startswith("descargado"):
            (TEXT_DIR / f"{filename.stem}.txt").write_text(text, encoding="utf-8")
        rows.append(
            {
                **candidate,
                "filename": str(filename.relative_to(ROOT)),
                "status": status,
                "file_size": filename.stat().st_size if filename.exists() else 0,
                "sha256": hashlib.sha256(html.encode("utf-8")).hexdigest() if html else "",
                "texto_chars": len(text),
                "nota": "descargada y extraida" if status.startswith("descargado") else "requiere reintento manual o sesion de navegador estable",
            }
        )

    with MANIFEST.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    counts: dict[str, int] = {}
    for row in rows:
        counts[str(row["status"])] = counts.get(str(row["status"]), 0) + 1
    with SUMMARY.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["metric", "value"])
        writer.writeheader()
        writer.writerow({"metric": "candidatos_unicos", "value": len(rows)})
        for status, count in sorted(counts.items()):
            writer.writerow({"metric": status, "value": count})
    print(MANIFEST)
    print(SUMMARY)


if __name__ == "__main__":
    main()
