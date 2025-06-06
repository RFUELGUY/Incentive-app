# incentive-app/backend/api/product_router.py

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from tempfile import NamedTemporaryFile
import shutil

from backend.db.database import SessionLocal
from backend.schemas.product_schema import ProductSubmit
from backend.crud.product_crud import upsert_product, upsert_products_from_file
from backend.utils.security import get_current_user_role

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload-product-file")
def upload_product_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin=Depends(get_current_user_role("admin"))
):
    """
    Admin: Upload an Excel/CSV file to bulk insert/update products.
    """
    if not file.filename.endswith((".xlsx", ".csv")):
        raise HTTPException(status_code=400, detail="Only .xlsx or .csv files are supported")

    try:
        with NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
        result = upsert_products_from_file(db, tmp_path)
        return {"message": "File processed", "details": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add-product")
def add_product(
    payload: ProductSubmit,
    db: Session = Depends(get_db),
    admin=Depends(get_current_user_role("admin"))
):
    """
    Admin: Add or update a single product manually.
    """
    try:
        upsert_product(db, payload)
        return {"message": "Product saved", "barcode": payload.barcode}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save product: {str(e)}")
