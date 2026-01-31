from shiftledger_shared.config import settings
from shiftledger_shared.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    url=settings.DATABASE_URL,
)

session = sessionmaker(engine)


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


def drop_tables() -> None:
    Base.metadata.drop_all(bind=engine)
