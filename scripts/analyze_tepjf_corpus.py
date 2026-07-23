from __future__ import annotations

import csv
import re
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "interim" / "tepjf_diputaciones_2023_2024_manifest.csv"
TEXT_DIR = ROOT / "data" / "interim" / "diputaciones_2023_2024_text"
OUT_DIR = ROOT / "data" / "analysis"
SUMMARY_OUT = OUT_DIR / "tepjf_corpus_resumen.csv"
SNIPPETS_OUT = OUT_DIR / "tepjf_corpus_fragmentos.csv"
PERSONAS_OUT = OUT_DIR / "tepjf_personas_detectadas.csv"


KEYWORDS = {
    "constancia_mayoria": ["constancia de mayoría", "constancia de mayoria"],
    "fiscalizacion": ["fiscalización", "fiscalizacion", "INE/Q-COF", "dictamen consolidado"],
    "rebase_tope": ["rebase de tope", "tope de gastos"],
    "nulidad": ["nulidad de la elección", "nulidad de eleccion", "causal de nulidad"],
    "rp": ["representación proporcional", "representacion proporcional", "diputaciones federales de representación proporcional"],
    "inelegibilidad": ["inelegibilidad", "requisito de elegibilidad", "elegibilidad"],
    "propaganda": ["propaganda", "equipamiento urbano", "espectacular"],
}

SENTIDO_PATTERNS = [
    ("revoca", re.compile(r"\brevoca\b", re.I)),
    ("confirma", re.compile(r"\bconfirma\b", re.I)),
    ("desecha", re.compile(r"\bdesecha\b|\bdesechamiento\b", re.I)),
    ("sobresee", re.compile(r"\bsobresee\b|\bsobreseimiento\b", re.I)),
    ("modifica", re.compile(r"\bmodifica\b", re.I)),
]

PERSON_CONTEXT = re.compile(
    r"(?:candidat[ao]|diputad[ao]|precandidat[ao]|actor[ae]?|promovente|denunciad[ao]|recurrente)\s+"
    r"(?:a|o|federal|propietari[ao]|suplente|ciudadan[ao]|por)?\s*:?\s*"
    r"([A-ZÁÉÍÓÚÑ][A-Za-zÁÉÍÓÚÑáéíóúñ'.-]+(?:\s+[A-ZÁÉÍÓÚÑ][A-Za-zÁÉÍÓÚÑáéíóúñ'.-]+){1,5})"
)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def find_snippets(text: str, terms: list[str], window: int = 280) -> list[str]:
    snippets: list[str] = []
    lower = text.lower()
    for term in terms:
        start = 0
        term_l = term.lower()
        while True:
            idx = lower.find(term_l, start)
            if idx == -1:
                break
            snippets.append(normalize(text[max(0, idx - window) : idx + len(term) + window]))
            start = idx + len(term)
            if len(snippets) >= 5:
                return snippets
    return snippets


def sentido_probable(text: str) -> str:
    first = text[:5000]
    found = [label for label, pattern in SENTIDO_PATTERNS if pattern.search(first)]
    return " / ".join(found) if found else "no detectado"


def medio_from_expediente(expediente: str) -> str:
    match = re.search(r"-([A-Z]+)-", expediente)
    return match.group(1) if match else ""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = pd.read_csv(MANIFEST, keep_default_na=False)
    summaries = []
    snippets_rows = []
    personas = []
    for row in manifest.to_dict("records"):
        if not str(row["status"]).startswith("descargado"):
            continue
        stem = Path(row["filename"]).stem
        text_path = TEXT_DIR / f"{stem}.txt"
        if not text_path.exists():
            continue
        text = text_path.read_text(encoding="utf-8", errors="ignore")
        flags = {name: int(any(term.lower() in text.lower() for term in terms)) for name, terms in KEYWORDS.items()}
        summaries.append(
            {
                "expediente": row["expediente"],
                "year": row["year"],
                "tema_inventario": row["tema"],
                "medio": medio_from_expediente(row["expediente"]),
                "status": row["status"],
                "texto_chars": len(text),
                "sentido_probable": sentido_probable(text),
                **flags,
            }
        )
        for name, terms in KEYWORDS.items():
            for idx, snippet in enumerate(find_snippets(text, terms), start=1):
                snippets_rows.append(
                    {
                        "expediente": row["expediente"],
                        "categoria": name,
                        "numero": idx,
                        "fragmento": snippet,
                    }
                )
        for match in PERSON_CONTEXT.finditer(text[:30000]):
            persona = normalize(match.group(1)).strip(" .,:;")
            if len(persona.split()) >= 2:
                personas.append(
                    {
                        "expediente": row["expediente"],
                        "persona_detectada": persona,
                        "contexto": normalize(text[max(0, match.start() - 180) : match.end() + 180]),
                    }
                )

    pd.DataFrame(summaries).to_csv(SUMMARY_OUT, index=False)
    pd.DataFrame(snippets_rows).to_csv(SNIPPETS_OUT, index=False)
    pd.DataFrame(personas).drop_duplicates().to_csv(PERSONAS_OUT, index=False)
    print(SUMMARY_OUT)
    print(SNIPPETS_OUT)
    print(PERSONAS_OUT)


if __name__ == "__main__":
    main()
