from pathlib import Path

class Paths:
    _BASE_DIR = Path(__file__).parent.parent.parent
    
    # 配置文件路径
    config_file = _BASE_DIR / "conf" / "config.json"
    
    # 默认文件路径
    default_student_file = _BASE_DIR / "data" / "students.xlsx"
    default_absence_file = _BASE_DIR / "data" / "absence.json"
    
    # 目录路径
    default_backup_dir = _BASE_DIR / "backups"
    default_log_dir = _BASE_DIR / "logs"