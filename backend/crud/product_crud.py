import pandas as pd
from sqlalchemy.orm import Session
from models.product import Product
from schemas.product_schema import ProductSubmit


def upsert_product(db: Session, payload: ProductSubmit) -> Product:
    """
    Insert or update a single product row.
    Returns the upserted product instance.
    """
    existing = db.query(Product).filter_by(barcode=payload.barcode).first()

    try:
        if existing:
            existing.verticle = payload.verticle
            existing.trait = payload.trait
            existing.rsp = payload.rsp
        else:
            new = Product(
                barcode=payload.barcode,
                verticle=payload.verticle,
                trait=payload.trait,
                rsp=payload.rsp
            )
            db.add(new)

        db.commit()
        return existing or new

    except Exception as e:
        db.rollback()
        raise e


def upsert_products_from_file(db: Session, file_path: str) -> dict:
    """
    Insert or update multiple products from an Excel or CSV file.
    File must contain: barcode, verticle, trait, rsp
    Returns count of processed products.
    """
    try:
        if file_path.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file_path)
        elif file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        else:
            raise ValueError("Unsupported file format. Use .xlsx or .csv")

        required_columns = {"barcode", "verticle", "trait", "rsp"}
        if not required_columns.issubset(set(df.columns)):
            raise ValueError(f"Missing required columns: {required_columns - set(df.columns)}")

        upserted_count = 0

        for _, row in df.iterrows():
            barcode = str(row.get("barcode")).strip()
            if not barcode or pd.isna(barcode):
                continue

            existing = db.query(Product).filter_by(barcode=barcode).first()
            rsp = float(row["rsp"]) if not pd.isna(row["rsp"]) else 0.0

            if existing:
                existing.verticle = str(row["verticle"]).strip()
                existing.trait = str(row["trait"]).strip()
                existing.rsp = rsp
            else:
                product = Product(
                    barcode=barcode,
                    verticle=str(row["verticle"]).strip(),
                    trait=str(row["trait"]).strip(),
                    rsp=rsp
                )
                db.add(product)

            upserted_count += 1

        db.commit()

    except Exception as e:
        db.rollback()
        raise e

    return {"upserted": upserted_count}
