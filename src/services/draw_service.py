import random
import re  # 新增导入正则表达式模块
from datetime import datetime
from models.draw_record import DrawRecord
from utils.animation_utils import start_animation
from PyQt5.QtCore import QTimer
import logging

logger = logging.getLogger(__name__)

class DrawService:
    """抽签核心服务（支持滚动、多模式）"""
    def __init__(self):
        self.students = []  # 学生列表
        self.history = []  # 抽签历史
        self.animation_timer = None  # 新增动画计时器
        self.timer = None
        self.unique_students_cache = None

    def start_draw(self, count: int, mode: str) -> list:
        """执行抽签（支持单次/多次/全部抽取）"""
        if mode == "single":
            results = random.sample(self.students, min(count, len(self.students)))
        elif mode == "all":
            results = self.students.copy()
        else:
            raise ValueError("无效抽签模式")
        
        # 记录历史
        record = DrawRecord(
            date=datetime.now().date(),
            time=datetime.now().time(),
            results=[str(s.student_id) for s in results],
            count=count,
            mode=mode
        )
        self.history.append(record)
        return results

    def start_animation(self, duration: int, callback, scroll_speed: int, result_label, mode="rolling"):
        try:
            unique_students = self.get_unique_students()
            self.animation_timer = start_animation(result_label, scroll_speed, duration, callback, unique_students, mode)
        except Exception as e:
            logger.error(f"启动动画时出错: {e}")

        self.result_label = result_label

        # 移除多余的定时器
        if self.timer:
            self.timer.stop()
            self.timer = None

    def stop_animation(self):
        if self.animation_timer:
            self.animation_timer.stop()
            self.animation_timer = None
        if self.timer:
            self.timer.stop()
            self.timer = None  # 重置定时器

    def reset(self):
        # 实现重置逻辑，例如清空已抽签的记录
        self.history = []
        # 可以根据实际需求添加更多重置逻辑

    def load_students(self, students: list):
        valid_students = []
        for student in students:
            if hasattr(student, 'name') and student.name:
                valid_students.append(student)
            else:
                logger.warning(f"无效学生信息，姓名缺失，该学生将被忽略。")
        self.students = valid_students

    def get_unique_students(self):
        unique_students = []
        student_ids = set()
        for student in self.students:
            if student.student_id not in student_ids:
                unique_students.append(student)
                student_ids.add(student.student_id)
        return unique_students