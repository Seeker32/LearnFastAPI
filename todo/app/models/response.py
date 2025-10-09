"""Standard API response models."""

from pydantic import Field
from sqlmodel import SQLModel

class ApiResponse[DataT](SQLModel):
    """Standard API response wrapper."""

    code: int = Field(..., description="Response code")
    msg: str = Field(..., description="Response message")
    data: DataT | None = Field(default=None, description="Response data")


def success_response(data=None, msg: str = "Success", code: int = 200) -> dict:
    """Helper function to create a success response."""
    return {"code": code, "msg": msg, "data": data}


def error_response(msg: str, code: int = 400, data=None) -> dict:
    """Helper function to create an error response."""
    return {"code": code, "msg": msg, "data": data}

