import os  # 新增 os 模块导入
from pathlib import Path
from PyQt5.QtWidgets import QMainWindow, QLabel, QMessageBox, QVBoxLayout, QWidget, QPushButton, QTextEdit, QSplitter, QHBoxLayout, QSpinBox, QComboBox, QFontComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from services.config_service import ConfigService
from services.draw_service import DrawService
from src.services.record_service import RecordService
from services.excel_service import ExcelService
import pandas as pd
import json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.draw_service = DrawService()  # 初始化抽签服务
        self.config = ConfigService.load_config()  # 初始化配置
        # 修正配置文件路径
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'conf', 'config.json')
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            print(f"未找到配置文件: {config_path}")
            QMessageBox.warning(self, "错误", f"未找到配置文件: {config_path}")
        
        # 获取 spacing 参数
        self.spacing = self.config.get('spacing', 50)
        
        # 应用 spacing 参数到布局
        self.init_ui()
        self.auto_load_student_list()
        self.is_drawing = False  # 新增标志位，用于判断是否正在抽签

        # 读取配置中的宽度和高度并设置窗口大小
        window_config = self.config.get('window', {})
        width = window_config.get('width', 800)
        height = window_config.get('height', 600)
        # 不要设置固定大小，允许窗口最大化
        # self.setFixedSize(width, height)
        self.resize(width, height)

        # 读取全屏启动配置并设置
        start_fullscreen = window_config.get('start_fullscreen', False)
        if start_fullscreen:
            self.showMaximized()
        else:
            self.showNormal()

        # 允许窗口最大化
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)

    def init_ui(self):
        # 创建主分割器
        splitter = QSplitter(Qt.Horizontal)

        # 左边布局
        left_widget = QWidget()
        left_layout = QVBoxLayout()

        # 增加伸缩空间，将 “抽签中” 区域往下移动
        # 修改前：left_layout.addStretch()
        left_layout.addStretch(1)  # 可根据实际情况调整数值，数值越大，标签越往下

        # 添加抽签中的姓名显示区域
        self.drawing_label = QLabel("准备抽签", left_widget)
        # 设置标签的对齐方式为水平居中
        self.drawing_label.setAlignment(Qt.AlignHCenter)
        # 允许标签在水平方向上扩展
        self.drawing_label.setWordWrap(False)
        self.drawing_label.setMinimumWidth(100)  # 可以根据实际情况调整最小宽度

        # 设置抽签界面的字体大小
        drawing_font_size = self.config.get('font', {}).get('drawing_label_size', 12)
        drawing_font = self.drawing_label.font()
        drawing_font.setPointSize(drawing_font_size)
        self.drawing_label.setFont(drawing_font)
        left_layout.addWidget(self.drawing_label, alignment=Qt.AlignHCenter)

        # 减少标签和按钮之间的伸缩空间，让按钮往上移动
        # 修改前：left_layout.addStretch()
        left_layout.addStretch(1)  # 可根据实际情况调整数值，数值越小，按钮越往上

        # 从配置文件中获取填充参数
        padding = self.config.get('padding', "10px")  # 可以根据需要调整默认值

        # 获取按钮间距配置
        button_spacing = self.config.get('button', {}).get('spacing', 20)

        # 提取设置按钮样式的函数
        def set_button_style(button, config):
            btn_font_size = self.config.get('font', {}).get('button_size', 12)
            btn_font = button.font()
            btn_font.setPointSize(btn_font_size)
            button.setFont(btn_font)

            padding = f"padding-top: {config.get('padding_top', '5px')}; " \
                      f"padding-bottom: {config.get('padding_bottom', '5px')}; " \
                      f"padding-left: {config.get('padding_left', '10px')}; " \
                      f"padding-right: {config.get('padding_right', '10px')};"
            button.setStyleSheet(f"background-color: {config.get('color', '#FFFFFF')}; {padding}")

            if 'height' in config:
                button.setFixedHeight(config['height'])

        # 设置按钮字体大小，确保 btn_font 被正确定义
        btn_font_size = self.config.get('font', {}).get('button_size', 12)
        btn_font = QFont()
        btn_font.setPointSize(btn_font_size)

        # 添加抽签按钮
        self.draw_btn = QPushButton("开始抽签", left_widget)
        self.draw_btn.clicked.connect(self.start_draw)
        self.draw_btn.setFont(btn_font)  # 这里使用已定义的 btn_font
        draw_btn_config = self.config.get('button', {}).get('draw', {})
        set_button_style(self.draw_btn, draw_btn_config)

        # 提取创建中止和重置按钮的方法
        stop_reset_layout = self.create_stop_reset_buttons()
        # 使用 spacing 参数设置开始抽签按钮和中止、重置按钮布局之间的间距
        left_layout.addWidget(self.draw_btn, alignment=Qt.AlignHCenter)
        left_layout.addSpacing(self.spacing)
        left_layout.addLayout(stop_reset_layout)

        draw_width = draw_btn_config.get('width', 100)
        draw_height = draw_btn_config.get('height', 30)
        self.draw_btn.setFixedSize(draw_width, draw_height)

        # 删除重复创建中止和重置按钮的代码

        left_widget.setLayout(left_layout)

        # 右边布局
        right_widget = QWidget()
        right_layout = QVBoxLayout()

        # 添加结果显示区域
        self.result_text = QTextEdit(right_widget)
        self.result_text.setReadOnly(True)
        # 设置结果显示区域字体大小
        result_font_size = self.config.get('font', {}).get('result_text_size', 12)
        result_font = self.result_text.font()
        result_font.setPointSize(result_font_size)
        self.result_text.setFont(result_font)
        right_layout.addWidget(self.result_text)

        right_widget.setLayout(right_layout)

        # 将左右部件添加到分割器
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)

        # 获取配置文件中的左框比例
        left_ratio = self.config.get('window', {}).get('left_ratio', 40)
        right_ratio = 100 - left_ratio

        # 获取分割器的总宽度
        total_width = splitter.width()
        left_width = int(total_width * left_ratio / 100)
        right_width = total_width - left_width

        # 设置分割器的比例
        splitter.setSizes([left_width, right_width])

        # 设置主窗口的中央部件为分割器
        self.setCentralWidget(splitter)

    def handle_error(self, error_message, log_message=None):
        if log_message:
            print(log_message)
        QMessageBox.warning(self, "错误", error_message)

    def auto_load_student_list(self):
        excel_file_path = self._get_excel_file_path()
        if not excel_file_path:
            return

        try:
            if excel_file_path.exists():
                self._load_or_create_students(excel_file_path)
            else:
                self._create_and_load_sample_file(excel_file_path)
        except Exception as e:
            self.handle_error(f"处理学生名单文件时出错: {e}", f"处理学生名单文件时出错: {e}")

    def _get_excel_file_path(self):
        excel_file_path_str = self.config.get("excel_file_path")
        if not excel_file_path_str:
            print("配置文件中未找到 'excel_file_path' 配置项，请检查配置文件。")
            QMessageBox.warning(self, "错误", "配置文件中未找到 'excel_file_path' 配置项，请检查配置文件。")
            return None
        return Path(__file__).parents[2] / excel_file_path_str

    def _load_or_create_students(self, excel_file_path):
        try:
            df = pd.read_excel(excel_file_path)
            expected_columns = ["学号", "姓名"]
            if all(col in df.columns for col in expected_columns):
                # 去重处理
                df = df.drop_duplicates(subset=["学号"])
                students = ExcelService.load_students(str(excel_file_path))
                self.draw_service.load_students(students)
                print("学生名单自动加载成功")
            else:
                print("Excel 文件列名不匹配，将创建示例文件。")
                self._create_and_load_sample_file(excel_file_path)
        except Exception as e:
            raise

    def _create_and_load_sample_file(self, excel_file_path):
        try:
            excel_file_path.parent.mkdir(parents=True, exist_ok=True)
            sample_data = {
                "学号": [f"00{i}" for i in range(1, 11)],
                "姓名": [f"学生{i}" for i in range(1, 11)]
            }
            df = pd.DataFrame(sample_data)
            df.to_excel(excel_file_path, index=False)
            students = ExcelService.load_students(str(excel_file_path))
            self.draw_service.load_students(students)
            print(f"学生名单文件 {excel_file_path.name} 创建成功并加载")
        except Exception as e:
            self.handle_error(f"创建学生名单文件 {excel_file_path.name} 时出错: {e}", f"创建学生名单文件 {excel_file_path.name} 时出错: {e}")

    def start_draw(self):
        try:
            self.is_drawing = True
            self.draw_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.drawing_label.setText("抽签中: ")
            count = 1  # 单次抽签人数
            mode = "single"  # 抽签模式
            config = ConfigService.load_config()
            duration = config.get("animation", {}).get("duration", 5)
            scroll_speed = config.get("animation", {}).get("scroll_speed", 50)

            # 获取学生列表
            students = self.draw_service.students

            def callback():
                results = self.draw_service.start_draw(count, mode)
                result_str_list = []
                for s in results:
                    student_id = s.student_id if hasattr(s, 'student_id') else ""
                    if student_id:
                        result_str_list.append(f"{student_id}-{s.name}")
                    else:
                        result_str_list.append(s.name)
                result_str = "\n".join(result_str_list)
                # 追加结果到结果显示区域
                current_text = self.result_text.toPlainText()
                if current_text:
                    self.result_text.append(result_str)
                else:
                    self.result_text.setText(result_str)
                self.save_draw_record()  # 保存抽签记录
                self.is_drawing = False
                self.draw_btn.setEnabled(True)
                self.stop_btn.setEnabled(False)
                self.drawing_label.setText("准备抽签")

            # 检查 DrawService.start_animation 方法的参数需求，这里假设需要调整参数
            # 若 start_animation 方法需要 students 参数，可能需要调整方法定义
            self.draw_service.start_animation(duration, callback, scroll_speed, self.drawing_label)

        except ValueError as e:
            print(f"抽签出错: {e}")
            QMessageBox.warning(self, "错误", f"抽签出错: {e}")
            self.is_drawing = False
            self.draw_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.drawing_label.setText("准备抽签")

    def reset_draw(self):
        # 停止正在进行的动画
        self.draw_service.stop_animation()
        # 清空结果显示区域
        self.result_text.clear()
        self.drawing_label.setText("准备抽签")
        # 重置抽签服务状态
        self.draw_service.reset()  # 假设 DrawService 有 reset 方法
        self.is_drawing = False
        self.draw_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

    def save_draw_record(self):
        record = self.draw_service.history[-1]
        RecordService.save_draw_record(record)

    def set_button_style(self, button, config):
        btn_font_size = self.config.get('font', {}).get('button_size', 12)
        btn_font = button.font()
        btn_font.setPointSize(btn_font_size)
        button.setFont(btn_font)

        padding = f"padding-top: {config.get('padding_top', '5px')}; " \
                  f"padding-bottom: {config.get('padding_bottom', '5px')}; " \
                  f"padding-left: {config.get('padding_left', '10px')}; " \
                  f"padding-right: {config.get('padding_right', '10px')};"
        button.setStyleSheet(f"background-color: {config.get('color', '#FFFFFF')}; {padding}")

        if 'height' in config:
            button.setFixedHeight(config['height'])

    def create_stop_reset_buttons(self):
        btn_font_size = self.config.get('font', {}).get('button_size', 12)
        btn_font = QFont()
        btn_font.setPointSize(btn_font_size)

        stop_reset_layout = QHBoxLayout()
        self.stop_btn = QPushButton("中止抽签", self)
        self.stop_btn.clicked.connect(self.stop_draw)
        self.stop_btn.setFont(btn_font)
        self.stop_btn.setEnabled(False)
        stop_btn_config = self.config.get('button', {}).get('stop', {})
        self.set_button_style(self.stop_btn, stop_btn_config)

        self.reset_btn = QPushButton("重置抽签", self)
        self.reset_btn.clicked.connect(self.reset_draw)
        self.reset_btn.setFont(btn_font)
        reset_btn_config = self.config.get('button', {}).get('reset', {})
        self.set_button_style(self.reset_btn, reset_btn_config)

        # 使用 spacing 参数设置中止按钮和重置按钮之间的间距
        stop_reset_layout.addWidget(self.stop_btn)
        stop_reset_layout.addSpacing(self.spacing)
        stop_reset_layout.addWidget(self.reset_btn)
        return stop_reset_layout

    def stop_draw(self):
        try:
            # 停止动画
            self.draw_service.stop_animation()
            self.is_drawing = False
            self.draw_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.drawing_label.setText("准备抽签")
            print("抽签已中止")
        except Exception as e:
            print(f"中止抽签时出错: {e}")
            QMessageBox.warning(self, "错误", f"中止抽签时出错: {e}")
