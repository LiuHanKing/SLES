import json
from pathlib import Path
from services.excel_service import ExcelService
import logging
import subprocess  # 新增导入
import pandas as pd  # 统一在开头导入

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
        import pandas as pd
        df = pd.DataFrame(data)
        df.to_excel(str(student_template), index=False)
        logger.info(f"创建学生模板文件: {student_template}")
    except Exception as e:
        logger.error(f"创建学生模板文件时出错: {e}")

def init_app_files():
    """初始化缺失的配置文件、学生模板、日志目录"""
    logger.info("开始初始化应用文件")
    # 初始化配置目录
    config_dir = Path(__file__).parents[2] / "conf"
    config_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"检测配置目录: {config_dir}，已存在或创建成功")

    # 创建默认配置文件
    config_file = config_dir / "config.json"
    if not config_file.exists():
        create_default_config(config_file)
    else:
        logger.info(f"配置文件已存在: {config_file}")
    
    # 移除检查 conf参数说明.txt 和执行 add_config_explanation.py 的代码

    logger.info("应用文件初始化完成")

    # 移除创建 default_students.xlsx 的逻辑
    config = json.loads(config_file.read_text(encoding='utf-8'))
    excel_file_path_str = config.get("excel_file_path")
    if excel_file_path_str:
        excel_file_path = Path(__file__).parents[2] / excel_file_path_str
        if not excel_file_path.exists():
            create_student_template(excel_file_path)

# 删除重复的 pandas 导入和 create_student_template_file 函数
import os
from pathlib import Path
from services.config_service import ConfigService

def create_student_template_file():
    config = ConfigService.load_config()
    excel_file_path_str = config.get("excel_file_path")
    if not excel_file_path_str:
        print("配置文件中未找到 'excel_file_path' 配置项，请检查配置文件。")
        return
    
    excel_file_path = Path(__file__).parents[2] / excel_file_path_str
    excel_file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 这里可以添加创建 Excel 文件的具体逻辑
    print(f"创建学生模板文件: {excel_file_path}")
    # 示例：创建一个空的 Excel 文件
    # 这里需要导入相应的库，如 pandas
    import pandas as pd
    df = pd.DataFrame()
    df.to_excel(excel_file_path, index=False)