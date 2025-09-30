import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

IMAGES_DIR = "images"

def generate_metric_chart_and_save(data, device_id: str, metric: str, filename_prefix: str = "plc_image"):
    """
    依照 metric (voltage 或 current) 產生線圖，並存到 imgs 資料夾
    x 軸僅顯示 "start_time ~ end_time"
    """
    if not data:
        raise ValueError("沒有資料可繪製圖表")

    # 保留 datetime 作為 x 軸
    timestamps = []
    for d in data:
        # 確保轉成 datetime，並加 +8 小時
        dt = datetime.fromisoformat(d.timestamp.replace("Z", "+00:00"))
        timestamps.append(dt)

    values = [d.voltage if metric == "電壓(Voltage)" else d.current for d in data]
    color = "blue" if metric == "電壓(Voltage)" else "green"

    plt.rcParams["font.family"] = ["Microsoft JhengHei", "Arial Unicode MS"]
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, values, color=color, marker="o", linestyle="-", label=metric)

    # 加入基準線
    baseline = 220 if metric == "電壓(Voltage)" else 5.0
    plt.axhline(y=baseline, color="red", linestyle="--", linewidth=1.5, label=f"基準線: {baseline}")

    # 增加上下邊界空白
    min_val, max_val = min(values), max(values)
    padding = (max_val - min_val) * 0.1 if max_val != min_val else 1
    plt.ylim(min_val - padding, max_val + padding)

    plt.title(f"{device_id} {metric} 線條圖")
    plt.ylabel(metric)
    plt.legend()

    # 顯示的 x 軸：只放區間範圍
    start_label = timestamps[0].strftime("%Y-%m-%d %H:%M")
    end_label = timestamps[-1].strftime("%Y-%m-%d %H:%M")
    plt.xlabel(f"{start_label} ~ {end_label}")

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
    plt.xticks([])

    # 檔名加上當前時間
    now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{metric}_{now_str}.png"
    save_path = os.path.join(IMAGES_DIR, filename)
    os.makedirs(IMAGES_DIR, exist_ok=True)
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()

    return save_path
