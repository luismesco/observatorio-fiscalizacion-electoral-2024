from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "documents" / "federal" / "tepjf_html"
OUT_DIR = ROOT / "data" / "interim" / "extracted_text"


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
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
    for path in SOURCE_DIR.glob("*.html"):
        if "Captcha" in path.read_text(errors="ignore")[:500]:
            continue
        text = html_to_text(path.read_text(errors="ignore"))
        (OUT_DIR / f"{path.stem}.txt").write_text(text, encoding="utf-8")
        print(f"{path.name}: {len(text):,} chars")


if __name__ == "__main__":
    main()

