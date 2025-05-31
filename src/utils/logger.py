def setup_logging(config):
    log_dir = Paths.default_log_dir
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=config.get("log_level", "INFO"),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            RotatingFileHandler(
                log_dir / config.get("log_file", "app.log"),
                maxBytes=1024*1024,
                backupCount=5,
                encoding='utf-8'
            ),
            logging.StreamHandler()
        ]
    )