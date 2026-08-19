import sys
from pathlib import Path

from epub_parser import extract_chapters
from chunker import split_text
from azure_tts import text_to_mp3


def main():
    if len(sys.argv) != 2:
        print("Uso:")
        print("python app/main.py libro.epub")
        sys.exit(1)

    epub_path = sys.argv[1]

    if not Path(epub_path).exists():
        print(f"File non trovato: {epub_path}")
        sys.exit(1)

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    print("Lettura EPUB...")

    chapters = extract_chapters(epub_path)

    print(f"Trovati {len(chapters)} capitoli.")

    for chapter_index, chapter in enumerate(chapters, start=1):

        print()
        print(
            f"[{chapter_index}/{len(chapters)}] "
            f"{chapter['title']}"
        )

        chunks = split_text(chapter["text"])

        chapter_dir = output_dir / f"{chapter_index:03d}"
        chapter_dir.mkdir(exist_ok=True)

        for chunk_index, chunk in enumerate(chunks, start=1):

            output_file = (
                chapter_dir /
                f"{chunk_index:04d}.mp3"
            )

            print(
                f"  → blocco "
                f"{chunk_index}/{len(chunks)}"
            )

            text_to_mp3(
                chunk,
                str(output_file),
            )

    print()
    print("Conversione completata.")


if __name__ == "__main__":
    main()
    