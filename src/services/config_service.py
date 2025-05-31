from pydantic import BaseModel  # 新增导入

class AppConfig(BaseModel):
    version: str
    student_file: str
    
    # 添加缺失字段定义
    absence_file: str
    backup_dir: str
    log_dir: str
    
    class Config:
        extra = 'allow'  # 允许配置文件包含额外字段

class ConfigService:
    @classmethod
    def create_default(cls) -> AppConfig:
        return AppConfig(
            version="1.0.0",
            student_file="data/students.xlsx",
            absence_file="conf/absence.json",  # 确保包含缺失字段
            backup_dir="bakfiles",
            log_dir="log",
            animation_duration=3,
            weights={"default": 1, "custom_weights": {}},
            draw_mode={"countdown": 3, "display_mode": 2},
            schedule={
                "morning_start": "08:00",
                "morning_end": "12:00",
                "afternoon_start": "14:00",
                "afternoon_end": "18:00"
            },
            result_font_size=48,
            scroll_font_size=36,
            splitter_ratio=30,
            draw_btn_width=120,
            stop_btn_width=100,
            reset_btn_width=100
        )

    @staticmethod
    def load_config() -> AppConfig:
        config_path = Paths.config_file
        if not config_path.exists():
            return ConfigService.create_default()
            
        with open(config_path, 'r', encoding='utf-8') as f:
            return AppConfig(**json.load(f))  # 现在可以正确解析