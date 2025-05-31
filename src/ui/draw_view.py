from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QListWidget, QPushButton, QSplitter)
from PyQt5.QtCore import Qt  # 新增 Qt 模块导入
from PyQt5.QtWidgets import QMessageBox
# 确保顶部已包含QFont导入
from PyQt5.QtGui import QFont

class DrawView(QWidget):
    def __init__(self, parent=None, config=None):
        super().__init__(parent)
        self.config = config  # 接收全局配置
        self._init_ui()

    def _init_ui(self):
        # 修复组件初始化顺序（删除重复的result_label初始化）
        self.result_label = QLabel("准备抽签")
        self.result_label.setAlignment(Qt.AlignCenter)
        
        self.result_list = QListWidget()  # 提前初始化result_list
        
        # 确保配置参数正确应用
        result_font_size = self.config.get("result_font_size", 48)
        scroll_font_size = self.config.get("scroll_font_size", 36)
        
        self.result_label.setStyleSheet(f"""
            font-size: {result_font_size}px;
            font-weight: bold;
            color: #333333;
        """)
        
        self.result_list.setStyleSheet(f"""
            QListWidget {{
                font-size: {scroll_font_size}px;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
            }}
        """)
        
        # 添加布局有效性验证
        if not self.layout():
            self.setLayout(QVBoxLayout())  # 确保始终有有效布局
        # 主水平分割布局（左右结构）
        main_splitter = QSplitter(self)
        main_splitter.setStyleSheet("QSplitter::handle { background: #f0f0f0; width: 2px; }")  # 美化分割线
        
        # 左边容器（抽签操作区）
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(20, 20, 20, 20)  # 增大内边距（上右下左）
        left_layout.setSpacing(20)  # 控件间距
        
        # 结果提示标签（大字体）
        self.result_label = QLabel("准备抽签")
        self.result_label.setStyleSheet(f"""
            font-size: {self.config.get("result_font_size", 48)}px;
            font-weight: bold;
            color: #333333;
            alignment: center;
        """)
        self.result_label.setAlignment(Qt.AlignCenter)  # 现在 Qt 已正确导入
        left_layout.addWidget(self.result_label, 6)  # 60%高度
        
        # 按钮区域（40%高度）
        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setSpacing(20)  # 按钮间间距
        
        # 中止/重置按钮组（垂直排列）
        control_layout = QVBoxLayout()
        control_layout.setSpacing(10)
        
        # 中止按钮（使用配置参数控制宽度）
        self.stop_btn = QPushButton("中止抽签")
        self.stop_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #f44336;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                min-width: {self.config.get("stop_btn_width", 100)}px;  /* 读取配置参数 */
                font-size: {self.config.get("font_size", 14)}px;
            }}
            QPushButton:hover {{
                background-color: #d32f2f;
            }}
        """)
        control_layout.addWidget(self.stop_btn)
        
        # 重置按钮（使用配置参数控制宽度）
        self.reset_btn = QPushButton("重置结果")
        self.reset_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #ff9800;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                min-width: {self.config.get("reset_btn_width", 100)}px;  /* 读取配置参数 */
                font-size: {self.config.get("font_size", 14)}px;
            }}
            QPushButton:hover {{
                background-color: #f57c00;
            }}
        """)
        control_layout.addWidget(self.reset_btn)
        
        # 调换顺序：先添加控制按钮组，再添加开始按钮
        btn_layout.addLayout(control_layout)  # 原顺序：先添加开始按钮，现调整为控制按钮组在前
        # 开始按钮（浅色背景+文字）
        self.draw_btn = QPushButton("开始抽签")
        self.draw_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(33, 150, 243, 0.2);
                color: #2196F3;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                min-width: {self.config.get("draw_btn_width", 120)}px;  /* 读取配置参数 */
                font-size: {self.config.get("font_size", 14)}px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: rgba(33, 150, 243, 0.3);
            }}
            QPushButton:pressed {{
                background-color: rgba(33, 150, 243, 0.4);
            }}
        """)
        btn_layout.addWidget(self.draw_btn)  # 原顺序：后添加控制按钮组，现调整为开始按钮在后
        
        left_layout.addWidget(btn_container, 4)  # 40%高度
        
        # 右边容器（结果显示区）
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(20, 20, 20, 20)
        
        self.result_list = QListWidget()
        self.result_list.setStyleSheet(f"""
            QListWidget {{
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                font-size: {self.config.get("scroll_font_size", 36)}px;
                background-color: #f8f9fa;
            }}
            QListWidget::item {{
                padding: 12px;
                border-bottom: 1px solid #f0f0f0;
            }}
            QListWidget::item:selected {{
                background-color: #e3f2fd;
                color: #1976D2;
            }}
        """)
        right_layout.addWidget(self.result_list)
        
        # 应用布局比例配置
        main_splitter.addWidget(left_container)
        main_splitter.addWidget(right_container)
        # 应用布局比例配置（使用 splitter_ratio 控制左边比例）
        if self.config:
            splitter_ratio = self.config.get("splitter_ratio", 30)
            # 总宽度按 100 份计算，左边占 splitter_ratio%，右边占 100 - splitter_ratio%
            main_splitter.setSizes([splitter_ratio * 10, (100 - splitter_ratio) * 10])  # 放大 10 倍避免过小
        else:
            main_splitter.setSizes([300, 700])  # 默认值（左300px，右700px）

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.addWidget(main_splitter)
        self.setLayout(main_layout)

    # 新增：更新动画状态的方法
    def update_animation_state(self, is_animating: bool):
        """更新动画运行状态（控制按钮可用状态和提示文本）"""
        self.draw_btn.setEnabled(not is_animating)  # 动画运行时禁用开始按钮
        self.stop_btn.setEnabled(is_animating)      # 动画运行时启用中止按钮
        if is_animating:
            self.result_label.setText("正在抽签...")  # 动画运行中提示
        else:
            self.result_label.setText("准备抽签")     # 动画停止后恢复初始提示

    def show_error_message(self, message):
        QMessageBox.critical(self, "错误", message)

    def start_draw(self):
        if not self.controller.is_drawing:  # 新增状态检查
            self.start_btn.setEnabled(False)  # 禁用按钮
            self.controller.start_draw()

    def _on_draw_finished(self):
        self.start_btn.setEnabled(True)  # 抽签完成恢复按钮
    
    def set_button_font(self, font: QFont):  # 现在QFont已正确定义
        """设置所有按钮字体"""
        self.start_btn.setFont(font)
        self.settings_btn.setFont(font)
        self.weight_btn.setFont(font)
        
    def _apply_styles(self):
        """集中处理样式设置"""
        result_font_size = self.config.get("result_font_size", 48)
        scroll_font_size = self.config.get("scroll_font_size", 36)
        
        self.result_label.setStyleSheet(f"""
            font-size: {result_font_size}px;
            font-weight: bold;
            color: #333333;
        """)
        
        self.result_list.setStyleSheet(f"""
            QListWidget {{
                font-size: {scroll_font_size}px;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
            }}
        """)