from pydantic import BaseModel

class SignupRequest(BaseModel):
    name: str
    phone: str
    password: str
    role: str  # "admin" or "salesman"
