import yaml
from src.api_client import APIClient
from src.data_storage import DataStorage
from src.data_aggregator import DataAggregator

def load_config(config_path="config/config.yaml"):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
     # Wczytanie konfiguracji
    config = load_config()
    #print(config)
    
    # Inicjalizacja komponentów
    api_client = APIClient(
        url=config['api']['url'],
        timeout=config['api']['timeout']
    )
    storage = DataStorage(
        output_dir=config['storage']['output_dir'],
        filename_prefix=config['storage']['filename_prefix']
    )
    aggregator = DataAggregator()

    # Pobieranie, zapisywanie i agregowanie danych
    data = api_client.fetch_data()
    if data:
        storage.save_to_json(data)
        aggregator.aggregate(data)

if __name__ == "__main__":
    main()