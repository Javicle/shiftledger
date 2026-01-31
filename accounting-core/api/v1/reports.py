from api.deps import get_db_session_dep
from crud.reports import (
    create_shift_report,
    get_shift_report,
    get_shift_reports,
    get_today_report,
)
from fastapi import APIRouter
from schemas import ShiftReportCreate, ShiftReportRead

router = APIRouter(prefix='/reports', tags=['Отчёты за смену'])


@router.post('/', response_model=ShiftReportRead, status_code=201)
def create_new_report(report: ShiftReportCreate, db: get_db_session_dep):
    return create_shift_report(db, report)


@router.get('/today', response_model=ShiftReportRead)
def read_today_report(db: get_db_session_dep):
    return get_today_report(db)


@router.get('/{report_id}', response_model=ShiftReportRead)
def read_report(report_id: int, db: get_db_session_dep):
    return get_shift_report(db, report_id)


@router.get('/', response_model=list[ShiftReportRead])
def read_reports(
    db: get_db_session_dep,
    skip: int = 0,
    limit: int = 100,
):
    return get_shift_reports(db, skip=skip, limit=limit)
