from fastapi import HTTPException, status
from sqlalchemy.orm import Session


def get_or_404(db: Session, model, id: int):
    obj = db.get(model, id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'{model.__name__} not found',
        )
    return obj
