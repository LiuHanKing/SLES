from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox, QMessageBox, QHBoxLayout, QTableWidget, QHeaderView
from .common_imports import *

class StudentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["选择", "学生信息"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setColumnWidth(0, 60)
        
        self.id_label = QLabel("学号:")
        self.id_input = QLineEdit()
        layout.addWidget(self.id_label)
        layout.addWidget(self.id_input)
        
        self.name_label = QLabel("姓名:")
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        
        # 初始化按钮
        self.confirm_btn = QDialogButtonBox(QDialogButtonBox.Ok)
        self.cancel_btn = QDialogButtonBox(QDialogButtonBox.Cancel)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.confirm_btn)
        btn_layout.addWidget(self.cancel_btn)
        
        layout.addWidget(self.table)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        self.setWindowTitle("添加学生")
        
    def get_student_info(self):
        name = self.name_input.text().strip()
        student_id = self.id_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "警告", "姓名不能为空")
            return None, None
            
        if student_id and not student_id.isalnum():
            QMessageBox.warning(self, "警告", "学号必须为字母或数字组合")
            return None, None
            
        if len(student_id) > 20:
            QMessageBox.warning(self, "警告", "学号长度不能超过20个字符")
            return None, None
            
        return student_id, name