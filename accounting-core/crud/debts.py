from schemas import DebtPaymentCreate, DebtRecordCreate
from shiftledger_shared.models import (
    DebtPayment,
    DebtRecord,
    ShiftReport,
    SupplyItem,
)
from sqlalchemy import func, select
from sqlalchemy.orm import Session


def create_debt_record(db: Session, debt_in: DebtRecordCreate) -> DebtRecord:
    db_obj = DebtRecord(**debt_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def create_debt_payment(
    db: Session, payment_in: DebtPaymentCreate
) -> DebtPayment:
    db_obj = DebtPayment(**payment_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_debt_records(db: Session, skip: int = 0, limit: int = 100):
    return db.scalars(select(DebtRecord).offset(skip).limit(limit)).all()


def get_total_debt(db: Session) -> float:
    total_incurred = db.scalar(
        select(func.coalesce(func.sum(DebtRecord.amount), 0.0))
    )
    total_paid = db.scalar(
        select(func.coalesce(func.sum(DebtPayment.amount), 0.0))
    )
    return float(
        total_incurred - total_paid if total_incurred and total_paid else 0
    )


def get_total_debt_breakdown(db) -> dict:
    # Месяцы с отчётами
    months_subq = select(
        func.distinct(func.date_trunc('month', ShiftReport.report_date))
    ).subquery()
    months_count = (
        db.scalar(select(func.count()).select_from(months_subq)) or 0
    )
    base_debt = 100_000.0 * float(months_count)

    supply_debt_deciminal = (
        db.scalar(
            select(
                func.coalesce(
                    func.sum(SupplyItem.quantity * SupplyItem.price_per_unit),
                    0.0,
                )
            )
        )
        or 0.0
    )
    supply_debt = float(supply_debt_deciminal)
    # Выплачено
    total_paid = float(
        db.scalar(
            select(func.coalesce(func.sum(ShiftReport.debt_payment_made), 0.0))
        )
        or 0.0
    )

    total_debt = base_debt + supply_debt - total_paid

    return {
        'total_debt': max(float(total_debt), 0.0),
        'base_debt': float(base_debt),
        'supply_debt': float(supply_debt),
        'total_paid': float(total_paid),
    }
