import logging
import os
import shutil
import time

from download.download_strategy import HttpDownloadStrategy
from download.file_downloader import FileDownloader
from summary.summarizer import AnthropicSummarizer
from summary.summary_saver import SummarySaver
from summary.transcript_reader import TranscriptReader
from transcribe.transcriber import OpenAITranscriber
from transcribe.video_processor import VideoProcessor

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def delete_unnecessary_files(lecture_name):
    original_file = f"{lecture_name}.mp4"
    if os.path.exists(original_file):
        os.remove(original_file)
        logger.info(f"Deleted original lecture file: {original_file}")

    lecture_folder = lecture_name
    if os.path.exists(lecture_folder) and os.path.isdir(lecture_folder):
        for item in os.listdir(lecture_folder):
            item_path = os.path.join(lecture_folder, item)
            if os.path.isfile(item_path) and item != "transcriptions":
                os.remove(item_path)
                logger.info(f"Deleted non-transcription file: {item_path}")
            elif os.path.isdir(item_path) and item != "transcriptions":
                shutil.rmtree(item_path)
                logger.info(f"Deleted non-transcription folder: {item_path}")

    logger.info(f"Finished cleaning up unnecessary files for {lecture_name}")


def process_lecture(lecture):
    start_time = time.time()

    downloader = FileDownloader(HttpDownloadStrategy)
    video_processor = VideoProcessor(
        transcriber=OpenAITranscriber(model_name="whisper-1"),
    )
    summarizer = AnthropicSummarizer(model_name="claude-3-sonnet-20240229")

    downloader.download(lecture["video_url"], f"data/{lecture['name']}.mp4")

    transcriptions_folder = f"data/{lecture['name']}/transcriptions"

    video_processor.process_videos(
        input_file=f"data/{lecture['name']}.mp4",
        output_dir=f"data/{lecture['name']}",
        transcriptions_dir=transcriptions_folder,
        language=lecture.get("language", "en"),
        start_time=lecture["start_time"],
        end_time=lecture["end_time"],
        segment_time="00:10:00",
    )

    transcripts = TranscriptReader.read_transcripts(transcriptions_folder)

    full_summary = ""
    for i, transcript in enumerate(transcripts):
        summary = summarizer.summarize_lecture_part(transcript, i)
        full_summary += "\n\n" + summary
    SummarySaver.save_summary(full_summary, f"{transcriptions_folder}/raw_full_summary.txt")

    processed_full_summary = summarizer.rearrange_summary(full_summary)
    SummarySaver.save_summary(processed_full_summary, f"{transcriptions_folder}/refined_full_summary.txt")

    delete_unnecessary_files(lecture_name=f"data/{lecture['name']}")

    end_time = time.time()
    execution_time_minutes = (end_time - start_time) / 60
    logger.info(f"Lecture {lecture['name']} processed. Execution time: {execution_time_minutes:.2f} minutes")


if __name__ == "__main__":
    # This can be used for testing the process_lecture function with a single lecture
    test_lecture = {
        "name": "test_lecture",
        "video_url": "https://example.com/test_lecture.mp4",
        "start_time": "00:00:00",
        "end_time": "01:00:00",
        "language": "en",
    }
    process_lecture(test_lecture)
