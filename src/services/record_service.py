import csv
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class RecordService:
    @staticmethod
    def save_draw_record(record):
        logs_dir = Path(__file__).parents[2] / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        csv_file_path = logs_dir / "draw_records.csv"

        # 写入 CSV 文件
        with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
            if hasattr(record, "to_dict"):
                row = record.to_dict()
            else:
                row = record
            fieldnames = row.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(row)