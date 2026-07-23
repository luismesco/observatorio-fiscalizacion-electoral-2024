from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "interim" / "tepjf_diputaciones_2023_2024_manifest.csv"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else ""


def status_for(path: Path) -> str:
    if not path.exists():
        return "no_descargado"
    text = path.read_text(encoding="utf-8", errors="ignore")
    head = text[:2000].lower()
    if "radware bot manager captcha" in head or "captcha page" in head:
        return "captcha_portal"
    if len(text.strip()) < 1000:
        return "descarga_sospechosa"
    return "descargado_chrome"


def main() -> None:
    with MANIFEST.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        path = ROOT / row["filename"]
        row["status"] = status_for(path)
        row["file_size"] = str(path.stat().st_size if path.exists() else 0)
        row["sha256"] = sha256(path)
        row["returncode"] = "0" if row["status"].startswith("descargado") else row["returncode"]
    with MANIFEST.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(MANIFEST)


if __name__ == "__main__":
    main()
