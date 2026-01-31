# api/v1/products.py
from api.deps import get_db_session_dep
from crud.products import (
    create_product,
    get_product,
    get_products,
    update_product,
)
from fastapi import APIRouter
from schemas import ProductCreate, ProductRead

router = APIRouter(prefix='/products', tags=['Продукты'])


@router.post('/', response_model=ProductRead, status_code=201)
def create(prod: ProductCreate, db: get_db_session_dep):
    return create_product(db, prod)


@router.get('/{id}', response_model=ProductRead)
def read(id: int, db: get_db_session_dep):
    return get_product(db, id)


@router.get('/', response_model=list[ProductRead])
def list(
    db: get_db_session_dep,
    skip: int = 0,
    limit: int = 100,
):
    return get_products(db, skip, limit)


@router.put('/{id}', response_model=ProductRead)
def update(id: int, prod: ProductCreate, db: get_db_session_dep):
    return update_product(db, id, prod)
