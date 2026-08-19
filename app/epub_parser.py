from pathlib import Path

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup


def extract_chapters(epub_path: str):
    book = epub.read_epub(epub_path)

    chapters = []

    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_content(), "html.parser")

        # Eliminiamo elementi non utili alla lettura
        for tag in soup(["script", "style", "nav"]):
            tag.decompose()

        text = soup.get_text("\n")

        # Pulizia righe vuote
        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        text = "\n".join(lines)

        if len(text) < 100:
            continue

        title = None

        heading = soup.find(["h1", "h2", "h3"])

        if heading:
            title = heading.get_text(" ", strip=True)

        if not title:
            title = Path(item.get_name()).stem

        chapters.append({
            "id": item.get_id(),
            "title": title,
            "text": text,
        })

    return chapters