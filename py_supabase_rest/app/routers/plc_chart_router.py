from enum import Enum
from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException, Query
from py_supabase_rest.app.services.plc_device_service import get_data_by_deviceID_and_time
from py_supabase_rest.app.services.plc_chart_service import (
    generate_metric_chart_and_save, 
    generate_metric_chart_interactive,
    generate_metric_chart_3d,
)

router = APIRouter(
    prefix="/plc-chart",
    tags=["PLC Chart"]
)

class Metric(str, Enum):
    voltage = "電壓(Voltage)"
    current = "電流(Current)"

class DeviceID(str, Enum):
    PLC_001 = "PLC-001"
    PLC_006 = "PLC-006"
    PLC_008 = "PLC-008"
    PLC_010 = "PLC-010"

class DateEnum(str, Enum):
    date1 = "2025-09-30"
    date2 = "2025-10-01"

class HourEnum(str, Enum):
    h00 = "00"
    h01 = "01"
    h02 = "02"
    h03 = "03"
    h04 = "04"
    h05 = "05"
    h06 = "06"
    h07 = "07"
    h08 = "08"
    h09 = "09"
    h10 = "10"
    h11 = "11"
    h12 = "12"
    h13 = "13"
    h14 = "14"
    h15 = "15"
    h16 = "16"
    h17 = "17"
    h18 = "18"
    h19 = "19"
    h20 = "20"
    h21 = "21"
    h22 = "22"
    h23 = "23"

class MinuteSecondEnum(str, Enum):
    ms00 = "00"
    ms01 = "01"
    ms02 = "02"
    ms03 = "03"
    ms04 = "04"
    ms05 = "05"
    ms06 = "06"
    ms07 = "07"
    ms08 = "08"
    ms09 = "09"
    ms10 = "10"
    ms11 = "11"
    ms12 = "12"
    ms13 = "13"
    ms14 = "14"
    ms15 = "15"
    ms16 = "16"
    ms17 = "17"
    ms18 = "18"
    ms19 = "19"
    ms20 = "20"
    ms21 = "21"
    ms22 = "22"
    ms23 = "23"
    ms24 = "24"
    ms25 = "25"
    ms26 = "26"
    ms27 = "27"
    ms28 = "28"
    ms29 = "29"
    ms30 = "30"
    ms31 = "31"
    ms32 = "32"
    ms33 = "33"
    ms34 = "34"
    ms35 = "35"
    ms36 = "36"
    ms37 = "37"
    ms38 = "38"
    ms39 = "39"
    ms40 = "40"
    ms41 = "41"
    ms42 = "42"
    ms43 = "43"
    ms44 = "44"
    ms45 = "45"
    ms46 = "46"
    ms47 = "47"
    ms48 = "48"
    ms49 = "49"
    ms50 = "50"
    ms51 = "51"
    ms52 = "52"
    ms53 = "53"
    ms54 = "54"
    ms55 = "55"
    ms56 = "56"
    ms57 = "57"
    ms58 = "58"
    ms59 = "59"

class Mode(str, Enum):
    static = "static"
    interactive = "interactive"

@router.get(
    "/device-line_drawing", 
    summary="產生 PLC 設備電壓, 電流圖表", 
    description="可輸出電壓或電流折線圖並直接另存圖片"
)
async def get_device_line_drawing(
    device_id: DeviceID = Query(default=DeviceID.PLC_001, description="裝置 ID"),
    start_date: DateEnum = Query(default=DateEnum.date1, description="開始日期"),
    start_hh: HourEnum = Query(default=HourEnum.h13, description="開始小時"),
    start_mm: MinuteSecondEnum = Query(default=MinuteSecondEnum.ms00, description="開始分鐘"),
    end_date: DateEnum = Query(default=DateEnum.date1, description="結束日期"),
    end_hh: HourEnum = Query(default=HourEnum.h13, description="結束小時"),
    end_mm: MinuteSecondEnum = Query(default=MinuteSecondEnum.ms10, description="結束分鐘"),
    metric: Metric = Query(default=Metric.voltage, description="選擇輸出的數據類型"),
    mode: Mode = Query(default=Mode.interactive, description="輸出模式：static=靜態圖片, interactive=互動式網頁圖表")
):
    """
    依 device_id 與時間區間，產生電壓或電流的線圖，存圖並回傳檔案路徑
    """
    try:
        data = get_data_by_deviceID_and_time(
            device_id.value,
            start_date.value, start_hh.value, start_mm.value,
            end_date.value, end_hh.value, end_mm.value
        )

        if not data:
            raise HTTPException(status_code=404, detail="沒有符合條件的資料")

        if mode == Mode.static:
            saved_path = generate_metric_chart_and_save(
                data, device_id.value, metric.value, filename_prefix=f"線條圖_{device_id.value}"
            )
        elif mode == Mode.interactive:
            saved_path = generate_metric_chart_interactive(
                data, device_id.value, metric.value, filename_prefix=f"線條圖_{device_id.value}"
            )
            # 直接回傳 HTML 頁面
            import aiofiles
            async with aiofiles.open(saved_path, "r", encoding="utf-8") as f:
                await f.read()
        
        return {
            "status": "success",
            "mode": mode.value,
            "metric": metric.value,
            "message": "圖表已儲存(PNG)",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/device-line_drawing/3d",
    summary="產生 PLC 多設備 3D 折線圖",
    description="支援 3D 互動式或靜態圖表"
)
async def get_device_line_drawing_3d(
    device_ids: List[DeviceID] = Query(default=[DeviceID.PLC_001], description="請至少選擇一個裝置 ID(按住 Ctrl 以便多選)"),
    start_date: DateEnum = Query(default=DateEnum.date1, description="開始日期"),
    start_hh: HourEnum = Query(default=HourEnum.h13, description="開始小時"),
    start_mm: MinuteSecondEnum = Query(default=MinuteSecondEnum.ms00, description="開始分鐘"),
    end_date: DateEnum = Query(default=DateEnum.date1, description="結束日期"),
    end_hh: HourEnum = Query(default=HourEnum.h13, description="結束小時"),
    end_mm: MinuteSecondEnum = Query(default=MinuteSecondEnum.ms10, description="結束分鐘"),
    metric: Metric = Query(default=Metric.voltage, description="選擇輸出的數據類型"),
    mode: Mode = Query(default=Mode.interactive, description="輸出模式：static=靜態圖片, interactive=互動式網頁圖表")
):
    try:
        all_data = []
        for device_id in device_ids:
            data = get_data_by_deviceID_and_time(
                device_id.value,
                start_date.value, start_hh.value, start_mm.value,
                end_date.value, end_hh.value, end_mm.value
            )
            if not data:
                continue
            all_data.append((device_id.value, data))

        if not all_data:
            raise HTTPException(status_code=404, detail="沒有符合條件的資料")

        x_label_start_time = datetime.fromisoformat(start_date + "T" + start_hh + ":" + start_mm + ":00")
        x_label_end_time = datetime.fromisoformat(end_date + "T" + end_hh + ":" + end_mm + ":00")

        saved_path = generate_metric_chart_3d(all_data, metric.value, mode.value, x_label_start_time, x_label_end_time, filename_prefix="3d_chart")

        if mode == Mode.interactive:
            import aiofiles
            async with aiofiles.open(saved_path, "r", encoding="utf-8") as f:
                await f.read()

        return {
            "status": "success",
            "mode": mode.value,
            "metric": metric.value,
            "message": "3D 圖表已產生(Html)",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))