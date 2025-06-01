import time
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLabel
import random
from models.student import Student
import logging

logger = logging.getLogger(__name__)

def start_animation(result_label, scroll_speed, duration, callback, student_ids, student_names):
    # 这里可以添加对动画模式的处理，当前假设没有模式要求
    timer = QTimer()
    elapsed_time = 0
    total_time = duration * 1000  # 转换为毫秒

    def update_label():
        nonlocal elapsed_time
        if elapsed_time * scroll_speed >= total_time:
            timer.stop()
            callback()
            return

        # 随机选择一个学生显示
        index = elapsed_time % len(student_ids)
        student_id = student_ids[index]
        student_name = student_names[index]
        if student_id:
            display_text = f"抽签中: {student_id}-{student_name}"
        else:
            display_text = f"抽签中: {student_name}"
        result_label.setText(display_text)

        elapsed_time += 1

    timer.timeout.connect(update_label)
    timer.start(scroll_speed)
    return timer
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLabel
import random
import logging

logger = logging.getLogger(__name__)

def start_animation(result_label, scroll_speed, duration, callback, students=None, mode="rolling"):
    try:
        logger.info(f"开始 {mode} 动画")
        timer = QTimer()
        if mode == "rolling":
            elapsed_time = 0
            def update_label():
                nonlocal elapsed_time
                if elapsed_time >= duration * 1000:
                    timer.stop()
                    callback()
                    logger.info("滚动抽签动画结束")
                    return
                if students:
                    random_student = random.choice(students)
                    if isinstance(random_student, str):
                        result_label.setText(f"抽签中: {random_student}")
                    else:
                        if hasattr(random_student, 'name'):
                            name = random_student.name
                            if hasattr(random_student, 'student_id'):
                                student_id = random_student.student_id
                                result_label.setText(f"抽签中: {student_id}-{name}")
                            else:
                                result_label.setText(f"抽签中: {name}")
                        else:
                            result_label.setText("抽签中: 未知姓名")
                # 每次更新时增加 scroll_speed
                elapsed_time += scroll_speed
            timer.timeout.connect(update_label)
        elif mode == "scroll":
            current_offset = 0
            frame_count = 0
            total_frames = (duration * 1000) // 100
            def update_scroll():
                nonlocal current_offset, frame_count
                current_offset += scroll_speed / 10
                result_label.setStyleSheet(f"margin-left: -{current_offset}px;")
                frame_count += 1
                if frame_count >= total_frames:
                    timer.stop()
                    callback()
                    logger.info("滚动显示结果动画结束")
            timer.timeout.connect(update_scroll)
        else:
            # 当模式无效时，使用默认模式
            logger.warning(f"无效的动画模式: {mode}，将使用默认模式 'rolling'")
            mode = "rolling"
            # 递归调用自身使用默认模式
            return start_animation(result_label, scroll_speed, duration, callback, students, mode)
        
        timer.start(scroll_speed if mode == "rolling" else 100)
        return timer
    except Exception as e:
        logger.error(f"动画启动时发生错误: {e}")
        return None