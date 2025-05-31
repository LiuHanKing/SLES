import sys
import os
# 添加项目根目录到 sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

import logging
from logging.handlers import RotatingFileHandler
from typing import List
from PyQt5.QtWidgets import QApplication, QMessageBox
from ui.main_window import MainWindow
from config.config_manager import ConfigManager
from model.student import Student
from tools.create_student_template import create_student_template
from data.student_manager import StudentManager
from datetime import datetime
from pathlib import Path
import json  # 统一导入

def setup_logging(config):
    log_dir = config.get("log_dir", "log")
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    # 读取配置中的日志级别（默认INFO）
    log_level = config.get("log_level", "INFO")
    level = getattr(logging, log_level, logging.INFO)
    
    logging.basicConfig(
        level=level,  # 使用配置的日志级别
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            RotatingFileHandler(
                os.path.join(log_dir, config.get("log_file", "app.log")),  # 文件处理器
                maxBytes=1024*1024,
                backupCount=5,
                encoding='utf-8'
            ),
            logging.StreamHandler()  # 控制台输出处理器
        ]
    )
    logging.info("日志系统初始化完成")

def _ensure_dirs_exist(dirs: List[str]) -> None:
    for dir_path in dirs:
        try:
            if not os.path.exists(dir_path):
                logging.info(f"创建目录: {dir_path}")
                os.makedirs(dir_path, exist_ok=True)
                if not os.access(dir_path, os.W_OK):
                    logging.error(f"目录不可写: {dir_path}")
                    raise PermissionError(f"目录不可写: {dir_path}")
        except OSError as e:
            logging.error(f"创建目录失败: {dir_path}, 错误: {str(e)}")
            raise

def create_default_config(config_path):
    os.makedirs("conf", exist_ok=True)
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump({
            "version": "1.0.0",
            "student_file": "students.xlsx",
            "absence_file": "conf/absence.json",
            "backup_dir": "bakfiles",
            "log_dir": "log",
            "animation_duration": 3,
            "weights": {
                "default": 1,
                "custom_weights": {}
            }
        }, f, indent=4)
    logging.info("默认配置文件已创建")

def main() -> None:
    config_path = Path("conf") / "config.json"
    if not config_path.exists():
        create_default_config(config_path)
    
    try:
        config = ConfigManager.load_config()
        setup_logging(config)
        _ensure_dirs_exist([Path(config["log_dir"]), Path(config["backup_dir"])])
        
        student_file = Path(config["student_file"])
        if not student_file.exists():
            logging.warning("学生名单不存在，正在创建模板")
            create_student_template(str(student_file))
            
        absence_file = Path(config["absence_file"])
        if not absence_file.exists():
            logging.warning("缺席名单不存在，正在创建")
            absence_file.write_text("[]", encoding="utf-8")
                
        check_log_path = Path(config["log_dir"]) / "config_check.log"
        with open(check_log_path, "w", encoding="utf-8") as f:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"配置文件状态检查报告 [{now}]\n{'='*50}\n")
            
            for file_type, path in [
                ("主配置文件", "conf/config.json"),
                ("学生名单", config["student_file"]), 
                ("缺席记录", config["absence_file"]),
                ("备份目录", config["backup_dir"]),
                ("日志目录", config["log_dir"])
            ]:
                status = "存在" if Path(path).exists() else "缺失"
                f.write(f"[{now}] {file_type}状态: {status} ({path})\n")
        
        app = QApplication(sys.argv)
        window = MainWindow(config)
        window.showMaximized()
        sys.exit(app.exec_())
    except KeyError as e:
        logging.error("配置项缺失: %s", str(e))
        sys.exit(1)
    except OSError as e:
        logging.error("目录创建失败: %s", str(e))
        sys.exit(1)
    except Exception as e:
        logging.error("应用程序启动失败: %s", str(e), exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()  # 仅保留主入口调用，移除冗余代码
    # config = ConfigManager.load_config()
    # students = StudentManager.load_students(config["student_file"])
    # if not students:
    #     logging.error("没有加载到学生数据")
    #     QMessageBox.critical(None, "错误", "无法加载学生数据，请检查学生名单文件")