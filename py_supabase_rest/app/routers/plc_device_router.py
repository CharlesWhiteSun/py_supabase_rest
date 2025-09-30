from fastapi import APIRouter, HTTPException
from typing import List
from py_supabase_rest.app.services.plc_device_service import get_plc_device_data

router = APIRouter(
    prefix="/plc",
    tags=["PLC Device Data"]
)

@router.get("/data", summary="取得 PLC Device 資料", description="從 Supabase 撈取 PLC Device 前 N 筆資料")
async def fetch_plc_data(limit: int = 10):
    try:
        result = get_plc_device_data(limit)

        if isinstance(result, dict) and result.get("status") != "success":
            raise HTTPException(status_code=500, detail="Supabase 查詢失敗")

        return result.get("data") if isinstance(result, dict) else result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
