import uvicorn
from api.deps import get_db_session_dep
from api.v1 import categories, products, reports, supplies
from crud.debts import get_total_debt_breakdown
from crud.reports import get_shift_reports, get_today_report
from database import create_tables
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# application
app = FastAPI(title='Бухалтерия')
# templates
templates = Jinja2Templates(directory='accounting-core/templates')
# static files
app.mount(
    '/static', StaticFiles(directory='accounting-core/static'), name='static'
)
# create database tables
create_tables()

# include routers
app.include_router(reports.router, prefix='/api/v1')
app.include_router(supplies.router, prefix='/api/v1')
app.include_router(products.router, prefix='/api/v1')
app.include_router(categories.router, prefix='/api/v1')


# route to view main page
@app.get('/', include_in_schema=False)
async def home(request: Request, db: get_db_session_dep):
    debt_info = get_total_debt_breakdown(db)

    today_report = None
    try:
        today_report = get_today_report(db)
    except HTTPException:
        today_report = None

    return templates.TemplateResponse(
        'index.html',
        {
            'request': request,
            'debt_info': debt_info,
            'today_report': today_report,
        },
    )


@app.get('/reports/new', include_in_schema=False)
async def reports_new(request: Request):
    return templates.TemplateResponse('reports_new.html', {'request': request})


@app.get('/reports', include_in_schema=False)
async def reports_list(request: Request, db: get_db_session_dep):
    reports = get_shift_reports(db, limit=50)
    return templates.TemplateResponse(
        'reports_list.html', {'request': request, 'reports': reports}
    )


@app.get('/supplies/new', include_in_schema=False)
async def supplies_new(request: Request):
    return templates.TemplateResponse(
        'supplies_new.html', {'request': request}
    )


@app.get('/supplies', include_in_schema=False)
async def supplies_list(request: Request):
    return templates.TemplateResponse(
        'supplies_list.html', {'request': request}
    )


@app.get('/debt', include_in_schema=False)
async def debt_page(request: Request, db: get_db_session_dep):
    debt_info = get_total_debt_breakdown(db)
    return templates.TemplateResponse(
        'debt.html', {'request': request, 'debt_info': debt_info}
    )


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
