from crud import get_or_404
from schemas import ProductCategoryCreate
from shiftledger_shared.models import ProductCategory
from sqlalchemy import select
from sqlalchemy.orm import Session


def create_category(
    db: Session, category_in: ProductCategoryCreate
) -> ProductCategory:
    db_obj = ProductCategory(**category_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_category(db: Session, category_id: int) -> ProductCategory:
    return get_or_404(db, ProductCategory, category_id)


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.scalars(select(ProductCategory).offset(skip).limit(limit)).all()


def update_category(
    db: Session, category_id: int, category_in: ProductCategoryCreate
) -> ProductCategory:
    db_obj = get_or_404(db, ProductCategory, category_id)
    for key, value in category_in.model_dump().items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_category(db: Session, category_id: int) -> bool:
    db_obj = get_or_404(db, ProductCategory, category_id)
    db.delete(db_obj)
    db.commit()
    return True
