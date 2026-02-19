# api/v1/supplies.py
from fastapi import APIRouter
from src.crud.supplies import create_supply, get_supplies, get_supply
from src.schemas import SupplyCreate, SupplyRead

router = APIRouter(prefix='/supplies', tags=['Поставки'])


@router.post('/', response_model=SupplyRead, status_code=201)
def create_new_supply(supply: SupplyCreate):
    return create_supply(supply)


@router.get('/{supply_id}', response_model=SupplyRead)
def read_supply(supply_id: int):
    return get_supply(supply_id)


@router.get('/', response_model=list[SupplyRead])
def read_supplies(
    skip: int = 0,
    limit: int = 100,
):
    return get_supplies(skip=skip, limit=limit)
