# api/v1/categories.py
from api.deps import get_db_session_dep
from crud.categories import (
    create_category,
    delete_category,
    get_categories,
    get_category,
    update_category,
)
from fastapi import APIRouter
from schemas import ProductCategoryCreate, ProductCategoryRead

router = APIRouter(prefix='/categories', tags=['Категории'])


@router.post('/', response_model=ProductCategoryRead, status_code=201)
def create(cat: ProductCategoryCreate, db: get_db_session_dep):
    return create_category(db, cat)


@router.get('/{id}', response_model=ProductCategoryRead)
def read(id: int, db: get_db_session_dep):
    return get_category(db, id)


@router.get('/', response_model=list[ProductCategoryRead])
def list(
    db: get_db_session_dep,
    skip: int = 0,
    limit: int = 100,
):
    return get_categories(db, skip, limit)


@router.put('/{id}', response_model=ProductCategoryRead)
def update(id: int, cat: ProductCategoryCreate, db: get_db_session_dep):
    return update_category(db, id, cat)


@router.delete('/{id}')
def delete(id: int, db: get_db_session_dep):
    delete_category(db, id)
    return {'ok': True}
