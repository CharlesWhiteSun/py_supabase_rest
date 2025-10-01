from fastapi import APIRouter
from py_supabase_rest.app.services.plc_handler_service import PLCDataHandleService
from py_supabase_rest.app.routers.register import register_service_routes

router = APIRouter()

services = [
    PLCDataHandleService(),
]

# 自動註冊
register_service_routes(router, services)
