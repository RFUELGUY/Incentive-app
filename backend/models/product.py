from sqlalchemy import Column, String, Float
from backend.db.database import Base

class Product(Base):
    __tablename__ = "products"
    
    barcode = Column(String, primary_key=True, index=True)
    verticle = Column(String)
    trait = Column(String)  # old / new / specialxyz
    rsp = Column(Float)     # retail selling price
