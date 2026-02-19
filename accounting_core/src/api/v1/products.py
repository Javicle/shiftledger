# api/v1/products.py
from fastapi import APIRouter
from src.crud.products import (
    create_product,
    get_product,
    get_products,
    update_product,
)
from src.schemas import ProductCreate, ProductRead

router = APIRouter(prefix='/products', tags=['Продукты'])


@router.post('/', response_model=ProductRead, status_code=201)
def create(
    prod: ProductCreate,
):
    return create_product(prod)


@router.get('/{id}', response_model=ProductRead)
def read(
    id: int,
):
    return get_product(id)


@router.get('/', response_model=list[ProductRead])
def list(
    skip: int = 0,
    limit: int = 100,
):
    return get_products(skip, limit)


@router.put('/{id}', response_model=ProductRead)
def update(
    id: int,
    prod: ProductCreate,
):
    return update_product(id, prod)
