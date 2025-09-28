from app.models import PLCData
from app.db import get_all_data, insert_data

def read_plc_data():
    return get_all_data()

def create_plc_data(data: PLCData):
    return insert_data(data)
