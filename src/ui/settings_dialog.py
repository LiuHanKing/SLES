from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QSpinBox, 
                             QComboBox, QPushButton, QFontComboBox, QLineEdit)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from services.config_service import ConfigService

class SettingsDialog(QDialog):
    def __init__(self, parent=None, current_config=None):
        super().__init__(parent)
        self.current_config = current_config or ConfigService.load_config()
        self.init_ui()

    def init_ui(self):
        # 去掉窗口问号
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        # 设置窗口标题为功能名字
        self.setWindowTitle("系统设置")
        layout = QVBoxLayout()

        form_layout = QFormLayout()
        # 左右比例
        self.left_ratio = QSpinBox()
        self.left_ratio.setRange(10, 90)
        self.left_ratio.setValue(self.current_config.get("window", {}).get("left_ratio", 40))
        form_layout.addRow("左右区域比例（左%）", self.left_ratio)

        # 动画时长
        self.anim_duration = QSpinBox()
        self.anim_duration.setRange(1, 30)
        self.anim_duration.setValue(self.current_config.get("animation", {}).get("duration", 5))
        form_layout.addRow("动画时长（秒）", self.anim_duration)

        # 日志级别
        self.log_level = QComboBox()
        self.log_level.addItems(["DEBUG", "INFO", "WARNING", "ERROR"])
        self.log_level.setCurrentText(self.current_config.get("log", {}).get("level", "INFO").upper())
        form_layout.addRow("日志级别", self.log_level)

        # 字体设置
        self.font_combo = QFontComboBox()
        self.font_size = QSpinBox()
        self.font_size.setRange(8, 72)
        self.font_combo.setCurrentFont(QFont(self.current_config.get("font", {}).get("name", "Arial")))
        self.font_size.setValue(self.current_config.get("font", {}).get("size", 12))
        form_layout.addRow("字体选择", self.font_combo)
        form_layout.addRow("字体大小", self.font_size)

        # 保存/取消按钮
        btn_layout = QVBoxLayout()
        save_btn = QPushButton("保存")
        save_btn.clicked.connect(self.save_settings)
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.close)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        self.resize(400, 300)

    def save_settings(self):
        new_config = {
            "window": {
                "left_ratio": self.left_ratio.value(),
                "top_ratio": self.current_config.get("window", {}).get("top_ratio", 60)
            },
            "animation": {
                "duration": self.anim_duration.value(),
                "scroll_speed": self.current_config.get("animation", {}).get("scroll_speed", 50)
            },
            "log": {
                "level": self.log_level.currentText()
            },
            "font": {
                "name": self.font_combo.currentFont().family(),
                "size": self.font_size.value()
            }
        }
        ConfigService.save_config(new_config)
        self.accept()