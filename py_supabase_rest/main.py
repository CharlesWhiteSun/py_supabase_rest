from fastapi import FastAPI
from py_supabase_rest.app.routers import plc_device_router, plc_chart_router

app = FastAPI(title="Python Supabase REST API")

# app.include_router(plc_device_router.router)
app.include_router(plc_chart_router.router)
