from datetime import date, time

class DrawRecord:
    def __init__(self, date: date, time: time, results: list, count: int, mode: str, draw_times: int = 1):
        self.date = date
        self.time = time
        self.results = results
        self.count = count
        self.mode = mode
        self.draw_times = draw_times

    def to_dict(self):
        return {
            "日期": str(self.date),
            "时间": str(self.time),
            "抽签结果": ','.join(self.results),
            "抽签人数": self.count,
            "抽签方式": self.mode,
            "抽签次数": self.draw_times
        }

    def __str__(self):
        return f"日期: {self.date}, 时间: {self.time}, 模式: {self.mode}, 结果: {', '.join(self.results)}"