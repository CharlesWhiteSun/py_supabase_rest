import csv
from datetime import datetime, timedelta

INPUT_CSV = "csv\\plc_device_rows.csv"
OUTPUT_CSV = "csv\\new.csv"


def process_csv():
    with open(INPUT_CSV, "r", newline="", encoding="utf-8") as infile, \
         open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # 新的 title
        writer.writerow(["device_id", "voltage", "current", "timestamp", "date", "hh", "mm", "ss"])

        next(reader)  # 忽略第一行 title

        for row in reader:
            try:
                device_id = row[1]  # 第2欄 device_id
                voltage = row[2]    # 第3欄 voltage
                current = row[3]    # 第4欄 current
                timestamp_str = row[4]  # timestamp

                # 轉換 timestamp
                dt = datetime.fromisoformat(timestamp_str.replace("+00", "")) + timedelta(hours=8)

                date = dt.strftime("%Y-%m-%d") 
                hh = dt.strftime("%H")
                mm = dt.strftime("%M")
                ss = dt.strftime("%S")

                writer.writerow([device_id, voltage, current, dt, date, hh, mm, ss])

            except Exception as e:
                print(f"Error processing row: {row}, error: {e}")


if __name__ == "__main__":
    process_csv()
    print(f"CSV 處理完成，輸出檔案: {OUTPUT_CSV}")
