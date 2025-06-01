from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # 去掉窗口问号
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        # 设置窗口标题为功能名字
        self.setWindowTitle("关于系统")
        layout = QVBoxLayout()

        info_label = QLabel("系统名称: 抽签系统\n开发人员:liuzhiwen \n邮箱地址: liuzhiwenmr@gmail.com\n程序下载地址: https://github.com/LiuHanKing/SLES")
        # 设置文本可选择复制
        info_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        self.setLayout(layout)
        self.resize(300, 200)