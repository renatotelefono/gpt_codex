import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup


def extract_chapters(epub_path: str):
    book = epub.read_epub(epub_path)
    chapters = []

    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_content(), "html.parser")
        for tag in soup(["script", "style", "nav"]):
            tag.decompose()

        heading = soup.find(["h1", "h2", "h3"])
        title = heading.get_text(" ", strip=True) if heading else item.get_name()
        text = "\n\n".join(
            p.get_text(" ", strip=True)
            for p in soup.find_all(["p", "div", "section"])
            if p.get_text(" ", strip=True)
        )
        if len(text) >= 100:
            chapters.append({"id": item.get_id(), "title": title, "text": text})

    return chapters
