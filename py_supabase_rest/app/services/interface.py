from typing import Protocol, Any
from py_supabase_rest.app.services.dto import ServiceResult

class IDataHandleService(Protocol):
    """資料處理介面"""
    
    route: str
    method: str
    
    def Process(self, data: Any) -> ServiceResult:
        ...
