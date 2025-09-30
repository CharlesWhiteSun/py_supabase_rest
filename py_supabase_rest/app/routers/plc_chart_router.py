from fastapi import APIRouter, HTTPException, Query
from enum import Enum
from typing import Optional
from py_supabase_rest.app.services.plc_device_service import get_data_by_deviceID_and_time
from py_supabase_rest.app.services.plc_chart_service import generate_metric_chart_and_save

router = APIRouter(
    prefix="/plc-chart",
    tags=["PLC Chart"]
)

class Metric(str, Enum):
    voltage = "電壓(Voltage)"
    current = "電流(Current)"

METRIC_MAP = {
    Metric.voltage.value: "voltage",
    Metric.current.value: "current",
}

@router.get(
    "/device-status", 
    summary="產生 PLC Device 電壓與電流圖表", 
    description="可選擇輸出電壓或電流，存圖並回傳成功訊息"
)
async def get_device_status_line_drawing(
    device_id: str = Query(default="PLC-001", description="裝置 ID"),
    start_time: Optional[str] = Query(default="2025-09-30T13:00:00", description="開始時間 (ISO 格式)"),
    end_time: Optional[str] = Query(default="2025-09-30T13:10:00", description="結束時間 (ISO 格式)"),
    metric: Metric = Query(default=Metric.voltage, description="選擇輸出的數據類型")
):
    """
    依 device_id 與時間區間，產生電壓或電流的線圖，存圖並回傳檔案路徑
    """
    try:
        data = get_data_by_deviceID_and_time(device_id, start_time, end_time)

        if not data:
            raise HTTPException(status_code=404, detail="沒有符合條件的資料")

        metric_key = METRIC_MAP[metric.value]

        saved_path = generate_metric_chart_and_save(
            data, metric_key, filename_prefix=f"{device_id}_線條圖"
        )

        return {
            "status": "success",
            "metric": metric.value, # 回傳中文方便 UI 顯示
            "message": "圖表已儲存",
            "file_path": saved_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
