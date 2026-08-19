import subprocess
from pathlib import Path


def merge_mp3s(files: list[str], output_file: str):
    if not files:
        raise ValueError("Nessun MP3 da unire")
    manifest = Path(output_file).with_suffix(".txt")
    manifest.write_text("".join(f"file '{Path(f).resolve()}'\n" for f in files), encoding="utf-8")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(manifest), "-c", "copy", output_file,
    ], check=True)
    manifest.unlink(missing_ok=True)
    return output_file
