# 样式管理
def apply_global_style(widget):
    """应用全局样式"""
    widget.setStyleSheet(f"""
        QWidget {{
            font-family: "Microsoft YaHei";
            font-size: {get_stylesheet(14)};
        }}
        QPushButton {{
            {get_stylesheet(14)}
            padding: 8px 16px;
            border-radius: 4px;
            min-width: 80px;
        }}
        QListWidget::item {{
            padding: 8px;
            margin: 2px;
            background-color: #e9f5ff;
            border-radius: 4px;
            border: 1px solid #dee2e6;
        }}
        /* 新增菜单样式 */
        QMenu {{
            background-color: #ffffff;  /* 菜单背景色 */
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            padding: 4px;
        }}
        QMenu::item {{
            color: #333333;  /* 菜单项文字颜色 */
            padding: 6px 24px;
            min-width: 120px;
        }}
        QMenu::item:selected {{
            background-color: #e3f2fd;  /* 悬停时背景色 */
            color: #1976D2;
        }}
    """)

def get_stylesheet(font_size):
    """生成动态字体样式"""
    return f"""
        font-size: {font_size}px;
        font-weight: {'bold' if font_size > 16 else 'normal'};
    """