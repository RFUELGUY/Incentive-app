from pydantic import BaseModel

class SalesmanCreate(BaseModel):
    name: str
    mobile: str
    outlet: str

class SalesmanApprove(BaseModel):
    mobile: str
    category: str
    password: str

class SalesmanLogin(BaseModel):  # ⬅️ Add this
    mobile: str
    password: str

class SalesmanOut(BaseModel):
    id: int
    name: str
    mobile: str
    outlet: str
    is_approved: bool

    class Config:
        orm_mode = True  # works fine in Pydantic v1 or `from_attributes` in v2
