import sys
from pathlib import Path

from .azure_tts import text_to_mp3
from .audio_merger import merge_mp3s
from .chunker import split_text
from .epub_parser import extract_chapters


def convert(epub_path: str, output_dir: str = "output"):
    chapters = extract_chapters(epub_path)
    if not chapters:
        raise RuntimeError("Nessun capitolo leggibile trovato nell'EPUB")

    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    chapter_files = []

    for chapter_index, chapter in enumerate(chapters, 1):
        chapter_dir = root / f"{chapter_index:03d}"
        chunks = split_text(chapter["text"])
        files = []
        for chunk_index, chunk in enumerate(chunks, 1):
            out = chapter_dir / f"{chunk_index:04d}.mp3"
            if not out.exists():
                text_to_mp3(chunk, str(out))
            files.append(str(out))
        chapter_mp3 = root / f"{chapter_index:03d}-{chapter['title'][:60]}.mp3"
        merge_mp3s(files, str(chapter_mp3))
        chapter_files.append(str(chapter_mp3))

    merge_mp3s(chapter_files, str(root / "audiobook.mp3"))
    return str(root / "audiobook.mp3")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Uso: python -m app.main libro.epub")
    print(convert(sys.argv[1]))
