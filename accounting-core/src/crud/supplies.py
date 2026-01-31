from datetime import datetime

from crud import get_or_404
from schemas import SupplyCreate
from shiftledger_shared.models import Supply, SupplyItem
from sqlalchemy import select
from sqlalchemy.orm import Session


def create_supply(db: Session, supply_in: SupplyCreate) -> Supply:
    supply_data = supply_in.model_dump(exclude={'items'})
    if supply_data.get('supply_date') is None:
        supply_data['supply_date'] = datetime.now()
    db_supply = Supply(**supply_data)
    db.add(db_supply)
    db.flush()  # чтобы получить id

    total_debt_increase = 0.0
    for item in supply_in.items:
        db_item = SupplyItem(
            supply_id=db_supply.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_per_unit=item.price_per_unit,
        )
        db.add(db_item)
        total_debt_increase += item.quantity * item.price_per_unit

    db.commit()
    db.refresh(db_supply)
    return db_supply


def get_supply(db: Session, supply_id: int) -> Supply:
    return get_or_404(db, Supply, supply_id)


def get_supplies(db: Session, skip: int = 0, limit: int = 100):
    return db.scalars(select(Supply).offset(skip).limit(limit)).all()
