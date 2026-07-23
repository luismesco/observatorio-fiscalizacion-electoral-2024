from __future__ import annotations

import csv
import re
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "interim" / "tepjf_diputaciones_2023_2024_manifest.csv"
OUT_DIR = ROOT / "data" / "interim" / "diputaciones_2023_2024_text"


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


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with MANIFEST.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if not row["status"].startswith("descargado"):
                continue
            source = ROOT / row["filename"]
            text = html_to_text(source.read_text(encoding="utf-8", errors="ignore"))
            out = OUT_DIR / f"{Path(row['filename']).stem}.txt"
            out.write_text(text, encoding="utf-8")
            print(f"{row['expediente']}: {len(text):,} chars")


if __name__ == "__main__":
    main()
