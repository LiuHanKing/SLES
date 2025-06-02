import csv
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class RecordService:
    @staticmethod
    def save_draw_record(record):
        # 构建 logs 目录下的文件路径
        logs_dir = Path(__file__).parents[2] / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        csv_file_path = logs_dir / "draw_records.csv"

        # 写入 CSV 文件
        with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = record.keys()  # 假设 record 是字典
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # 如果文件为空，写入表头
            if csvfile.tell() == 0:
                writer.writeheader()

            writer.writerow(record)