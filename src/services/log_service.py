import logging
import os
from pathlib import Path
from services.config_service import ConfigService

def configure_logging(base_dir):
    config = ConfigService.load_config()
    log_level = config.get("log", {}).get("level", "DEBUG").upper()

    log_dir = os.path.join(base_dir, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'app.log')

    logging.basicConfig(
        level=getattr(logging, log_level, logging.DEBUG),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )