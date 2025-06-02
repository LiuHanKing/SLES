import logging
from pathlib import Path
from services.config_service import ConfigService

def configure_logging():
    config = ConfigService.load_config()
    # 删除强制设置为 DEBUG 级别的代码
    log_level = config.get("log", {}).get("level", "DEBUG").upper()

    log_dir = Path(__file__).parents[2] / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "app.log"

    logging.basicConfig(
        level=getattr(logging, log_level, logging.DEBUG),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename=str(log_file),
        filemode='a'
    )
    # 同时在控制台输出日志
    console = logging.StreamHandler()
    console.setLevel(getattr(logging, log_level, logging.DEBUG))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)