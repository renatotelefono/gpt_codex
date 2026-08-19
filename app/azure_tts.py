import os
from pathlib import Path

import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()


SPEECH_KEY = os.getenv("SPEECH_KEY")
SPEECH_REGION = os.getenv("SPEECH_REGION")


def create_speech_config():
    if not SPEECH_KEY:
        raise RuntimeError("SPEECH_KEY non configurata")

    if not SPEECH_REGION:
        raise RuntimeError("SPEECH_REGION non configurata")

    config = speechsdk.SpeechConfig(
        subscription=SPEECH_KEY,
        region=SPEECH_REGION,
    )

    # MP3 24 kHz / 160 kbps
    config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Audio24Khz160KBitRateMonoMp3
    )

    return config


def text_to_mp3(
    text: str,
    output_path: str,
    voice: str = "it-IT-IsabellaNeural",
):
    speech_config = create_speech_config()

    speech_config.speech_synthesis_voice_name = voice

    audio_config = speechsdk.audio.AudioOutputConfig(
        filename=output_path
    )

    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=audio_config,
    )

    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return True

    if result.reason == speechsdk.ResultReason.Canceled:
        cancellation = speechsdk.SpeechSynthesisCancellationDetails.from_result(
            result
        )

        raise RuntimeError(
            f"Azure Speech error: "
            f"{cancellation.reason} - "
            f"{cancellation.error_details}"
        )

    return False