import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class SummarySaver:
    @staticmethod
    def save_summary(content, output_path):
        try:
            with open(output_path, "w") as file:
                file.write(content)
            logging.info(f"Saved summary to {output_path}")
        except Exception as e:
            logging.error(f"Error saving summary to {output_path}: {e}")
            raise
