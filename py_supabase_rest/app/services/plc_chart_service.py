import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.graph_objects as go
import webbrowser
from datetime import datetime

IMAGES_DIR = "images"
INTERACTIVE_DIR = "interactive"

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


def generate_metric_chart_interactive(data, device_id: str, metric: str, filename_prefix: str = "plc_interactive"):
    """
    依照 metric (voltage 或 current) 產生互動式 HTML 圖表，並存到 images 資料夾
    """
    if not data:
        raise ValueError("沒有資料可繪製圖表")

    timestamps = [datetime.fromisoformat(d.timestamp.replace("Z", "+00:00")) for d in data]
    values = [d.voltage if metric == "電壓(Voltage)" else d.current for d in data]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timestamps, y=values, mode="lines+markers", name=metric))

    baseline = 220 if metric == "電壓(Voltage)" else 5.0
    fig.add_hline(y=baseline, line_dash="dash", line_color="red", annotation_text=f"基準線 {baseline}")

    fig.update_layout(
        title=f"{device_id} {metric} 互動式線圖",
        xaxis_title="時間",
        yaxis_title=metric,
        template="plotly_white"
    )

    now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{metric}_{now_str}.html"
    save_path = os.path.join(IMAGES_DIR, filename)
    os.makedirs(IMAGES_DIR, exist_ok=True)
    fig.write_html(save_path)

    webbrowser.open(f"file://{os.path.abspath(save_path)}")
    return save_path