import logging
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class TranscriptReader:
    @staticmethod
    def read_transcripts(folder_path):
        transcripts = []
        try:
            for filename in sorted(os.listdir(folder_path)):
                if filename.endswith(".txt"):
                    with open(os.path.join(folder_path, filename), "r") as file:
                        transcripts.append((filename, file.read()))
            logging.info(f"Read {len(transcripts)} transcripts from {folder_path}")
        except Exception as e:
            logging.error(f"Error reading transcripts: {e}")
            raise
        return transcripts
