# 修改导入部分
from PyQt5.QtWidgets import (QMainWindow, QMenuBar, QAction, QDialog, 
                            QVBoxLayout, QLabel, QTimeEdit, QPushButton, 
                            QHBoxLayout, QMessageBox, QWidget, QApplication, 
                            QFontDialog, QTextEdit)  # 新增QTextEdit导入
from ui.draw_panel import DrawPanel
from ui.setting_panel import SettingPanel
from ui.history_dialog import HistoryDialog
import logging
from config.config_manager import ConfigManager
from PyQt5.QtGui import QFont  # 添加这行导入
from PyQt5.QtWidgets import QMainWindow
from .draw_panel import DrawPanel
from PyQt5.QtWidgets import QSizePolicy  # 新增导入

class MainWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config  # 接收全局配置
        self.init_ui()

    def init_ui(self):
        # 直接使用容器布局
        container = QWidget()
        self.main_layout = QVBoxLayout(container)
        self.draw_panel = DrawPanel(parent=self, config=self.config)
        # 替换为直接操作splitter设置比例（假设DrawPanel包含splitter属性）
        if hasattr(self.draw_panel, 'splitter'):
            total_width = self.width()  # 获取当前窗口宽度
            left_width = int(total_width * 0.3)  # 默认左侧占30%
            right_width = total_width - left_width
            self.draw_panel.splitter.setSizes([left_width, right_width])
        self.main_layout.addWidget(self.draw_panel)
        self.setCentralWidget(container)
        self.resize(800, 600)
        self.setWindowTitle("学生抽签系统")
        self.init_menu()  # 确保菜单初始化

        # 应用全局样式（改为绝对导入）
        # 应用全局样式（增加异常处理）
        try:
            from src.utils.style_manager import apply_global_style
            apply_global_style(self)
        except ImportError as e:
            logging.error("样式加载失败: %s", str(e))
        
        self.show()
        QApplication.processEvents()

    # 删除重复的垂直布局init_ui方法（保留水平布局版本）
    # 合并重复导入（保留最终版）
    from PyQt5.QtWidgets import (QMainWindow, QMenuBar, QAction, QDialog, 
                                QVBoxLayout, QLabel, QTimeEdit, QPushButton, 
                                QHBoxLayout, QMessageBox, QWidget, QApplication, 
                                QFontDialog, QTextEdit)  # 包含QTextEdit的完整导入
    # 修改前的错误导入
    # from ui.draw_panel import DrawPanel
    
    # 修改后的正确导入（使用绝对路径）
    from src.ui.draw_panel import DrawPanel
    from ui.setting_panel import SettingPanel
    from ui.history_dialog import HistoryDialog
    import logging
    from config.config_manager import ConfigManager
    from PyQt5.QtGui import QFont
    from .draw_panel import DrawPanel  # 清理重复的DrawPanel导入
    
    # 删除重复的MainWindow类定义（保留唯一实例）
    # class MainWindow(QMainWindow):  # 注释掉重复定义
    #     def __init__(self, config):
    #         super().__init__()
    #         self.config = config
    #         self.init_ui()
    # 删除重复的init_ui方法，保留以下有效实现
    def init_ui(self):
        container = QWidget()
        self.main_layout = QHBoxLayout(container)
        self.main_layout.setContentsMargins(0,0,0,0)
        
        # 确保DrawPanel正确初始化
        self.draw_panel = DrawPanel(parent=self, config=self.config)
        self.main_layout.addWidget(self.draw_panel)
        
        self.setCentralWidget(container)
        self.setWindowTitle("学生抽签系统 V2.0")
        self.init_menu()
        self.show()  # 新增显示主窗口

    def init_menu(self):
        """初始化完整菜单结构"""
        menu_bar = QMenuBar(self)
        
        # 系统设置菜单
        system_menu = menu_bar.addMenu("系统设置")
        param_action = QAction("参数设置", self)
        font_action = QAction("字体设置", self)
        # 新增"关于系统"菜单项
        about_action = QAction("关于系统", self)
        # 添加所有菜单项（包含新增的关于系统）
        system_menu.addActions([param_action, font_action, about_action])
        param_action.triggered.connect(self.show_settings)
        font_action.triggered.connect(self.set_global_font)
        # 连接关于系统的点击事件
        about_action.triggered.connect(self.show_about_dialog)

        # 抽签管理菜单
        draw_menu = menu_bar.addMenu("抽签管理")
        mode_action = QAction("抽签模式设置", self)
        display_action = QAction("抽签显示设置", self)
        weight_action = QAction("抽签权重设置", self)
        history_action = QAction("抽签历史查看", self)
        draw_menu.addActions([mode_action, display_action, weight_action, history_action])
        weight_action.triggered.connect(self.draw_panel.show_weight_manager)
        history_action.triggered.connect(self.show_history)

        # 学生管理菜单
        student_menu = menu_bar.addMenu("学生管理")
        add_action = QAction("添加学生", self)
        del_action = QAction("删除学生", self)
        absence_action = QAction("缺席设置", self)
        student_menu.addActions([add_action, del_action, absence_action])
        add_action.triggered.connect(self.show_add_student_dialog)
        absence_action.triggered.connect(self.show_absence_dialog)

        # 课程作息菜单
        schedule_menu = menu_bar.addMenu("课程作息管理")
        time_action = QAction("课程时间设置", self)
        schedule_menu.addAction(time_action)
        time_action.triggered.connect(self.show_schedule_settings)

        self.setMenuBar(menu_bar)

    def show_error_dialog(self, message):
        """新增缺失的错误提示方法"""
        QMessageBox.critical(self, "错误", message)

    def show_settings(self):
        """显示系统设置面板"""
        from .setting_panel import SettingPanel
        self.setting_panel = SettingPanel(self.config)
        self.setting_panel.show()

    def show_add_student_dialog(self):
        """显示添加学生对话框"""
        from .student_dialog import StudentDialog
        dialog = StudentDialog(self)
        if dialog.exec_():
            student_id, name = dialog.get_student_info()
            if student_id and name:
                StudentManager.add_student(student_id, name)

    def show_history(self):
        """显示历史记录对话框"""
        from .history_dialog import HistoryDialog
        dialog = HistoryDialog(self)
        dialog.exec_()


    def reset_layout(self):
        """重置窗口布局"""
        self.draw_panel.set_splitter_ratio(30)
        QMessageBox.information(self, "提示", "布局已重置为默认")

    def set_global_font(self):
        """改进后的字体设置方法"""
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox
        from utils.constants import FontApplyArea  # 确保在此处导入枚举
        
        dialog = QDialog(self)
        layout = QVBoxLayout()
        
        # 字体选择控件
        font_dialog = QFontDialog(self)
        
        # 区域选择控件
        area_buttons = QDialogButtonBox()
        for area in FontApplyArea:  # 现在FontApplyArea已正确引用
            btn = area_buttons.addButton(area.value, QDialogButtonBox.ActionRole)
            btn.setObjectName(area.name)
        
        layout.addWidget(font_dialog)
        layout.addWidget(area_buttons)
        dialog.setLayout(layout)
        
        def apply_font():
            font = font_dialog.currentFont()
            area = FontApplyArea[area_buttons.checkedButton().objectName()]
            self.draw_panel.apply_global_font(font, area)
            dialog.accept()
        
        area_buttons.accepted.connect(apply_font)
        area_buttons.rejected.connect(dialog.reject)
        dialog.exec_()

    def show_absence_dialog(self):
        """显示缺席设置对话框"""
        from .absence_dialog import AbsenceDialog
        dialog = AbsenceDialog(self)
        dialog.exec_()

    def show_schedule_settings(self):
        """课程时间设置"""
        from .schedule_dialog import ScheduleDialog
        dialog = ScheduleDialog(self)
        if dialog.exec_():
            QMessageBox.information(self, "成功", "课程时间设置已更新")

    # 在closeEvent方法中移除配置保存逻辑
    def closeEvent(self, event):
        try:
            # 移除保存布局的代码
            pass
        except Exception as e:
            # 移除错误处理代码
            pass
        finally:
            event.accept()

    def show_about_dialog(self):
        """显示关于系统对话框（支持文本复制）"""
        dialog = QDialog(self)
        dialog.setWindowTitle("关于系统")
        dialog.setMinimumSize(600, 300)  # 增大最小尺寸
        dialog.resize(800, 400)  # 设置默认尺寸
        
        layout = QVBoxLayout()
        
        # 使用QTextEdit支持文本选择复制
        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_text.setText("""
            学生抽签系统 V2.0\n
            开发者：Liuzhiwen\n
            版本日期：2025-06\n
            功能说明：支持班级学生随机抽签、权重设置、历史记录查询等功能\n
            技术支持：liuzhiwenmr@gmail.com
            https://github.com/LiuHanKing/SLES
        """)
        about_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # 添加自适应策略
        
        layout.addWidget(about_text)
        dialog.setLayout(layout)
        dialog.exec_()