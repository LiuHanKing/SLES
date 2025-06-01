from datetime import date, time

class DrawRecord:
    def __init__(self, date: date, time: time, results: list, count: int, mode: str):
        self.date = date
        self.time = time
        self.results = results
        self.count = count
        self.mode = mode

    def __str__(self):
        return f"日期: {self.date}, 时间: {self.time}, 模式: {self.mode}, 结果: {', '.join(self.results)}"