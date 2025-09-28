from fastapi import APIRouter
from app.models import PLCData
from app.crud import *

router = APIRouter(prefix="/plc", tags=["PLC Data"])

@router.get("/")
def get_data():
    return read_plc_data()

@router.post("/")
def post_data(data: PLCData):
    return create_plc_data(data)
