import os
from pathlib import Path

import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()


def create_speech_config():
    key = os.getenv("SPEECH_KEY")
    region = os.getenv("SPEECH_REGION")
    if not key or not region:
        raise RuntimeError("Configura SPEECH_KEY e SPEECH_REGION nel file .env")

    config = speechsdk.SpeechConfig(subscription=key, region=region)
    config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Audio24Khz160KBitRateMonoMp3
    )
    return config


def text_to_mp3(text: str, output_path: str, voice: str | None = None):
    config = create_speech_config()
    config.speech_synthesis_voice_name = voice or os.getenv("SPEECH_VOICE", "it-IT-IsabellaNeural")
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_path)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=config, audio_config=audio_config)
    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return output_path
    if result.reason == speechsdk.ResultReason.Canceled:
        details = speechsdk.SpeechSynthesisCancellationDetails.from_result(result)
        raise RuntimeError(f"Azure Speech: {details.reason} - {details.error_details}")
    raise RuntimeError(f"Azure Speech synthesis failed: {result.reason}")
