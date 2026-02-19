from collections.abc import Generator
from contextlib import contextmanager
from typing import NoReturn

from shiftledger_shared.config import settings
from shiftledger_shared.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

engine = create_engine(
    url=settings.DATABASE_URL,
)

session = sessionmaker(engine)


@contextmanager
def read_only_session() -> Generator[Session]:
    def raise_for_read_only() -> NoReturn:
        raise ValueError('Read only session')

    session = Session()
    try:
        yield session

        session.commit = raise_for_read_only()
    finally:
        session.close()


@contextmanager
def write_session() -> Generator[Session]:
    session = Session()
    yield session
    try:
        session.commit()
    except Exception as exc:
        session.rollback()
        raise exc
    finally:
        session.close()


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


def drop_tables() -> None:
    Base.metadata.drop_all(bind=engine)
