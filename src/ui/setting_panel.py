from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                           QGroupBox, QSpinBox, QPushButton,
                           QFormLayout, QComboBox)
from config.config_manager import ConfigManager  # 修正相对导入路径
import logging  # 添加导入
import os  # 新增导入

# 清理重复导入，仅保留一次
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                           QGroupBox, QSpinBox, QPushButton,
                           QFormLayout, QComboBox)
from config.config_manager import ConfigManager  # 仅保留一次导入
import logging
import os  # 仅保留一次导入

# 定义全局配置路径（确保在全局作用域）
CONFIG_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'conf', 'config.json')
)

class SettingPanel(QWidget):
    def __init__(self, config):
        super().__init__()
        self.logger = logging.getLogger(__name__)  # 添加logger
        self.config = config
        self.setWindowTitle("系统设置")
        self.setMinimumSize(400, 300)
        self.setStyleSheet("""
            QWidget {
                font-size: 14px;
            }
            QGroupBox {
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        self.label = QLabel("系统设置")
        layout.addWidget(self.label)
        
        # 合并后的设置面板
        layout.addWidget(self.init_combined_settings())
        
        # 恢复保存按钮功能
        self.save_btn = QPushButton("应用设置")
        self.save_btn.clicked.connect(self.save_settings)
        layout.addWidget(self.save_btn)
        
        self.setLayout(layout)

    def save_settings(self):
        """恢复设置保存功能"""
        try:
            splitter_ratio = self.splitter_ratio_spin.value()
            default_weight = self.default_weight.value()
            countdown = self.countdown_spin.value()
            display_mode = self.display_combo.currentIndex()
            font_size = self.font_size_spin.value()
            scroll_font = self.scroll_font_spin.value()
            log_level = self.log_level_combo.currentText()
            animation_duration = self.animation_spin.value()

            if default_weight <= 0:
                QMessageBox.warning(self, "警告", "默认权重必须大于0")
                return

            # 更新全局配置
            ConfigManager.update_config({
                "splitter_ratio": splitter_ratio,
                "weights": {"default": default_weight},
                "draw_settings": {
                    "countdown": countdown,
                    "display_mode": display_mode,
                    "font_size": font_size,
                    "scroll_font": scroll_font
                },
                "log_level": log_level,
                "animation_duration": animation_duration
            }, config_path=CONFIG_PATH)
            
            QMessageBox.information(self, "成功", "设置已应用")
        except Exception as e:
            self.logger.error(f"应用设置失败: {str(e)}", exc_info=True)
            QMessageBox.warning(self, "错误", f"应用失败: {str(e)}")

    def init_combined_settings(self):
        """初始化合并后的设置面板"""
        self.settings_group = QGroupBox("系统设置")
        layout = QFormLayout()
        
        # 权重设置部分
        self.default_weight = QSpinBox()
        self.default_weight.setRange(0, 10)
        self.default_weight.setValue(1)
        layout.addRow("默认权重:", self.default_weight)
        
        # 抽签模式设置部分
        self.countdown_spin = QSpinBox()
        self.countdown_spin.setRange(1, 10)
        self.countdown_spin.setValue(3)
        layout.addRow("倒计时时间(秒):", self.countdown_spin)
        
        self.display_combo = QComboBox()
        self.display_combo.addItems(["显示学号和姓名", "仅显示学号", "仅显示姓名"])
        layout.addRow("显示方式:", self.display_combo)
    
        # 新增字体大小设置
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(12, 72)
        self.font_size_spin.setValue(36)  # 默认36号字体
        layout.addRow("抽签结果字体大小:", self.font_size_spin)
        
        # 新增滚动字体大小设置
        self.scroll_font_spin = QSpinBox()
        self.scroll_font_spin.setRange(12, 36)
        self.scroll_font_spin.setValue(24)  # 默认24号字体
        layout.addRow("滚动列表字体大小:", self.scroll_font_spin)
    
        # 新增日志级别设置
        self.log_level_combo = QComboBox()
        self.log_level_combo.addItems(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        layout.addRow("日志级别:", self.log_level_combo)
    
        # 新增动画持续时间设置
        self.animation_spin = QSpinBox()
        self.animation_spin.setRange(1, 10)
        self.animation_spin.setValue(self.config.get("animation_duration", 3))
        layout.addRow("动画持续时间(秒):", self.animation_spin)
    
        # 新增分屏比例设置
        self.splitter_ratio_spin = QSpinBox()
        self.splitter_ratio_spin.setRange(10, 90)  # 10%-90%
        self.splitter_ratio_spin.setValue(30)  # 默认30%
        layout.addRow("左侧面板宽度比例(%):", self.splitter_ratio_spin)

        self.settings_group.setLayout(layout)
        return self.settings_group