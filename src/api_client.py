import requests
from src.logger import setup_logging

class APIClient:
    def __init__(self,url,timeout=10):
        self.url = url
        self.timeout = timeout
        self.logger = setup_logging()
    
    def fetch_data(self):
        try:
            response = requests.get(self.url,timeout=self.timeout)
            response.raise_for_status()
            self.logger.info("Pomyślnie pobrano z API dane.")
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Błąd podczas poierania danych: {e}")
            return None