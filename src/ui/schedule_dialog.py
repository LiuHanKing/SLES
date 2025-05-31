from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTimeEdit, QFormLayout, QPushButton

class ScheduleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("课程时间设置")
        self.init_ui()
        
    def init_ui(self):
        layout = QFormLayout()
        
        self.start_time = QTimeEdit()
        self.end_time = QTimeEdit()
        
        layout.addRow("课程开始时间:", self.start_time)
        layout.addRow("课程结束时间:", self.end_time)
        
        btn_save = QPushButton("保存设置")
        btn_save.clicked.connect(self.save_settings)
        layout.addWidget(btn_save)
        
        self.setLayout(layout)
        
    def save_settings(self):
        from config.config_manager import ConfigManager
        ConfigManager.update_config({
            "schedule": {
                "start": self.start_time.time().toString("HH:mm"),
                "end": self.end_time.time().toString("HH:mm")
            }
        })
        self.accept()