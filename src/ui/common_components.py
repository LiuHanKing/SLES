from .common_imports import *

class DialogButtonLayout(QHBoxLayout):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.add_btn = QPushButton("添加")
        self.remove_btn = QPushButton("移除")
        self.addStretch(1)  # 添加弹性空间
        self.addWidget(self.add_btn)
        self.addWidget(self.remove_btn)