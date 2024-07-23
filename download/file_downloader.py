import os

from download.download_strategy import DownloadStrategy


class FileDownloader:
    def __init__(self, download_strategy: DownloadStrategy):
        self.download_strategy = download_strategy

    def download(self, url: str, output_filename: str = None) -> bool:
        clean_url = self._clean_url(url)
        output_filename = self._get_output_filename(clean_url, output_filename)

        if os.path.exists(output_filename):
            print(f"File already exists: {output_filename}")
            return True

        return self.download_strategy.download(clean_url, output_filename)

    @staticmethod
    def _clean_url(url: str) -> str:
        return url.replace("\\", "")

    @staticmethod
    def _get_output_filename(url: str, output_filename: str = None) -> str:
        return output_filename or url.split("/")[-1]
