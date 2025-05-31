import json
import logging
import random  # 补充缺失的随机模块导入
from datetime import datetime
from typing import List
from model.student import Student

class DrawEngine:
    def __init__(self, students: List[Student], absence_list: List[str]) -> None:
        """初始化抽签引擎
        Args:
            students: 学生列表
            absence_list: 缺席学生ID列表
        """
        self.students = [s for s in students if s.id not in absence_list]
        self.logger = logging.getLogger(__name__)
        
    def draw(self, count: int = 1) -> List[Student]:
        """
        执行加权随机抽签
        Args:
            count: 抽取数量 (默认1)
        Returns:
            List[Student]: 有序抽签结果
        Raises:
            ValueError: 当无有效数据时抛出异常
        """
        # 添加权重归一化处理
        total_weight = sum(s.weight for s in self.students)
        if total_weight <= 0:
            self.logger.warning("权重总和异常，使用平均权重")
            for s in self.students:
                s.weight = 1
                
        if not self.students:
            self.logger.error("抽签失败: 没有可用的学生名单")
            raise ValueError("没有可用的学生名单")
            
        # 过滤掉无效学生(学号和姓名都为空的情况)
        valid_students = [s for s in self.students if s.id or s.name]
        if not valid_students:
            self.logger.error("抽签失败: 学生名单中没有有效数据")
            raise ValueError("学生名单中没有有效数据")
            
        results = random.choices(valid_students, weights=[s.weight for s in valid_students], k=count)
        self.logger.info(f"成功抽取{len(results)}名学生")
        # 格式化显示结果
        for student in results:
            if not student.id:
                student.display_text = student.name
            else:
                student.display_text = f"{student.id} {student.name}"
        return results
