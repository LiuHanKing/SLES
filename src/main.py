import sys
import logging
from pathlib import Path
# 将项目根目录添加到 sys.path
project_root = Path(__file__).parents[1]
sys.path.append(str(project_root))

from PyQt5.QtWidgets import QApplication
# 修改为绝对导入
from src.ui.main_window import MainWindow
from src.services.log_service import configure_logging
from src.utils.file_utils import init_app_files

if __name__ == '__main__':
    configure_logging()
    init_app_files()
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())