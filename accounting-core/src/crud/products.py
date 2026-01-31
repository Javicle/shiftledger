# crud/products.py
from crud import get_or_404
from schemas import ProductCreate
from shiftledger_shared.models import Product
from sqlalchemy import select
from sqlalchemy.orm import Session


def create_product(db: Session, product_in: ProductCreate) -> Product:
    db_obj = Product(**product_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_product(db: Session, product_id: int) -> Product:
    return get_or_404(db, Product, product_id)


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.scalars(select(Product).offset(skip).limit(limit)).all()


def update_product(
    db: Session, product_id: int, product_in: ProductCreate
) -> Product:
    db_obj = get_or_404(db, Product, product_id)
    for key, value in product_in.model_dump().items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj
