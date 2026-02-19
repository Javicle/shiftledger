# app/schemas.py
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

# ========================
# Категории и продукты
# ========================


class Model(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ProductCategoryCreate(Model):
    name: str = Field(..., min_length=1, max_length=50)
    description: str | None = None


class ProductCategoryRead(Model):
    id: int
    name: str
    description: str | None


class ProductCreate(Model):
    name: str = Field(..., min_length=1, max_length=100)
    category_id: int
    default_price: float = Field(gt=0)


class ProductRead(Model):
    id: int
    name: str
    category_id: int
    default_price: float


# ========================
# Поставки (Supply)
# ========================


class SupplyItemCreate(Model):
    product_id: int
    quantity: int = Field(gt=0)
    price_per_unit: float = Field(gt=0)


class SupplyItemRead(Model):
    id: int
    product_id: int
    quantity: int
    price_per_unit: float
    total_cost: float  # вычисляется в модели


class SupplyCreate(Model):
    supply_date: datetime | None = None
    supplier_name: str = 'Начальник'
    note: str | None = None
    items: list[SupplyItemCreate]  # вложенные позиции


class SupplyRead(Model):
    id: int
    supply_date: datetime
    supplier_name: str
    note: str | None
    items: list[SupplyItemRead]


# ========================
# Продажи / Отчёты за смену (ShiftReport)
# ========================


class SaleItemCreate(Model):
    product_id: int
    quantity_sold: int = Field(gt=0)
    price_sold_at: float = Field(gt=0)


class SaleItemRead(Model):
    id: int
    product_id: int
    quantity_sold: int
    price_sold_at: float
    revenue: float  # вычисляется


class ShiftReportCreate(Model):
    report_date: date | None = None  # по умолчанию — сегодня
    start_time: datetime
    end_time: datetime
    is_night: bool = False
    debt_payment_made: float = Field(ge=0, default=0.0)
    sales_items: list[SaleItemCreate]


class ShiftReportRead(Model):
    id: int
    report_date: date
    start_time: datetime
    end_time: datetime
    is_night: bool
    total_revenue: float
    debt_payment_made: float
    net_income: float
    sales_items: list[SaleItemRead]


# ========================
# Долги (Debt)
# ========================


class DebtRecordCreate(Model):
    description: str = Field(..., min_length=1, max_length=200)
    amount: float = Field(gt=0)
    is_supply_related: bool = False
    supply_id: int | None = None


class DebtRecordRead(Model):
    id: int
    description: str
    amount: float
    created_at: datetime
    is_supply_related: bool
    supply_id: int | None


class DebtPaymentCreate(Model):
    amount: float = Field(gt=0)
    shift_report_id: int | None = None


class DebtPaymentRead(Model):
    id: int
    amount: float
    paid_at: datetime
    shift_report_id: int | None
