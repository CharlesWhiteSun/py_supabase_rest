from app.config import supabase
from app.models import PLCData

TABLE_NAME = "plc_device"

def get_all_data():
    response = supabase.table(TABLE_NAME).select("*").execute()
    return response.data

def insert_data(data: PLCData):
    record = data.model_dump()
    response = supabase.table(TABLE_NAME).insert(record).execute()
    return response.data
