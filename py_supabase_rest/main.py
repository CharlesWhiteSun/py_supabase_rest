from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from py_supabase_rest.app.routers import plc_chart_router
from py_supabase_rest.app.routers import register

# 掛載 router
app = FastAPI(title="Python Supabase REST API")
app.include_router(plc_chart_router.router)
app.include_router(register.router)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")
