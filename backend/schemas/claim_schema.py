from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ClaimRequest(BaseModel):
    remarks: Optional[str] = None

class ClaimOut(BaseModel):
    id: int
    salesman_id: int
    total_amount: float
    is_approved: bool
    remarks: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True

class ClaimOut(BaseModel):
    id: int
    salesman_id: int
    total_amount: float
    is_approved: bool
    remarks: Optional[str]
    timestamp: datetime

    # Extras for frontend
    salesman_name: Optional[str] = "Salesman"
    reason: Optional[str] = None

    class Config:
        orm_mode = True


class ClaimUpdateRequest(BaseModel):
    new_remarks: str