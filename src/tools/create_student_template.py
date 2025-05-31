import openpyxl
from openpyxl.styles import Font

def create_student_template(output_file="students.xlsx"):
    """创建学生名单Excel模板"""
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = "学生名单"
    
    # 设置表头
    headers = ["学号", "姓名"]
    sheet.append(headers)
    
    # 设置表头样式
    for cell in sheet[1]:
        cell.font = Font(bold=True)
    
    # 添加示例数据
    sample_data = [
        ["1001", "张三"],
        ["1002", "李四"]
    ]
    for row in sample_data:
        sheet.append(row)
    
    # 自动调整列宽
    for column in sheet.columns:
        max_length = 0
        column = [cell for cell in column]
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2
        sheet.column_dimensions[column[0].column_letter].width = adjusted_width
    
    wb.save(output_file)
    print(f"学生名单模板已创建: {output_file}")

if __name__ == "__main__":
    create_student_template()