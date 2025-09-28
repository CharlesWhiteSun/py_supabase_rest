from pydantic import BaseModel

class PLCData(BaseModel):
    device_id: str
    voltage: float
    current: float
    timestamp: str