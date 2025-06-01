import csv
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class RecordService:
    @staticmethod
    def save_draw_record(record, file_path="draw_records.csv"):
        try:
            with open(file_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if f.tell() == 0:
                    writer.writerow(["抽签日期", "抽签时间", "抽签结果", "抽签人数", "抽签方式", "抽签次数"])
                writer.writerow([
                    record.date,
                    record.time,
                    ",".join(record.results),
                    record.count,
                    record.mode,
                    record.count
                ])
        except (IOError, csv.Error) as e:
            logger.error(f"保存抽签记录时出错: {e}")