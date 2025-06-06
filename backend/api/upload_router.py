from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.database import SessionLocal
from backend.utils.security import get_current_user_role

import pandas as pd
from io import BytesIO
from backend.models.actual_sale import ActualSale
from backend.models.product import Product

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/sales-file")
async def upload_sales_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin=Depends(get_current_user_role("admin"))
):
    """
    Admin: Upload Excel file with actual sales.
    Avoids exact duplicates. Summarizes skipped rows.
    """
    try:
        contents = await file.read()
        df = pd.read_excel(BytesIO(contents))

        required_columns = {"date", "customer", "barcode", "qty", "net amount"}
        if not required_columns.issubset(df.columns):
            raise HTTPException(status_code=400, detail="Invalid file format: missing required columns.")

        inserted = 0
        skipped = 0
        skipped_dates = set()

        for _, row in df.iterrows():
            sale_data = {
                "date": pd.to_datetime(row["date"]),
                "customer": str(row["customer"]),
                "barcode": str(row["barcode"]),
                "qty": int(row["qty"]),
                "net_amount": float(row["net amount"])
            }

            exists = db.query(ActualSale).filter_by(**sale_data).first()
            if exists:
                skipped += 1
                skipped_dates.add(sale_data["date"].strftime("%Y-%m-%d"))
                continue

            db.add(ActualSale(**sale_data))
            inserted += 1

        db.commit()

        return {
            "message": "Sales file processed.",
            "inserted": inserted,
            "skipped": skipped,
            "skipped_dates": sorted(list(skipped_dates))
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Upload failed: {e}")


@router.post("/base-file")
async def upload_base_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin=Depends(get_current_user_role("admin"))
):
    """
    Admin: Upload Excel file containing base product data.
    Uses db.merge() to upsert based on barcode.
    """
    try:
        contents = await file.read()
        df = pd.read_excel(BytesIO(contents))

        required_columns = {"barcode", "verticle", "trait", "rsp"}
        if not required_columns.issubset(df.columns):
            raise HTTPException(status_code=400, detail="Invalid file format: missing required columns.")

        for _, row in df.iterrows():
            product = Product(
                barcode=str(row['barcode']),
                verticle=str(row['verticle']),
                trait=str(row['trait']),
                rsp=float(row['rsp']),
            )
            db.merge(product)

        db.commit()
        return {"message": "Base file uploaded and stored successfully."}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Upload failed: {e}")
