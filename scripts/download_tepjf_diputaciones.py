from __future__ import annotations

import csv
import hashlib
import re
import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "documents" / "diputaciones_2023_2024" / "tepjf_html"
MANIFEST = ROOT / "data" / "interim" / "tepjf_diputaciones_2023_2024_manifest.csv"
LOCAL_CACHE = ROOT / "documents" / "federal" / "tepjf_html"
ALT_CACHE = {
    "SUP-RAP-352/2024": "SUP-RAP-0352-2024.html",
    "SUP-RAP-357/2024": "SUP-RAP-0357-2024.html",
    "SUP-RAP-413/2024": "SUP-RAP-0413-2024.html",
}


@dataclass(frozen=True)
class Target:
    expediente: str
    year: int
    url: str
    tema: str


TARGETS = [
    Target("SUP-JDC-427/2023", 2023, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-JDC-0427-2023", "reeleccion legislativa"),
    Target("SUP-JDC-550/2023", 2023, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-JDC-0550-2023", "reeleccion legislativa"),
    Target("SUP-RAP-385/2023", 2023, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-RAP-385-2023", "asignacion rp"),
    Target("SUP-OP-4/2023", 2023, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-OP-0004-2023-", "opinion constitucional"),
    Target("SUP-JDC-296/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-JDC-0296-2024-", "seleccion interna rp"),
    Target("SUP-JDC-414/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-JDC-0414-2024-", "seleccion interna rp"),
    Target("SUP-JDC-559/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-JDC-0559-2024-", "seleccion interna rp"),
    Target("SUP-JDC-606/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-JDC-0606-2024", "seleccion interna rp"),
    Target("SUP-JDC-798/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-JDC-0798-2024-", "seleccion interna rp"),
    Target("SUP-JDC-858/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-JDC-0858-2024-", "seleccion interna"),
    Target("SUP-AG-182/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-AG-0182-2024-", "asignacion rp irreparable"),
    Target("SUP-AG-184/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-AG-0184-2024-", "integracion camara"),
    Target("SUP-AG-193/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-AG-0193-2024-", "asignacion rp irreparable"),
    Target("SUP-RAP-103/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-RAP-0103-2024-", "registro y rp"),
    Target("SUP-RAP-342/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-RAP-0342-2024", "fiscalizacion federal"),
    Target("SUP-RAP-352/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-RAP-0352-2024-", "fiscalizacion federal"),
    Target("SUP-RAP-357/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-RAP-0357-2024-", "fiscalizacion federal"),
    Target("SUP-RAP-413/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-RAP-0413-2024-", "fiscalizacion federal"),
    Target("SUP-RAP-414/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-RAP-0414-2024-Acuerdo1", "competencia fiscalizacion candidato"),
    Target("SUP-RAP-415/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-RAP-0415-2024-Acuerdo1", "competencia fiscalizacion candidato"),
    Target("SUP-REC-761/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-REC-0761-2024-", "reconsideracion jin"),
    Target("SUP-REC-763/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-REC-0763-2024-", "reconsideracion jin"),
    Target("SUP-REC-764/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-REC-0764-2024-", "reconsideracion jin"),
    Target("SUP-REC-1142/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-REC-1142-2024", "reconsideracion jin"),
    Target("SUP-REC-4505/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-REC-4505-2024-", "asignacion rp"),
    Target("SUP-REC-6450/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-REC-6450-2024-", "asignacion rp"),
    Target("SCM-JIN-27/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SCM-JIN-0027-2024-", "jin computo distrital"),
    Target("SCM-JIN-30/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SCM-JIN-0030-2024-", "jin computo distrital"),
    Target("SCM-JIN-56/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SCM-JIN-0056-2024-", "jin computo distrital"),
    Target("SCM-JIN-103/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SCM-JIN-0103-2024-", "jin computo distrital"),
    Target("SCM-RAP-47/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SCM-RAP-0047-2024-", "fiscalizacion candidato"),
    Target("SG-JDC-111/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SG-JDC-0111-2024-", "registro candidatura"),
    Target("SG-JIN-10/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SG-JIN-0010-2024-", "jin computo distrital"),
    Target("SG-JIN-143/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SG-JIN-0143-2024-", "jin computo distrital"),
    Target("SG-JIN-147/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SG-JIN-0147-2024-", "jin computo distrital"),
    Target("SG-JRC-221/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SG-JRC-0221-2024-", "diputaciones locales sonora"),
    Target("SM-AG-39/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SM-AG-0039-2024-Acuerdo1", "encauzamiento computo distrital"),
    Target("SM-JDC-132/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SM-JDC-0132-2024-", "sustitucion candidatura"),
    Target("SM-JIN-11/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SM-JIN-0011-2024-", "jin computo distrital"),
    Target("SM-JIN-58/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SM-JIN-0058-2024-", "jin computo distrital"),
    Target("SM-JIN-82/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SM-JIN-0082-2024-", "jin computo distrital"),
    Target("SM-JIN-109/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SM-JIN-0109-2024-", "jin computo distrital"),
    Target("SM-JIN-146/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SM-JIN-0146-2024-", "jin computo distrital"),
    Target("ST-JDC-69/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/ST-JDC-0069-2024-", "registro precandidatura"),
    Target("ST-JIN-85/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/ST-JIN-0085-2024-", "jin computo distrital"),
    Target("ST-RAP-50/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/ST-RAP-0050-2024-", "fiscalizacion precandidatura"),
    Target("ST-RAP-74/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/ST-RAP-0074-2024-", "fiscalizacion candidato"),
    Target("SRE-PSC-565/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SRE-PSC-0565-2024-", "diputada federal"),
    Target("SRE-PSD-36/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SRE-PSD-0036-2024-", "propaganda candidata diputada federal"),
    Target("SRE-PSD-80/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SRE-PSD-0080-2024-", "propaganda candidato diputado federal"),
    Target("SRE-PSD-85/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SRE-PSD-0085-2024-", "propaganda candidato diputado federal"),
    Target("SRE-PSD-87/2024", 2024, "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SRE-PSD-0087-2024-", "propaganda candidato diputado federal"),
]


def filename_for(target: Target) -> str:
    parsed = urlparse(target.url)
    slug = Path(parsed.path).name
    if not slug:
        slug = re.sub(r"[^A-Za-z0-9-]+", "-", target.expediente)
    return f"{slug}.html"


def status_for(path: Path) -> str:
    if not path.exists():
        return "no_descargado"
    text = path.read_text(encoding="utf-8", errors="ignore")[:1000]
    if "Radware Bot Manager Captcha" in text or "Captcha Page" in text:
        return "captcha_portal"
    if len(text.strip()) < 100:
        return "descarga_vacia"
    return "descargado"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else ""


def cached_source(target: Target, out: Path) -> Path | None:
    candidates = [LOCAL_CACHE / out.name]
    if target.expediente in ALT_CACHE:
        candidates.append(LOCAL_CACHE / ALT_CACHE[target.expediente])
    for path in candidates:
        if path.exists() and status_for(path) == "descargado":
            return path
    return None


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for target in TARGETS:
        out = OUT_DIR / filename_for(target)
        cache = cached_source(target, out)
        if cache is not None:
            shutil.copy2(cache, out)
            proc_returncode = 0
        else:
            cmd = ["curl", "-L", "--max-time", "45", target.url, "-o", str(out)]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            proc_returncode = proc.returncode
        state = status_for(out)
        rows.append(
            {
                "expediente": target.expediente,
                "year": target.year,
                "tema": target.tema,
                "url": target.url,
                "filename": str(out.relative_to(ROOT)),
                "returncode": proc_returncode,
                "status": state,
                "file_size": out.stat().st_size if out.exists() else 0,
                "sha256": sha256(out),
            }
        )
        print(f"{target.expediente}: {state}")
        time.sleep(0.6)

    with MANIFEST.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(MANIFEST)


if __name__ == "__main__":
    main()
