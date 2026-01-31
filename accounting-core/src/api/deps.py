from collections.abc import Generator
from typing import Annotated

from database import session
from fastapi import Depends
from sqlalchemy.orm import Session


def get_db_session() -> Generator[Session]:
    db = session()
    try:
        yield db
    finally:
        db.close()


get_db_session_dep = Annotated[Session, Depends(get_db_session)]
