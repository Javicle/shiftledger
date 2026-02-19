from fastapi import APIRouter
from src.crud.reports import (
    create_shift_report,
    get_shift_report,
    get_shift_reports,
    get_today_report,
)
from src.schemas import ShiftReportCreate, ShiftReportRead

router = APIRouter(prefix='/reports', tags=['Отчёты за смену'])


@router.post('/', response_model=ShiftReportRead, status_code=201)
def create_new_report(
    report: ShiftReportCreate,
):
    return create_shift_report(report)


@router.get('/today', response_model=ShiftReportRead)
def read_today_report():
    return get_today_report()


@router.get('/{report_id}', response_model=ShiftReportRead)
def read_report(
    report_id: int,
):
    return get_shift_report(report_id)


@router.get('/', response_model=list[ShiftReportRead])
def read_reports(
    skip: int = 0,
    limit: int = 100,
):
    return get_shift_reports(skip=skip, limit=limit)
