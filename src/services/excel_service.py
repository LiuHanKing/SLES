import pandas as pd
from pathlib import Path
from models.student import Student
import os

class ExcelService:
    """Excel文件读写服务（仅支持xlsx）"""
    @staticmethod
    def load_students(file_path: str) -> list[Student]:
        """加载学生名单（学号、姓名）"""
        df = pd.read_excel(file_path, usecols=["学号", "姓名"])
        return [Student(student_id=row["学号"], name=row["姓名"]) 
                for _, row in df.iterrows()]
    
    @staticmethod
    def create_template(file_path):
        # 确保目录存在
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        df = pd.DataFrame(columns=["学号", "姓名"])
        df.to_excel(file_path, index=False)

    @staticmethod
    def create_template_with_samples(file_path: str):
        data = [{"学号": f"00{i}", "姓名": f"学生{i}"} for i in range(1, 11)]
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False)