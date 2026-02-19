from datetime import datetime

from shiftledger_shared.models import Supply, SupplyItem
from sqlalchemy import select

from src.crud import get_or_404
from src.database import read_only_session, write_session
from src.schemas import SupplyCreate, SupplyRead


def create_supply(supply_in: SupplyCreate) -> SupplyRead:
    with write_session() as session:
        supply_date = supply_in.supply_date or datetime.now()

        db_supply = Supply(
            supply_date=supply_date,
            supplier_name=supply_in.supplier_name,
            note=supply_in.note,
        )
        session.add(db_supply)

        for item in supply_in.items:
            db_item = SupplyItem(
                supply=db_supply,
                product_id=item.product_id,
                quantity=item.quantity,
                price_per_unit=item.price_per_unit,
            )
            session.add(db_item)

        session.refresh(db_supply)
        return SupplyRead.model_validate(db_supply)


def get_supply(supply_id: int) -> SupplyRead:
    with read_only_session() as session:
        db_obj = get_or_404(session, Supply, supply_id)
        return SupplyRead.model_validate(db_obj)


def get_supplies(skip: int = 0, limit: int = 100) -> list[SupplyRead]:
    with read_only_session() as session:
        result = session.execute(select(Supply).offset(skip).limit(limit))
        return [
            SupplyRead.model_validate(obj) for obj in result.scalars().all()
        ]
