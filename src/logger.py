import logging
import os
import yaml

def setup_logging(config_path="config/config.yaml"):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
        
    log_config = config.get('logging', {})
    os.makedirs(os.path.dirname(log_config['filepath']),exist_ok=True)
    
    logging.basicConfig(
        level = log_config['level'],
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_config['filepath']),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)