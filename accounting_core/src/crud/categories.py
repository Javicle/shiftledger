from shiftledger_shared.models import ProductCategory
from sqlalchemy import select

from src.crud import get_or_404
from src.database import read_only_session, write_session
from src.schemas import ProductCategoryCreate, ProductCategoryRead


def create_category(category_in: ProductCategoryCreate) -> ProductCategoryRead:
    with write_session() as session:
        db_obj = ProductCategory(
            name=category_in.name,
            description=category_in.description,
        )
        session.add(db_obj)
        session.refresh(db_obj)
        return ProductCategoryRead.model_validate(db_obj)


def get_category(category_id: int) -> ProductCategoryRead:
    with read_only_session() as session:
        db_obj = get_or_404(session, ProductCategory, category_id)
        return ProductCategoryRead.model_validate(db_obj)


def get_categories(
    skip: int = 0, limit: int = 100
) -> list[ProductCategoryRead]:
    with read_only_session() as session:
        result = session.execute(
            select(ProductCategory).offset(skip).limit(limit)
        )
        return [
            ProductCategoryRead.model_validate(obj)
            for obj in result.scalars().all()
        ]


def update_category(
    category_id: int, category_in: ProductCategoryCreate
) -> ProductCategoryRead:
    with write_session() as session:
        db_obj = get_or_404(session, ProductCategory, category_id)
        db_obj.name = category_in.name
        db_obj.description = category_in.description
        session.refresh(db_obj)
        return ProductCategoryRead.model_validate(db_obj)


def delete_category(category_id: int) -> bool:
    with write_session() as session:
        db_obj = get_or_404(session, ProductCategory, category_id)
        session.delete(db_obj)
        return True
