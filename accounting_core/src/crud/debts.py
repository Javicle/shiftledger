from shiftledger_shared.models import (
    DebtPayment,
    DebtRecord,
    ShiftReport,
    SupplyItem,
)
from sqlalchemy import func, select

from src.database import read_only_session, write_session
from src.schemas import DebtPaymentCreate, DebtRecordCreate


def create_debt_record(debt_in: DebtRecordCreate) -> DebtRecord:
    with write_session() as session:
        db_obj = DebtRecord(**debt_in.model_dump())
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj


def create_debt_payment(payment_in: DebtPaymentCreate) -> DebtPayment:
    with write_session() as session:
        db_obj = DebtPayment(**payment_in.model_dump())
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj


def get_debt_records(skip: int = 0, limit: int = 100):
    with read_only_session() as session:
        return session.scalars(
            select(DebtRecord).offset(skip).limit(limit)
        ).all()


def get_total_debt() -> float:
    with read_only_session() as session:
        total_incurred = session.scalar(
            select(func.coalesce(func.sum(DebtRecord.amount), 0.0))
        )
        total_paid = session.scalar(
            select(func.coalesce(func.sum(DebtPayment.amount), 0.0))
        )
        return float(
            total_incurred - total_paid if total_incurred and total_paid else 0
        )


def get_total_debt_breakdown() -> dict[str, float]:
    with read_only_session() as session:
        months_subq = select(
            func.distinct(func.date_trunc('month', ShiftReport.report_date))
        ).subquery()
        months_count = (
            session.scalar(select(func.count()).select_from(months_subq)) or 0
        )
        base_debt = 100_000.0 * float(months_count)

        supply_debt_deciminal = (
            session.scalar(
                select(
                    func.coalesce(
                        func.sum(
                            SupplyItem.quantity * SupplyItem.price_per_unit
                        ),
                        0.0,
                    )
                )
            )
            or 0.0
        )
        supply_debt = float(supply_debt_deciminal)
        # Выплачено
        total_paid = float(
            session.scalar(
                select(
                    func.coalesce(func.sum(ShiftReport.debt_payment_made), 0.0)
                )
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
