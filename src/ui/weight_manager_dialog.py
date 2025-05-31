from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton

class WeightManagerDialog(QDialog):
    def __init__(self, parent=None, config=None, students=None):
        super().__init__(parent)
        self.config = config
        self.students = students
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("学生权重管理")
        layout = QVBoxLayout()
        
        # 创建表格（调整列宽）
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["学号", "姓名", "权重"])
        self.table.setColumnWidth(0, 120)  # 学号列固定宽度
        self.table.setColumnWidth(1, 150)  # 姓名列固定宽度
        self.table.horizontalHeader().setStretchLastSection(True)  # 权重列自适应
        self._load_students()
        
        # 保存按钮（统一样式）
        self.save_btn = QPushButton("保存权重")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.save_btn.clicked.connect(self._save_weights)
        
        layout.addWidget(self.table)
        layout.addWidget(self.save_btn)
        self.setLayout(layout)
    
    def _load_students(self):
        # 添加数据有效性验证
        if not self.students:
            from src.data.student_manager import StudentManager  # 修正绝对路径
            self.students = StudentManager.load_students(self.config["student_file"])
            
        # 添加空数据保护
        if not self.students:
            self.students = [Student(id="000", name="示例学生", weight=1)]
            
        self.table.setRowCount(len(self.students))
        for i, student in enumerate(self.students):
            self.table.setItem(i, 0, QTableWidgetItem(student.id))
            self.table.setItem(i, 1, QTableWidgetItem(student.name))
            self.table.setItem(i, 2, QTableWidgetItem(str(student.weight)))
    
    def _save_weights(self):
        try:
            custom_weights = {}
            for row in range(self.table.rowCount()):
                student_id = self.table.item(row, 0).text().strip()
                weight_str = self.table.item(row, 2).text().strip()
                
                if not student_id or not weight_str:
                    raise ValueError("存在空字段")
                
                if not weight_str.isdigit() or int(weight_str) < 0:
                    raise ValueError(f"第{row+1}行权重必须为非负整数")
                
                custom_weights[student_id] = int(weight_str)

            ConfigManager.update_config({"weights": {"custom_weights": custom_weights}})
            QMessageBox.information(self, "成功", "权重保存完成")
        except Exception as e:
            QMessageBox.warning(self, "错误", f"保存失败: {str(e)}")