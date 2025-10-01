from typing import Generic, TypeVar, Optional

T = TypeVar("T")

class ServiceResult(Generic[T]):
    def __init__(self, success: bool, message: str = "", data: Optional[T] = None):
        self.success = success
        self.message = message
        self.data = data

    @classmethod
    def ok(cls, data: Optional[T] = None, message: str = "Success"):
        return cls(success=True, message=message, data=data)

    @classmethod
    def fail(cls, message: str = "Error", data: Optional[T] = None):
        return cls(success=False, message=message, data=data)

    def __repr__(self) -> str:
        return f"ServiceResult(success={self.success}, message='{self.message}', data={self.data})"
