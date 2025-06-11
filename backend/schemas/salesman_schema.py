from pydantic import BaseModel

class SalesmanCreate(BaseModel):
    name: str
    mobile: str
    outlet: str
    password: str

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
    category: str | None = None
    wallet_balance: int  # <- Add this

    class Config:
        orm_mode = True
