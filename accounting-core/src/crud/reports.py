# crud/reports.py
from datetime import date as dt_date

from crud import get_or_404
from fastapi import HTTPException
from schemas import ShiftReportCreate
from shiftledger_shared.models import SaleItem, ShiftReport
from sqlalchemy import select
from sqlalchemy.orm import Session


def create_shift_report(
    db: Session, report_in: ShiftReportCreate
) -> ShiftReport:
    report_data = report_in.model_dump(exclude={'sales_items'})
    if not report_data.get('report_date'):
        report_data['report_date'] = dt_date.today()

    db_report = ShiftReport(**report_data)
    db.add(db_report)
    db.flush()

    total_revenue = 0.0
    for sale in report_in.sales_items:
        revenue = sale.quantity_sold * sale.price_sold_at
        total_revenue += revenue
        db_sale = SaleItem(
            report_id=db_report.id,
            product_id=sale.product_id,
            quantity_sold=sale.quantity_sold,
            price_sold_at=sale.price_sold_at,
        )
        db.add(db_sale)

    db_report.total_revenue = total_revenue
    db.commit()
    db.refresh(db_report)
    return db_report


def get_shift_report(db: Session, report_id: int) -> ShiftReport:
    return get_or_404(db, ShiftReport, report_id)


def get_shift_reports(db: Session, skip: int = 0, limit: int = 100):
    return db.scalars(select(ShiftReport).offset(skip).limit(limit)).all()


def get_today_report(db: Session) -> ShiftReport:
    today = dt_date.today()
    report = db.scalar(
        select(ShiftReport).where(ShiftReport.report_date == today)
    )
    if not report:
        raise HTTPException(
            status_code=404, detail='Отчёт за сегодня не найден'
        )
    return report
