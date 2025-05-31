# 主入口文件保留接口
from .student_loader import load_students
from .student_writer import save_students
from .student_validator import validate_student

# 添加缺失的StudentManager类导出
class StudentManager:
    load_students = staticmethod(load_students)
    save_students = staticmethod(save_students)
    validate_student = staticmethod(validate_student)

__all__ = ['StudentManager', 'load_students', 'save_students', 'validate_student']