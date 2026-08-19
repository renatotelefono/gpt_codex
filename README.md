# EPUB to Audio

MVP Python per convertire un EPUB in audiobook MP3 usando Azure Speech.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Compila `.env` con `SPEECH_KEY` e `SPEECH_REGION` di Azure Speech.

È necessario avere `ffmpeg` installato e disponibile nel PATH.

## Uso

```bash
python -m app.main libro.epub
```

Il risultato viene creato in `output/audiobook.mp3`, con MP3 intermedi per capitolo.
