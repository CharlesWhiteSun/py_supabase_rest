from fastapi import APIRouter
from typing import Sequence
from py_supabase_rest.app.services.interface import IDataHandleService
from py_supabase_rest.app.services.dto import ServiceResult

def register_service_routes(router: APIRouter, services: Sequence[IDataHandleService]):
    """
    自動將多個 IDataHandleService 註冊到 API Router
    """
    for service in services:
        async def handler(data: dict, svc=service):  # 預設參數避免 late binding 問題
            result: ServiceResult = svc.Process(data)
            return {
                "success": result.success,
                "message": result.message,
                "data": result.data.dict() if (result.success and result.data) else None
            }

        router.add_api_route(
            service.route,
            handler,
            methods=[service.method],
            name=service.__class__.__name__
        )
