from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import Temperature
from app.dtos.dataset import DatasetResponse


router = APIRouter()


@router.get(
    "/read", status_code=status.HTTP_200_OK, response_model=List[DatasetResponse]
)
def read(
    db: Session = Depends(get_db),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1),
):
    query = db.query(Temperature)
    if page and page_size:
        query = query.limit(page_size).offset((page - 1) * page_size)
    return query.all()
