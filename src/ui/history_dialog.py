from PyQt5.QtWidgets import QDialog, QListWidget, QVBoxLayout
import json
import os
import logging

class HistoryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("抽签历史记录")
        self.setMinimumSize(400, 300)
        
        layout = QVBoxLayout()
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)
        layout.addWidget(self.list_widget)
        
        self.setLayout(layout)
        self._load_history()
        
    def _load_history(self):
        try:
            history_file = "data/draw_history.json"
            if os.path.exists(history_file):
                with open(history_file, "r", encoding="utf-8") as f:
                    history = [json.loads(line) for line in f]
                    self.list_widget.clear()
                    for record in history:
                        student = record["student"]
                        text = f"{record['time']} - {student['id']} {student['name']}"
                        self.list_widget.addItem(text)
        except Exception as e:
            logging.error(f"加载历史记录失败: {e}")