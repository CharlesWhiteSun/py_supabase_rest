import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.graph_objects as go
import webbrowser
from datetime import datetime, timedelta

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

    fig.update_layout(
        title=f"{device_id} {metric} 互動式線圖",
        xaxis_title="時間",
        yaxis_title=metric,
        template="plotly_dark"
    )

    now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{metric}_{now_str}.html"
    save_path = os.path.join(IMAGES_DIR, filename)
    os.makedirs(IMAGES_DIR, exist_ok=True)
    fig.write_html(save_path)

    webbrowser.open(f"file://{os.path.abspath(save_path)}")
    return save_path


def generate_metric_chart_3d(
        all_data, 
        metric: str, 
        mode: str, 
        x_label_start_time: datetime, 
        x_label_end_time: datetime, 
        filename_prefix: str = "plc_3d_chart",
    ):
    """
    all_data: List[(device_id, data)]
    metric: "電壓(Voltage)" 或 "電流(Current)"
    """

    fig = go.Figure()

    for device_id, data in all_data:
        # 先做安全的時間排序，避免亂跳
        sorted_data = sorted(
            data,
            key=lambda d: (
                d.date,                  # 日期
                d.hh,                    # 小時
                d.mm,                    # 分鐘
                getattr(d, "ss", "00")   # 秒 (可選，預設 "00")
            )
        )

        # 轉換為時間秒數（相對起始時間）
        base_time = datetime.fromisoformat(sorted_data[0].timestamp.replace("Z", "+00:00"))
        x_value = [
            (datetime.fromisoformat(d.timestamp.replace("Z", "+00:00")) - base_time).total_seconds()
            for d in sorted_data
        ]

        z_value = [
            d.voltage if metric == "電壓(Voltage)" else d.current
            for d in sorted_data
        ]
        y_value = [device_id] * len(z_value)

        fig.add_trace(go.Scatter3d(
            x=x_value,
            y=y_value,
            z=z_value,
            mode="lines+markers",
            name=device_id,
            marker=dict(size=2),  # 縮小點
            line=dict(width=1)
        ))

    # 為 X 軸生成刻度
    total_seconds = (x_label_end_time - x_label_start_time).total_seconds()
    tickvals = list(range(0, int(total_seconds) + 1, max(1, int(total_seconds) // 10)))
    ticktext = [
        (x_label_start_time + timedelta(seconds=sec)).strftime("%H:%M:%S")
        for sec in tickvals
    ]

    all_device_ids = [device_id for device_id, _ in all_data]
    fig.update_layout(
        title=f"多設備 {metric} 3D 折線圖",
        scene=dict(
            xaxis=dict(
                title="時間",
                type="linear",
                tickvals=tickvals,
                ticktext=ticktext
            ),
            yaxis=dict(
                title="Device ID",
                range=[-0.5, len(all_device_ids) - 0.5]  # 上下留空
            ),
            zaxis_title=metric,
        ),
        template="plotly_dark"
    )

    now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(IMAGES_DIR, exist_ok=True)

    if mode == "interactive":
        filename = f"{filename_prefix}_{metric}_{now_str}.html"
        save_path = os.path.join(IMAGES_DIR, filename)
        fig.write_html(save_path)
        webbrowser.open(f"file://{os.path.abspath(save_path)}")

    else:
        try:
            import kaleido  # Plotly 靜態輸出套件
        except ImportError:
            raise RuntimeError("OS 環境缺少 kaleido 套件, 安裝指令: pip install kaleido")
        filename = f"{filename_prefix}_{metric}_{now_str}.png"
        save_path = os.path.join(IMAGES_DIR, filename)
        fig.write_image(save_path, format="png")

    return save_path
