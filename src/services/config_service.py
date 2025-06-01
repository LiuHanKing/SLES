import json
from pathlib import Path
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ConfigService:
    @staticmethod
    def load_config() -> Dict[str, Any]:
        config_path = Path(__file__).parents[2] / "conf" / "config.json"
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error("配置文件未找到，使用默认配置")
            return {}
        except Exception as e:
            logger.error(f"读取配置文件时出错: {e}")
            return {}

    @staticmethod
    def save_config(config: Dict[str, Any]) -> None:
        config_path = Path(__file__).parents[2] / "conf" / "config.json"
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
            logger.info("配置文件保存成功")
        except Exception as e:
            logger.error(f"保存配置文件时出错: {e}")