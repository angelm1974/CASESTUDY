import json
from datetime import datetime
import os
from src.logger import setup_logging


class DataStorage:
    def __init__(self, output_dir, filename_prefix):
        self.output_dir = output_dir
        self.filename_prefix = filename_prefix
        self.logger = setup_logging()
        os.makedirs(output_dir, exist_ok=True)

    def save_to_json(self, data):
        if not data:
            self.logger.warning("Brak danych do zapisania.")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.filename_prefix}_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)

        try:
            with open(filepath, "w", encoding="utf") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            self.logger.info(f"Dane zapisano do pliku: {filepath}")
        except Exception as e:
            self.logger.error(f"Bład podczas zapiswywania danych: {e}")
