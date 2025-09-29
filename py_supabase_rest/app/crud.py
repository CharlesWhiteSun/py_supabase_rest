from py_supabase_rest.app.models import PLCData
from py_supabase_rest.app.db import get_all_data, insert_data

def read_plc_data():
    return get_all_data()

def create_plc_data(data: PLCData):
    return insert_data(data)
