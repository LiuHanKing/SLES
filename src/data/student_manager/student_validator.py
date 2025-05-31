from model.student import Student

def validate_student(student: Student) -> bool:
    """验证学生数据有效性"""
    if not student.id and not student.name:
        return False
    if student.weight and not isinstance(student.weight, (int, float)):
        return False
    return True