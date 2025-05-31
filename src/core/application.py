from PyQt5.QtWidgets import QApplication
import sys
from src.services.config_service import ConfigService  # 新增导入
from src.ui.main_window import MainWindow  # 新增MainWindow导入

class Application:
    def __init__(self):
        self.config = ConfigService.load_config()
        self._init_logging()
        self._verify_directories()
        
    def _init_logging(self):
        """迁移原main.py中的日志初始化逻辑"""
        from utils.logger import setup_logging
        setup_logging(self.config)
        
    def _verify_directories(self):
        """迁移目录验证逻辑"""
        required_dirs = [
            self.config.log_dir, 
            self.config.backup_dir
        ]
        DirectoryService.verify_dirs(required_dirs)


def main():
    app = QApplication(sys.argv)
    config = ConfigService.load_config()
    window = MainWindow(config)
    window.showMaximized()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()