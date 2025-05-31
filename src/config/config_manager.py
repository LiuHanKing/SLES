import json
import os
import logging
from pathlib import Path
from typing import Dict, List  # 添加 List 导入

class ConfigManager:
    CONFIG_DIR = "conf"
    CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
    DEFAULT_CONFIG = {
        "version": "1.0.0",
        "student_file": "students.xlsx",
        "absence_file": "conf/absence.json",
        "backup_dir": "bakfiles",
        "log_dir": "log",
        "animation_duration": 5,
        "weights": {"default": 1, "custom_weights": {}}
    }
    REQUIRED_KEYS = ["student_file", "absence_file", "backup_dir", "log_dir"]  # 新增类级必需键常量

    @classmethod
    def load_config(cls) -> Dict:
        """统一加载配置（合并重复方法）"""
        config_path = Path(cls.CONFIG_PATH)
        if not config_path.exists():
            return cls._create_default_config()
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 版本检查与迁移
        if not cls.check_config_version(config):
            config = cls.migrate_config(config)
            cls._save_config(config)
        
        # 验证配置有效性（整合类型检查和必填字段）
        if not cls.validate_config(config):
            raise ValueError("配置文件无效")
        
        # 使用类级常量补充缺失的必需键（原错误位置已修正）
        for key in cls.REQUIRED_KEYS:  # 改为访问类级常量
            if key not in config:
                config[key] = cls.DEFAULT_CONFIG[key]
        return config

    @classmethod
    def validate_config(cls, config: Dict) -> bool:
        """统一验证配置（整合类型和字段检查）"""
        # 使用类级常量替换局部变量
        missing_keys = [k for k in cls.REQUIRED_KEYS if k not in config]
        if missing_keys:
            logging.error(f"配置缺失必要字段: {missing_keys}")
            return False
        
        type_checks = {
            "animation_duration": int,
            "weights": dict,
            "weights.default": int
        }
        for key, expected_type in type_checks.items():
            value = cls._nested_get(config, key.split("."))
            if not isinstance(value, expected_type):
                logging.error(f"配置项 {key} 类型错误（期望{expected_type}）")
                return False
        return True

    @staticmethod
    @staticmethod
    def _nested_get(d: Dict, keys: List[str]):  # 此处 List 类型将正常识别
        """辅助函数：嵌套获取字典值"""
        for key in keys:
            d = d.get(key, {})
        return d

    @classmethod
    def _create_default_config(cls, path):
        """创建默认配置文件
        Args:
            path: 配置文件保存路径
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(cls.DEFAULT_CONFIG, f, indent=4)
            logging.info("默认配置文件创建完成: %s", str(path))
        # 创建配置文件后立即创建必需文件
        cls._create_required_files(cls.DEFAULT_CONFIG)  # 传入默认配置

    @classmethod 
    def _create_required_files(cls, config: dict) -> None:
        """创建所有必需的文件和目录"""
        # 使用Path对象处理路径
        from pathlib import Path
        
        # 学生名单文件
        student_file = Path(config["student_file"])
        student_file.parent.mkdir(parents=True, exist_ok=True)
        if not student_file.exists():
            from data.student_manager import StudentManager
            StudentManager._create_template(str(student_file))
            
        # 创建缺席记录文件
        absence_file = config["absence_file"]
        os.makedirs(os.path.dirname(absence_file), exist_ok=True)
        if not os.path.exists(absence_file):
            with open(absence_file, "w", encoding="utf-8") as f:
                json.dump({"records": []}, f)
                
        # 创建备份目录
        os.makedirs(config["backup_dir"], exist_ok=True)
        
        # 创建日志目录
        os.makedirs(config["log_dir"], exist_ok=True)
        
        # 创建数据目录
        os.makedirs(config.get("data_dir", "data"), exist_ok=True)

    @classmethod
    def update_weight(cls, student_id: str, weight: int):
        """更新学生权重
        Args:
            student_id: 学生ID
            weight: 权重值
        """
        config = cls.load_config()
        if weight == cls.DEFAULT_CONFIG["weights"]["default"]:
            config["weights"]["custom_weights"].pop(student_id, None)
        else:
            config["weights"]["custom_weights"][student_id] = weight
        
        with open(os.path.join(cls.CONFIG_DIR, "config.json"), 'w') as f:
            json.dump(config, f, indent=4)

    @classmethod
    def update_default_weight(cls, weight: int):
        """更新默认权重
        Args:
            weight: 默认权重值
        """
        config = cls.load_config()
        config["weights"]["default"] = weight
        cls._save_config(config)
    
    @classmethod 
    def update_custom_weights(cls, custom_weights: dict):
        """更新自定义权重
        Args:
            custom_weights: 自定义权重字典 {学生ID: 权重值}
        """
        config = cls.load_config()
        config["weights"]["custom_weights"] = custom_weights
        cls._save_config(config)
    
    @classmethod
    def _save_config(cls, config: dict):
        """保存配置到文件
        Args:
            config: 配置字典
        """
        with open(os.path.join(cls.CONFIG_DIR, "config.json"), 'w') as f:
            json.dump(config, f, indent=4)

    @classmethod
    def check_config_version(cls, config: dict) -> bool:
        """检查配置版本是否兼容
        Args:
            config: 配置字典
        Returns:
            bool: 版本是否兼容
        """
        try:
            return config.get("version") == cls.DEFAULT_CONFIG["version"]
        except (KeyError, AttributeError):
            return False

    @classmethod
    def migrate_config(cls, old_config: dict) -> dict:
        """迁移旧版配置到新版
        Args:
            old_config: 旧版配置字典
        Returns:
            dict: 迁移后的配置字典
        """
        new_config = cls.DEFAULT_CONFIG.copy()
        new_config.update(old_config)
        return new_config

    @classmethod
    def backup_config(cls, backup_dir=None):
        """备份当前配置文件
        Args:
            backup_dir: 备份目录路径，默认为配置中的backup_dir
        Returns:
            str: 备份文件路径
        """
        config = cls.load_config()
        backup_dir = backup_dir or config["backup_dir"]
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"config_{timestamp}.json")
        
        with open(os.path.join(cls.CONFIG_DIR, "config.json"), 'r') as src, \
             open(backup_path, 'w') as dst:
            dst.write(src.read())
            
        logging.info(f"配置文件已备份至: {backup_path}")
        return backup_path

    @classmethod
    def _validate_config_types(cls, config: dict) -> bool:
        """验证配置项数据类型是否正确"""
        type_checks = {
            "version": str,
            "student_file": str,
            "absence_file": str,
            "animation_duration": int,
            "weights": dict,
            "draw_settings": dict,
            "schedule": dict
        }
        
        try:
            for key, expected_type in type_checks.items():
                if not isinstance(config.get(key), expected_type):
                    logging.error(f"配置项类型错误: {key} 应为 {expected_type}")
                    return False
            return True
        except Exception as e:
            logging.error(f"配置类型验证异常: {str(e)}")
            return False

    # 删除以下无效注释和导入语句
    # """ 将配置验证逻辑拆分为独立文件 """
    # from .config_validator import validate_config_types, check_config_version
    # """ 将配置迁移逻辑拆分为独立文件 """
    # from .config_migrator import migrate_config
    
    @staticmethod
    def update_config(updates):
        """更新配置并添加类型检查"""
        original = ConfigManager.load_config()
        
        # 配置项类型验证
        type_spec = {
            'splitter_ratio': (int, lambda x: 0 <= x <= 100),
            'schedule': (dict, lambda x: 'start' in x and 'end' in x)
        }
        
        for key, value in updates.items():
            if key in type_spec:
                type_check, val_check = type_spec[key]
                if not isinstance(value, type_check) or not val_check(value):
                    raise ValueError(f"Invalid config value for {key}")
        
        merged = {**original, **updates}
        with open(CONFIG_PATH, 'w') as f:
            json.dump(merged, f, indent=4)