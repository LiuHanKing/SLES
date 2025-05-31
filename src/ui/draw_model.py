# 专注业务逻辑的文件
import json
import os
from data.student_manager import StudentManager
from datetime import datetime
import random  # 新增：导入random模块

class DrawModel:
    def __init__(self, config):
        self.config = config
        self.animation_progress = 0  # 假设存在动画进度计数器

    def _load_students(self):
        """加载学生名单（根据项目逻辑实现具体读取方式）"""
        from data.student_manager import StudentManager  # 假设使用StudentManager加载学生
        return StudentManager.load_students(self.config["student_file"])  # 从配置中获取学生文件路径

    def perform_draw(self, students):
        # 抽签算法实现
        weights = [s.weight or self.config["weights"]["default"] for s in students]
        return random.choices(students, weights=weights, k=1)[0]  # 此处需要random模块

    def save_draw_record(self, student, absence_list, draw_mode, draw_count):
        # 保存记录逻辑
        record = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "student": student.to_dict(),
            "absence_list": absence_list,
            "draw_mode": draw_mode,
            "draw_count": draw_count
        }
        data_dir = self.config["data_dir"]
        os.makedirs(data_dir, exist_ok=True)
        with open(f"{data_dir}/draw_history.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    # 新增：重置抽签结果的方法（解决 AttributeError）
    def reset_results(self):
        """新增结果重置方法"""
        self.current_draw_results = []
        self.history_records = []
        logging.info("抽签结果已重置")

    # 新增：重置动画进度的方法
    def reset_animation_progress(self):
        """重置动画进度（解决 AttributeError）"""
        self.animation_progress = 0  # 重置为初始值（如0）