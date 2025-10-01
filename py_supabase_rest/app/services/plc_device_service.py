from typing import List, Optional
from datetime import datetime, timedelta
from py_supabase_rest.app.config import supabase
from py_supabase_rest.app.dao.models import PLCData


TABLE_NAME = "plc_device"

def get_data_by_deviceID_and_time(
    device_id: str,
    start_date: str, start_hh: str, start_mm: str,
    end_date: str, end_hh: str, end_mm: str
) -> List[PLCData]:
    """
    根據 device_id 與時間區間查詢 PLC 資料
    """
    if not all([start_date, start_hh, start_mm, end_date, end_hh, end_mm]):
        raise ValueError("所有時間參數都必須有值")
    
    query = supabase.table(TABLE_NAME).select("*").eq("device_id", device_id)

    # 使用複合索引順序過濾
    query = query.gte("date", start_date).lte("date", end_date)
    query = query.gte("hh", start_hh).lte("hh", end_hh)
    query = query.gte("mm", start_mm).lte("mm", end_mm)
    # 排序確保時間正確
    query = query.order("date", desc=False)\
                .order("hh", desc=False)\
                .order("mm", desc=False)\
                .order("ss", desc=False)
    
    response = query.execute()

    if not hasattr(response, "data") or not isinstance(response.data, list):
        return []

    sorted_data = sorted(
        response.data,
        key=lambda x: (x["date"], x["hh"], x["mm"], x["ss"])
    )

    return [PLCData(**item) for item in sorted_data]
