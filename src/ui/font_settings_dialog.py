from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFontComboBox, QSpinBox, QPushButton, QLabel
from PyQt5.QtGui import QFont

class FontSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.setWindowTitle("字体设置")
        self.setMinimumSize(300, 180)  # 设置最小尺寸

    def init_ui(self):
        layout = QVBoxLayout()
        
        # 新增字体类型选择
        self.font_family = QFontComboBox()
        self.font_family.setCurrentFont(QFont("微软雅黑"))  # 默认字体
        
        # 字体大小选择
        self.font_size = QSpinBox()
        self.font_size.setRange(8, 72)
        self.font_size.setValue(12)  # 默认大小
        
        # 确认按钮（统一样式）
        self.confirm_btn = QPushButton("确认")
        self.confirm_btn.setStyleSheet("""
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
        
        layout.addWidget(QLabel("选择字体:"))
        layout.addWidget(self.font_family)
        layout.addWidget(QLabel("字体大小:"))
        layout.addWidget(self.font_size)
        layout.addWidget(self.confirm_btn)
        self.setLayout(layout)

class DeleteStudentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.font_size_spin = QSpinBox()
        self.confirm_btn = QPushButton("确认")
        layout.addWidget(self.font_size_spin)
        layout.addWidget(self.confirm_btn)
        self.setLayout(layout)