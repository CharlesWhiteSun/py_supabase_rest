import asyncio
from datetime import datetime, timedelta, timezone
from py_supabase_rest.app.dao.models import PLCData
from py_supabase_rest.app.services.interface import IDataHandleService
from py_supabase_rest.app.services.dto import ServiceResult
from py_supabase_rest.app.config import supabase

class PLCDataHandleService(IDataHandleService):
    """處理 PLC 資料的實作"""
    
    route = "/plc"
    method = "POST"

    def Process(self, data: dict) -> ServiceResult:
        try:
            ts = datetime.strptime(data["timestamp"], "%Y-%m-%dT%H:%M:%S%z")
            ts = ts.astimezone(timezone(timedelta(hours=8)))

            plc_data = PLCData(
                device_id=data["device_id"],
                voltage=float(data["voltage"]),
                current=float(data["current"]),
                timestamp=ts.isoformat(),
                date=ts.strftime("%Y-%m-%d"),
                hh=ts.strftime("%H"),
                mm=ts.strftime("%M"),
                ss=ts.strftime("%S"),
            )
            asyncio.create_task(self._async_insert(plc_data))

            return ServiceResult.ok(plc_data, "PLCData parsed successfully")
        except Exception as e:
            return ServiceResult.fail(f"Failed to parse PLC data: {e}")

    async def _async_insert(self, plc_data: PLCData):
        try:
            record = plc_data.model_dump()
            await asyncio.to_thread(self._sync_insert, record)
        except Exception as e:
            print(f"❌ Supabase insert failed: {e}")

    def _sync_insert(self, record: dict):
        try:
            supabase.table("plc_device").insert(record).execute()
            print(f"✅ 已成功插入 Supabase: {record}")
        except Exception as e:
            print(f"❌ Supabase insert error: {e}")
