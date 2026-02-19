from datetime import date as dt_date

from fastapi import HTTPException
from shiftledger_shared.models import SaleItem, ShiftReport
from sqlalchemy import select

from src.crud import get_or_404
from src.database import read_only_session, write_session
from src.schemas import ShiftReportCreate, ShiftReportRead


def create_shift_report(report_in: ShiftReportCreate) -> ShiftReportRead:
    with write_session() as session:
        report_date = report_in.report_date or dt_date.today()

        db_report = ShiftReport(
            report_date=report_date,
            start_time=report_in.start_time,
            end_time=report_in.end_time,
            is_night=report_in.is_night,
            debt_payment_made=report_in.debt_payment_made,
        )
        session.add(db_report)
        # Не нужен flush() — SQLAlchemy сам обработает при коммите

        total_revenue = 0.0
        for sale in report_in.sales_items:
            revenue = sale.quantity_sold * sale.price_sold_at
            total_revenue += revenue
            db_sale = SaleItem(
                report=db_report,  # ← через отношение, не report_id
                product_id=sale.product_id,
                quantity_sold=sale.quantity_sold,
                price_sold_at=sale.price_sold_at,
            )
            session.add(db_sale)

        db_report.total_revenue = total_revenue
        session.refresh(db_report)
        return ShiftReportRead.model_validate(db_report)


def get_shift_report(report_id: int) -> ShiftReportRead:
    with read_only_session() as session:
        db_obj = get_or_404(session, ShiftReport, report_id)
        return ShiftReportRead.model_validate(db_obj)


def get_shift_reports(
    skip: int = 0, limit: int = 100
) -> list[ShiftReportRead]:
    with read_only_session() as session:
        result = session.execute(select(ShiftReport).offset(skip).limit(limit))
        return [
            ShiftReportRead.model_validate(obj)
            for obj in result.scalars().all()
        ]


def get_today_report() -> ShiftReportRead:
    with read_only_session() as session:
        today = dt_date.today()
        db_obj = session.scalar(
            select(ShiftReport).where(ShiftReport.report_date == today)
        )
        if not db_obj:
            raise HTTPException(
                status_code=404, detail='Отчёт за сегодня не найден'
            )
        return ShiftReportRead.model_validate(db_obj)
