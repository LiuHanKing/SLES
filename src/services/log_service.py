import logging
from pathlib import Path
from services.config_service import ConfigService

def configure_logging():
    config = ConfigService.load_config()
    log_level = "DEBUG"  # 强制设置为 DEBUG 级别
    if "log" in config and "level" in config["log"]:
        log_level = config["log"]["level"].upper()
    else:
        print("配置文件中未找到 'log' 或 'level' 配置项，使用默认日志级别 DEBUG")

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