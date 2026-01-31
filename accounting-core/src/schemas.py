# app/schemas.py
from datetime import date, datetime

from pydantic import BaseModel, Field

# ========================
# Категории и продукты
# ========================


class ProductCategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: str | None = None


class ProductCategoryRead(BaseModel):
    id: int
    name: str
    description: str | None

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    category_id: int
    default_price: float = Field(gt=0)


class ProductRead(BaseModel):
    id: int
    name: str
    category_id: int
    default_price: float

    class Config:
        from_attributes = True


# ========================
# Поставки (Supply)
# ========================


class SupplyItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    price_per_unit: float = Field(gt=0)


class SupplyItemRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    price_per_unit: float
    total_cost: float  # вычисляется в модели

    class Config:
        from_attributes = True


class SupplyCreate(BaseModel):
    supply_date: datetime | None = None  # если не указано — сейчас
    supplier_name: str = 'Начальник'
    note: str | None = None
    items: list[SupplyItemCreate]  # вложенные позиции


class SupplyRead(BaseModel):
    id: int
    supply_date: datetime
    supplier_name: str
    note: str | None
    items: list[SupplyItemRead]

    class Config:
        from_attributes = True


# ========================
# Продажи / Отчёты за смену (ShiftReport)
# ========================


class SaleItemCreate(BaseModel):
    product_id: int
    quantity_sold: int = Field(gt=0)
    price_sold_at: float = Field(gt=0)


class SaleItemRead(BaseModel):
    id: int
    product_id: int
    quantity_sold: int
    price_sold_at: float
    revenue: float  # вычисляется

    class Config:
        from_attributes = True


class ShiftReportCreate(BaseModel):
    report_date: date | None = None  # по умолчанию — сегодня
    start_time: datetime
    end_time: datetime
    is_night: bool = False
    debt_payment_made: float = Field(ge=0, default=0.0)
    sales_items: list[SaleItemCreate]


class ShiftReportRead(BaseModel):
    id: int
    report_date: date
    start_time: datetime
    end_time: datetime
    is_night: bool
    total_revenue: float
    debt_payment_made: float
    net_income: float
    sales_items: list[SaleItemRead]

    class Config:
        from_attributes = True


# ========================
# Долги (Debt)
# ========================


class DebtRecordCreate(BaseModel):
    description: str = Field(..., min_length=1, max_length=200)
    amount: float = Field(gt=0)
    is_supply_related: bool = False
    supply_id: int | None = None


class DebtRecordRead(BaseModel):
    id: int
    description: str
    amount: float
    created_at: datetime
    is_supply_related: bool
    supply_id: int | None

    class Config:
        from_attributes = True


class DebtPaymentCreate(BaseModel):
    amount: float = Field(gt=0)
    shift_report_id: int | None = None


class DebtPaymentRead(BaseModel):
    id: int
    amount: float
    paid_at: datetime
    shift_report_id: int | None

    class Config:
        from_attributes = True
