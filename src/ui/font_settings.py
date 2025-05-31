from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QPushButton

class FontSettings:
    @staticmethod
    def show_font_settings(parent):
        """显示字体设置对话框"""
        dialog = QDialog(parent)
        dialog.setWindowTitle("字体设置")
        layout = QVBoxLayout()

        # 抽签字体设置
        layout.addWidget(QLabel("抽签字体大小:"))
        draw_font = QSpinBox()
        draw_font.setRange(12, 72)
        draw_font.setValue(parent.draw_font_size)
        layout.addWidget(draw_font)

        # 按钮字体设置
        layout.addWidget(QLabel("按钮字体大小:"))
        button_font = QSpinBox()
        button_font.setRange(8, 36)
        button_font.setValue(parent.button_font_size)
        layout.addWidget(button_font)

        # 结果字体设置
        layout.addWidget(QLabel("结果字体大小:"))
        result_font = QSpinBox()
        result_font.setRange(8, 999)
        result_font.setValue(parent.result_font_size)
        layout.addWidget(result_font)

        # 确认按钮
        confirm_btn = QPushButton("确认")
        confirm_btn.clicked.connect(lambda: parent._apply_font_settings(
            draw_font.value(),
            button_font.value(),
            result_font.value()
        ))
        confirm_btn.clicked.connect(dialog.accept)
        layout.addWidget(confirm_btn)

        dialog.setLayout(layout)
        dialog.exec_()