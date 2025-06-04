import os
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

if getattr(sys, 'frozen', False):
    # 打包后，sys.executable 是 exe 路径
    base_dir = os.path.dirname(sys.executable)
else:
    # 源码运行，__file__ 是当前文件路径
    base_dir = os.path.dirname(os.path.abspath(__file__))

conf_dir = os.path.join(base_dir, 'conf')
config_path = os.path.join(conf_dir, 'config.json')

log_dir = os.path.join(base_dir, 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'app.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

if __name__ == '__main__':
    configure_logging(base_dir)      # 传递 base_dir
    init_app_files(base_dir)         # 传递 base_dir
    app = QApplication(sys.argv)
    main_window = MainWindow(base_dir)  # 传递 base_dir
    main_window.show()
    sys.exit(app.exec_())