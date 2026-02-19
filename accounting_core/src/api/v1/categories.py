# api/v1/categories.py
from fastapi import APIRouter
from src.crud.categories import (
    create_category,
    delete_category,
    get_categories,
    get_category,
    update_category,
)
from src.schemas import ProductCategoryCreate, ProductCategoryRead

router = APIRouter(prefix='/categories', tags=['Категории'])


@router.post('/', response_model=ProductCategoryRead, status_code=201)
def create(
    cat: ProductCategoryCreate,
):
    return create_category(cat)


@router.get('/{id}', response_model=ProductCategoryRead)
def read(
    id: int,
):
    return get_category(id)


@router.get('/', response_model=list[ProductCategoryRead])
def list(
    skip: int = 0,
    limit: int = 100,
):
    return get_categories(skip, limit)


@router.put('/{id}', response_model=ProductCategoryRead)
def update(
    id: int,
    cat: ProductCategoryCreate,
):
    return update_category(id, cat)


@router.delete('/{id}')
def delete(
    id: int,
):
    delete_category(id)
    return {'ok': True}
