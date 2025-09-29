from fastapi import FastAPI
from py_supabase_rest.app.routers import router

app = FastAPI(title="PLC Power Cloud API")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Welcome to py_supabase_rest API"}
