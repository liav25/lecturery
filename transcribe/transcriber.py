import logging
from abc import ABC, abstractmethod

from openai import OpenAI

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class Transcriber(ABC):
    @abstractmethod
    def transcribe_audio(self, audio_file, language):
        pass


class OpenAITranscriber(Transcriber):
    def __init__(self, model_name):
        self.client = OpenAI()
        self.model_name = model_name

    def transcribe_audio(self, audio_file, language):
        try:
            with open(audio_file, "rb") as file:
                transcription = self.client.audio.transcriptions.create(
                    model=self.model_name, language=language, file=file
                )
            logging.info(f"Transcribed audio file: {audio_file}")
            return transcription.text
        except Exception as e:
            logging.error(f"Error transcribing audio file {audio_file}: {e}")
            raise
