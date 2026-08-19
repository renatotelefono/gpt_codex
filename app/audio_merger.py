from pathlib import Path
import subprocess


# Percorso di FFmpeg sul tuo PC
FFMPEG_PATH = r"C:\Users\HP\Desktop\programmi_rt\ffmpeg\bin\ffmpeg.exe"

# Cartella principale dei file generati
OUTPUT_DIR = Path("output")

# File finale
AUDIOBOOK_FILE = OUTPUT_DIR / "audiobook.mp3"


def find_mp3_files():
    """
    Trova tutti gli MP3 presenti nelle sottocartelle di output.

    audiobook.mp3 viene escluso per evitare di includerlo
    nuovamente nella fusione.
    """

    files = sorted(
        file
        for file in OUTPUT_DIR.glob("*/*.mp3")
        if file.is_file()
    )

    return files


def merge_mp3_files(input_files, output_file):
    """
    Unisce tutti i file MP3 usando FFmpeg.
    """

    if not input_files:
        raise RuntimeError(
            "Nessun file MP3 trovato."
        )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    concat_file = OUTPUT_DIR / "concat.txt"

    # Crea la lista utilizzata da FFmpeg
    with open(
        concat_file,
        "w",
        encoding="utf-8"
    ) as f:

        for file in input_files:

            path = file.resolve().as_posix()

            f.write(
                f"file '{path}'\n"
            )

    try:

        command = [
            FFMPEG_PATH,

            "-y",

            "-f",
            "concat",

            "-safe",
            "0",

            "-i",
            str(concat_file),

            "-c",
            "copy",

            str(output_file),
        ]

        print()
        print("Avvio FFmpeg...")
        print()

        subprocess.run(
            command,
            check=True
        )

    finally:

        # Elimina il file temporaneo
        if concat_file.exists():
            concat_file.unlink()


def main():

    print()
    print("================================")
    print("     EPUB TO AUDIO - MERGER")
    print("================================")
    print()

    # Controlla FFmpeg
    if not Path(FFMPEG_PATH).exists():

        raise RuntimeError(
            f"FFmpeg non trovato:\n{FFMPEG_PATH}"
        )

    # Controlla output
    if not OUTPUT_DIR.exists():

        raise RuntimeError(
            "La cartella output non esiste."
        )

    # Trova gli MP3
    mp3_files = find_mp3_files()

    if not mp3_files:

        raise RuntimeError(
            "Nessun file MP3 trovato nelle cartelle di output."
        )

    print(
        f"Trovati {len(mp3_files)} file MP3."
    )

    print()
    print("File che verranno uniti:")

    for index, file in enumerate(
        mp3_files,
        start=1
    ):
        print(
            f"{index:04d}. {file}"
        )

    print()
    print(
        f"Output: {AUDIOBOOK_FILE}"
    )

    # Fusione
    merge_mp3_files(
        mp3_files,
        AUDIOBOOK_FILE
    )

    print()
    print("================================")
    print("      AUDIOBOOK COMPLETATO")
    print("================================")
    print()
    print(
        f"File creato:\n{AUDIOBOOK_FILE.resolve()}"
    )
    print()


if __name__ == "__main__":
    main()