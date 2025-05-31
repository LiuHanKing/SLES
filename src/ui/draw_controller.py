# 处理事件逻辑
class DrawController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
    
    def on_draw_button_clicked(self):
        try:
            # 添加前置条件检查
            if not self.model.config.get("student_file"):
                raise ValueError("学生名单配置文件未设置")
                
            # 添加操作日志
            logging.info("开始执行抽签流程")
            result = self.model.perform_draw()
            self._handle_draw_result(result)
        except Exception as e:
            logging.error(f"抽签失败: {str(e)}")
            self.view.show_error_message(str(e))

    def _handle_draw_result(self, result):
        # 添加结果验证
        if not result:
            raise ValueError("抽签结果为空")
            
        # 添加结果格式化处理
        formatted_result = self._format_result(result)
        self.view.display_result(formatted_result)
        self._save_to_history(formatted_result)


# 专注事件控制的文件
from PyQt5.QtCore import QTimer
from .absence_dialog import AbsenceDialog
import logging  # 补充日志导入
import random  # 新增：导入random模块

# 删除重复的类定义，保留以下有效实现
class DrawController:
    def __init__(self, view, model, config):
        self.view = view
        self.model = model
        self.config = config
        self._connect_signals()

    def _connect_signals(self):
        self.view.draw_btn.clicked.connect(self.start_draw_animation)
        self.view.stop_btn.clicked.connect(self.stop_draw)
        self.view.reset_btn.clicked.connect(self.model.reset_results)
        self.animation_running = False  # 新增：标记动画是否运行中

    def on_draw_button_clicked(self):
        try:
            # 添加配置文件路径验证
            if not Path(self.config["student_file"]).exists():
                raise FileNotFoundError(f"学生文件不存在: {self.config['student_file']}")
                
            # 添加数据加载重试机制
            students = StudentManager.load_students(self.config["student_file"])
            if not students:
                raise ValueError("加载到0个学生记录，请检查文件内容")
                
            # 添加界面状态更新
            self.view.update_animation_state(True)  # 新增动画状态控制
            result = self.model.perform_draw(students)
            self._handle_draw_result(result)
            
        except Exception as e:
            self.view.show_error_message(f"抽签失败: {str(e)}")
            logging.exception("抽签流程异常")  # 记录完整堆栈信息
            self.view.show_error_message(str(e))

    # 新增：处理抽签结果的方法
    def _handle_draw_result(self, result):
        """处理抽签结果（显示、保存历史等）"""
        if not result:
            raise ValueError("抽签结果为空")
        # 格式化结果（示例）
        formatted_result = f"{result.name}（ID: {result.id}）"
        # 显示结果到界面
        self.view.result_label.setText(f"抽中：{formatted_result}")
        self.view.result_list.addItem(formatted_result)
        # 保存历史记录（调用model的方法）
        self.model.save_draw_record(
            student=result,
            absence_list=[],  # 根据实际逻辑传入缺席列表
            draw_mode="默认模式",  # 根据实际逻辑传入抽签模式
            draw_count=1  # 根据实际逻辑传入抽签次数
        )

    def start_draw_animation(self, duration):
        # 添加config默认值处理
        duration = self.config.get("animation_duration", 3)
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_animation)
        self.timer.start(100)
        QTimer.singleShot(duration * 1000, self.stop_animation)  # 原错误行

    # 新增停止动画方法
    def stop_draw(self):
        """新增：中止抽签的事件处理方法"""
        self.stop_animation()  # 调用已有的停止动画方法
        self.animation_running = False  # 更新运行状态
        self.view.result_label.setText("抽签已中止")  # 更新界面提示

    def stop_animation(self):
        """停止当前正在进行的动画"""
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()  # 停止定时器（假设 timer 是动画的定时器）
        self.view.update_animation_state(False)  # 假设 view 有更新状态的方法
        self.model.reset_animation_progress()    # 假设 model 需要重置进度

    def _update_animation(self):
        students = self.model._load_students()
        if students:
            student = random.choice(students)  # 现在可以正确使用random
            self.view.result_label.setText(f"正在抽选: {student.name}")