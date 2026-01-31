# api/v1/supplies.py
from api.deps import get_db_session_dep
from crud.supplies import create_supply, get_supplies, get_supply
from fastapi import APIRouter
from schemas import SupplyCreate, SupplyRead

router = APIRouter(prefix='/supplies', tags=['Поставки'])


@router.post('/', response_model=SupplyRead, status_code=201)
def create_new_supply(supply: SupplyCreate, db: get_db_session_dep):
    return create_supply(db, supply)


@router.get('/{supply_id}', response_model=SupplyRead)
def read_supply(supply_id: int, db: get_db_session_dep):
    return get_supply(db, supply_id)


@router.get('/', response_model=list[SupplyRead])
def read_supplies(
    db: get_db_session_dep,
    skip: int = 0,
    limit: int = 100,
):
    return get_supplies(db, skip=skip, limit=limit)
