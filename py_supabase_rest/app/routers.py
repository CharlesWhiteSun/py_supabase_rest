from fastapi import APIRouter
from py_supabase_rest.app.models import PLCData
from py_supabase_rest.app.crud import get_all_data, insert_data

router = APIRouter(prefix="/plc", tags=["PLC Data"])

@router.get("/")
def get_data():
    return {"status": "success", "data": get_all_data()}

@router.post("/")
def post_data(data: PLCData):
    return {"status": "success", "data": insert_data(data)}
