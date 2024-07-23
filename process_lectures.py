import json
import logging
import time

from process_lecture import process_lecture

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def main():
    total_start_time = time.time()

    json_file = "lectures.json"
    with open(json_file, "r") as file:
        lectures = json.load(file)

    for lecture in lectures:
        process_lecture(lecture)

    total_end_time = time.time()
    total_execution_time_minutes = (total_end_time - total_start_time) / 60

    logger.info(f"All lectures processed. Total execution time: {total_execution_time_minutes:.2f} minutes")


if __name__ == "__main__":
    main()
