import os
import json
import logging
import subprocess
from pathlib import Path
import pandas as pd
from services.excel_service import ExcelService
from services.config_service import ConfigService

logger = logging.getLogger(__name__)

def create_default_config(config_file: Path):
    default_config = {
        "window": {
            "left_ratio": 40,
            "top_ratio": 60
        },
        "animation": {
            "duration": 5,
            "scroll_speed": 50
        },
        "log": {
            "level": "INFO"
        },
        "font": {
            "name": "Arial",
            "size": 12
        }
    }
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=4)
        logger.info(f"创建默认配置文件: {config_file}")
    except Exception as e:
        logger.error(f"创建默认配置文件时出错: {e}")

def create_student_template(student_template: Path):
    try:
        student_names = [
            "其家豪", "屠梓睿", "刁梓睿", "胡红", "万敬阳",
            "泰梓睿", "纵国平", "詹丽", "张三", "李四"
        ]
        data = {
            "学号": [f"{i:03d}" for i in range(1, len(student_names) + 1)],
            "姓名": student_names
        }
        df = pd.DataFrame(data)
        df.to_excel(str(student_template), index=False)
        logger.info(f"创建学生模板文件: {student_template}")
    except Exception as e:
        logger.error(f"创建学生模板文件时出错: {e}")

def init_app_files(base_dir):
    """初始化缺失的配置文件、学生模板、日志目录"""
    logger.info("开始检查应用文件")
    conf_dir = os.path.join(base_dir, 'conf')
    if not os.path.exists(conf_dir):
        os.makedirs(conf_dir, exist_ok=True)
        logging.info(f"检测配置目录: {conf_dir}，不存在，已创建成功")
    else:
        logging.info(f"检测配置目录: {conf_dir}，已存在")
    # 创建默认配置文件
    config_file = Path(conf_dir) / "config.json"
    if not config_file.exists():
        create_default_config(config_file)
    else:
        logger.info(f"配置文件已存在: {config_file}")
    
    logger.info("应用文件初始化完成")

    config = json.loads(config_file.read_text(encoding='utf-8'))
    excel_file_path_str = config.get("excel_file_path")
    if excel_file_path_str:
        excel_file_path = Path(base_dir) / excel_file_path_str
        if not excel_file_path.exists():
            create_student_template(excel_file_path)

def create_student_template_file(base_dir):
    config = ConfigService.load_config()
    excel_file_path_str = config.get("excel_file_path")
    if not excel_file_path_str:
        print("配置文件中未找到 'excel_file_path' 配置项，请检查配置文件。")
        return
    
    excel_file_path = Path(base_dir) / excel_file_path_str
    excel_file_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"创建学生模板文件: {excel_file_path}")
    df = pd.DataFrame()
    df.to_excel(excel_file_path, index=False)