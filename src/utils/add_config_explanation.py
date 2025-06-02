# 定义配置说明内容
config_explanation = '''### window 窗口配置
- left_ratio: 窗口左右区域的比例（左区域占比），取值范围 10 - 90，当前值 40 表示左区域占 40%。
- top_ratio: 窗口上下区域的比例（上区域占比），当前值 60 表示上区域占 60%。
- width: 窗口的宽度，单位为像素，当前值为 800 像素。
- height: 窗口的高度，单位为像素，当前值为 600 像素。
- start_fullscreen: 窗口是否以全屏模式启动，true 表示全屏启动，false 表示非全屏启动。

### animation 动画配置
- duration: 滚动动画的时长，单位为秒，取值范围 1 - 30，当前值为 5 秒。
- scroll_speed: 结果超过屏幕时滚动的频率，当前值为 50。

### log 日志配置
- level: 日志的级别，可选值有 "DEBUG", "INFO", "WARNING", "ERROR"，当前值为 "INFO"。

### font 字体配置
- name: 字体的名称，当前使用的是 "Arial" 字体。
- drawing_label_size: 绘制标签的字体大小，当前值为 30。
- button_size: 按钮的字体大小，当前值为 24。
- result_text_size: 结果文本的字体大小，当前值为 28。

### excel_file_path Excel 文件路径配置
- excel_file_path: 学生名单 Excel 文件的路径，相对于项目根目录，当前路径为 "conf/students.xlsx"。

### button 按钮配置
#### draw 绘制按钮
- color: 绘制按钮的颜色，使用十六进制颜色码表示，当前颜色为 "#4CAF50"。
- width: 绘制按钮的宽度，单位为像素，当前值为 200 像素。
- height: 绘制按钮的高度，单位为像素，当前值为 80 像素。

#### stop 停止按钮
- color: 停止按钮的颜色，使用十六进制颜色码表示，当前颜色为 "#F44336"。
- width: 停止按钮的宽度，单位为像素，当前值为 100 像素。
- height: 停止按钮的高度，单位为像素，当前值为 50 像素。

#### reset 重置按钮
- color: 重置按钮的颜色，使用十六进制颜色码表示，当前颜色为 "#2196F3"。
- width: 重置按钮的宽度，单位为像素，当前值为 100 像素。
- height: 重置按钮的高度，单位为像素，当前值为 50 像素。

### padding 内边距配置
- padding: 元素的内边距，当前值为 "5px"。

### draw 抽签配置
- allow_repeat: 是否允许本轮抽签重复，true 表示允许，false 表示不允许，当前值为 false。
'''

# 写入文件
file_path = r'conf\conf参数说明.txt'
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(config_explanation)

print("配置说明已成功写入文件。")