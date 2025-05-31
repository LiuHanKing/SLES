from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QListWidget, 
                            QPushButton, QInputDialog, QHBoxLayout)
from PyQt5.QtWidgets import QMessageBox
import json
import os
from .common_imports import *
from .common_components import DialogButtonLayout

class AbsenceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("缺席设置")  # 添加明确的窗口标题
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)
        self._load_absence_list()
        layout.addWidget(self.list_widget)

        # 使用通用按钮布局组件替换原有按钮创建逻辑
        btn_layout = DialogButtonLayout()
        btn_layout.add_btn.clicked.connect(self.add_absence)
        btn_layout.remove_btn.clicked.connect(self.remove_absence)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        
    @property
    def absence_file(self):
        """获取缺席名单文件路径"""
        return os.path.join("conf", "absence.json")
    
    def _load_absence_list(self):
        """加载缺席名单"""
        try:
            if os.path.exists(self.absence_file):
                with open(self.absence_file, 'r', encoding='utf-8') as f:
                    self.absence_list = json.load(f)
                    self.list_widget.clear()
                    self.list_widget.addItems(self.absence_list)
        except FileNotFoundError:
            logging.error(f"缺席名单文件 {self.absence_file} 未找到")
            self.absence_list = []
        except json.JSONDecodeError as e:
            logging.error(f"解析缺席名单文件 {self.absence_file} 时出错: {str(e)}")
            self.absence_list = []
        except Exception as e:
            logging.error(f"加载缺席名单失败: {str(e)}")
            self.absence_list = []
                
    def _save_absence_list(self):
        with open(self.absence_file, 'w', encoding='utf-8') as f:
            json.dump(self.absence_list, f, ensure_ascii=False, indent=4)
        
    def add_absence(self):
        student_id, ok = QInputDialog.getText(
            self, "添加缺席", "输入学生ID:"
        )
        if ok and student_id:
            # 添加输入验证
            if not student_id.strip():
                QMessageBox.warning(self, "警告", "学生ID不能为空")
                return
            if student_id in self.absence_list:
                QMessageBox.warning(self, "警告", "该学生已在缺席名单中")
                return
                
            self.absence_list.append(student_id)
            self._save_absence_list()
            self.list_widget.addItem(student_id)
            
    def remove_absence(self):
        if item := self.list_widget.currentItem():
            self.absence_list.remove(item.text())
            self._save_absence_list()
            self.list_widget.takeItem(self.list_widget.row(item))