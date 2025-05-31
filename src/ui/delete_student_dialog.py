from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QCheckBox
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton
from PyQt5.QtWidgets import QMessageBox
from data.student_manager import StudentManager

class DeleteStudentDialog(QDialog):
    @staticmethod
    def show_delete_student_dialog(parent):
        """显示删除学生对话框"""
        dialog = QDialog(parent)
        dialog.setWindowTitle("删除学生")
        layout = QVBoxLayout()

        # 加载学生列表
        students = StudentManager.load_students(parent.config["student_file"])
        if not students:
            QMessageBox.information(dialog, "提示", "没有可删除的学生")
            return

        # 创建带复选框的学生列表
        list_widget = QListWidget()
        for student in students:
            item = QListWidgetItem(f"{student.name} ({student.id})")
            checkbox = QCheckBox()
            list_widget.addItem(item)
            list_widget.setItemWidget(item, checkbox)

        layout.addWidget(list_widget)

        # 删除按钮
        delete_btn = QPushButton("删除选中学生")
        delete_btn.clicked.connect(lambda: DeleteStudentDialog._confirm_delete_students(dialog, list_widget, students))
        layout.addWidget(delete_btn)

        dialog.setLayout(layout)
        dialog.exec_()

    @staticmethod
    def _confirm_delete_students(dialog, list_widget, students):
        deleted_ids = []
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            checkbox = list_widget.itemWidget(item)
            if checkbox.isChecked():
                deleted_ids.append(students[i].id)
        
        if deleted_ids:
            StudentManager.delete_students(deleted_ids)
            QMessageBox.information(dialog, "提示", f"已删除{len(deleted_ids)}名学生")
            dialog.accept()