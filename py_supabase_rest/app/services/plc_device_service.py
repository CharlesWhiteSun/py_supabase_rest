from typing import List, Optional
from datetime import datetime, timedelta
from py_supabase_rest.app.config import supabase
from py_supabase_rest.app.dao.models import PLCData


TABLE_NAME = "plc_device"


def get_plc_device_data(limit: int = 10) -> List[PLCData]:
    """
    從 Supabase 撈取 PLC Device 資料，限制筆數
    並轉換成 PLCData 型別
    """
    response = supabase.table(TABLE_NAME).select("*").limit(limit).execute()
    
    if not response.data:
        return []
    
    if hasattr(response, "status") and response.status != "success":
        raise Exception(f"Supabase 查詢失敗: {response}")

    return [PLCData(**item) for item in response.data]


def get_data_by_deviceID_and_time(
    device_id: str,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None
) -> List[PLCData]:
    """
    根據 device_id 與時間區間查詢 PLC 資料
    """
    query = supabase.table(TABLE_NAME).select("*").eq("device_id", device_id)

    # 處理時間轉換：從 UTC+8 轉為 UTC+0
    if start_time:
        start_dt = datetime.fromisoformat(start_time) - timedelta(hours=8)
        start_time = start_dt.isoformat()
        query = query.gte("timestamp", start_time)

    if end_time:
        end_dt = datetime.fromisoformat(end_time) - timedelta(hours=8)
        end_time = end_dt.isoformat()
        query = query.lte("timestamp", end_time)

    response = query.order("timestamp", desc=False).execute()

    if not hasattr(response, "data") or not isinstance(response.data, list):
        return []

    return [PLCData(**item) for item in response.data]