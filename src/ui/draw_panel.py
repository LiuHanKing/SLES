# 顶部统一导入（确保顺序正确）
from PyQt5.QtCore import Qt  # 新增Qt模块导入
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QSplitter, QVBoxLayout, QWidget, QTableWidgetItem, 
                            QTableWidget, QLabel, QScrollArea)
from utils.constants import FontApplyArea
from .draw_view import DrawView
from .draw_model import DrawModel
from .draw_controller import DrawController
from .draw_settings_dialog import DrawSettingsDialog
from .weight_manager_dialog import WeightManagerDialog
# 在顶部导入部分新增QTimer
from PyQt5.QtCore import QTimer  # 新增导入

class DrawPanel(QWidget):
    def __init__(self, parent=None, config=None):
        super().__init__(parent)
        self.config = config
        self.splitter_ratio = 30
        self._init_view()
        self._init_ui()

    def _init_view(self):
        self.view = DrawView(self, config=self.config)
        self.model = DrawModel(self.config)
        self.controller = DrawController(self.view, self.model, self.config)
        self.result_list = QTableWidget()  # 现在 QTableWidget 已正确导入

    def _init_ui(self):
        self.splitter = QSplitter(Qt.Horizontal)
        try:
            self.splitter_ratio = int(self.config.get("splitter_ratio", 30))
        except (ValueError, TypeError) as e:
            self.splitter_ratio = 30
            logging.warning(f"使用默认分割比例: {self.splitter_ratio}%")
        
        # 确保视图正确初始化
        self._init_view()  # 新增调用视图初始化
        self.splitter.addWidget(self.view)
        self.splitter.addWidget(self._create_result_panel())
        
        # 延迟计算窗口尺寸
        # 确保QTimer调用正确
        QTimer.singleShot(100, self.adjust_splitter)

    def adjust_splitter(self):
        total_width = self.width()
        if total_width <= 0:
            total_width = 800  # 设置默认宽度
        left_width = int(total_width * self.splitter_ratio / 100)
        self.splitter.setSizes([left_width, total_width - left_width])

    def _create_result_panel(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)  # 添加自适应设置
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(QLabel("抽签结果"))  # 添加标题
        
        # 初始化表格时添加默认数据占位符
        self.result_list = QTableWidget()
        self.result_list.setRowCount(1)
        self.result_list.setItem(0, 0, QTableWidgetItem("等待抽签结果..."))
        
        layout.addWidget(self.result_list)
        scroll.setWidget(container)
        return scroll

    def _update_result_display(self):
        """================= 动态布局核心 =================
        布局流程：
            1. 计算可用宽度 → 2. 确定列数 → 3. 分配列宽 → 4. 填充数据
        """
        # 计算可用宽度（扣除滚动条宽度）
        available_width = self.result_list.viewport().width() - 20
        
        # 列数计算逻辑
        min_col_width = 220  # 可调整的最小列宽
        max_columns = max(1, available_width // min_col_width)
        columns = min(len(self.current_draw_results), max_columns)
        
        # 列宽分配（保留5px列间距）
        col_width = (available_width - 20) // columns
        self.result_list.setColumnCount(columns)
        for col in range(columns):
            self.result_list.setColumnWidth(col, col_width - 5)  # 每列留出间距
            
        # 行数计算（总数/列数，向上取整）
        self.result_list.setRowCount((len(self.current_draw_results) + columns - 1) // columns)
        
        # 填充学生数据
        for idx, student_id in enumerate(self.current_draw_results):
            row = idx // columns
            col = idx % columns
            student = self.model.get_student_by_id(student_id)
            item = QTableWidgetItem(student.name)
            self.result_list.setItem(row, col, item)

    def apply_global_font(self, font: QFont, area: FontApplyArea):
        """修复字体设置核心方法"""
        if area in [FontApplyArea.GLOBAL, FontApplyArea.OPERATION_PANEL]:
            self.view.setFont(font)
            self.view.set_button_font(font)
        if area in [FontApplyArea.GLOBAL, FontApplyArea.RESULT_AREA]:
            self.result_list.setFont(font)

    def show_weight_manager(self):
        """权重管理对话框入口方法（修复AttributeError）"""
        weight_dialog = WeightManagerDialog(self)
        weight_dialog.exec_()
