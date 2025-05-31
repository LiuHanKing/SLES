from model.student import Student
import openpyxl

def save_students(file_path: str, students: list[Student]):
    """保存学生数据到Excel文件"""
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.append(["学号", "姓名", "权重"])
    
    for student in students:
        sheet.append([student.id, student.name, student.weight])
        
    wb.save(file_path)