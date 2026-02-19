from shiftledger_shared.models import Product
from sqlalchemy import select

from src.crud import get_or_404
from src.database import read_only_session, write_session
from src.schemas import ProductCreate, ProductRead


def create_product(product_in: ProductCreate) -> ProductRead:
    with write_session() as session:
        db_obj = Product(
            name=product_in.name,
            category_id=product_in.category_id,
            default_price=product_in.default_price,
        )
        session.add(db_obj)
        session.refresh(db_obj)
        return ProductRead.model_validate(db_obj)


def get_product(product_id: int) -> ProductRead:
    with read_only_session() as session:
        db_obj = get_or_404(session, Product, product_id)
        return ProductRead.model_validate(db_obj)


def get_products(skip: int = 0, limit: int = 100) -> list[ProductRead]:
    with read_only_session() as session:
        result = session.execute(select(Product).offset(skip).limit(limit))
        return [
            ProductRead.model_validate(obj) for obj in result.scalars().all()
        ]


def update_product(product_id: int, product_in: ProductCreate) -> ProductRead:
    with write_session() as session:
        db_obj = get_or_404(session, Product, product_id)
        db_obj.name = product_in.name
        db_obj.category_id = product_in.category_id
        db_obj.default_price = product_in.default_price
        session.refresh(db_obj)
        return ProductRead.model_validate(db_obj)
