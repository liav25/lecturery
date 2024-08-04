import logging
import os

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class VideoProcessor:
    def __init__(self, transcriber):
        self.transcriber = transcriber

    def __split_video(
        self, input_file, output_dir, start_time, end_time, segment_time="00:10:00"
    ):
        if not os.path.exists(output_dir):
            os.makedirs(f"{output_dir}/transcriptions")
        else:
            logging.info(
                f"Output directory {output_dir} already exists. Skipping creation."
            )

        command = f"ffmpeg -i {input_file} -ss {start_time} -to {end_time} -c copy -map 0 -segment_time {segment_time} -f segment {output_dir}/output%03d.mp4"
        os.system(command)
        logging.info(f"Video split into segments and saved to {output_dir}")

    def __extract_audio(self, video_file, audio_file):
        command = f"ffmpeg -i {video_file} -q:a 0 -map a {audio_file}"
        os.system(command)
        logging.info(f"Extracted audio from {video_file} to {audio_file}")

    def __process_video_file(
        self, video_file, output_dir, transcriptions_dir, language
    ):
        video_path = os.path.join(output_dir, video_file)
        audio_path = os.path.join(output_dir, os.path.splitext(video_file)[0] + ".mp3")

        if not os.path.exists(audio_path):
            self.__extract_audio(video_path, audio_path)
            logging.info(f"Extracted audio for {video_file}")

        transcription_text = self.transcriber.transcribe_audio(audio_path, language)
        transcription_file = os.path.join(
            transcriptions_dir, f"{os.path.splitext(video_file)[0]}_transcription.txt"
        )

        with open(transcription_file, "w") as f:
            f.write(transcription_text)
        logging.info(f"Transcription saved for {video_file}")

    def process_videos(
        self,
        input_file,
        output_dir,
        transcriptions_dir,
        language,
        start_time="00:00:00",
        end_time=None,
        segment_time="00:10:00",
    ):
        self.__split_video(input_file, output_dir, start_time, end_time, segment_time)

        for video_file in os.listdir(output_dir):
            if video_file.endswith(".mp4"):
                self.__process_video_file(
                    video_file, output_dir, transcriptions_dir, language
                )
