import os
from abc import ABC, abstractmethod

import requests
from tqdm import tqdm


class DownloadStrategy(ABC):
    @abstractmethod
    def download(url: str, output_filename: str) -> bool:
        pass


class HttpDownloadStrategy(DownloadStrategy):
    @staticmethod
    def download(url: str, output_filename: str) -> bool:
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            file_size = int(response.headers.get("content-length", 0))

            with open(output_filename, "wb") as file, tqdm(
                desc=output_filename,
                total=file_size,
                unit="iB",
                unit_scale=True,
                unit_divisor=1024,
            ) as progress_bar:
                for data in response.iter_content(chunk_size=1024):
                    size = file.write(data)
                    progress_bar.update(size)

            print(f"Download completed: {output_filename}")
            return True

        except requests.RequestException as e:
            print(f"Error downloading file: {e}")
            return False
