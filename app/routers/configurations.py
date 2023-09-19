from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import Example


router = APIRouter()


@router.post("/ingest", status_code=status.HTTP_201_CREATED)
def ingest(db: Session = Depends(get_db)):
    get_data = db.query(Example).all()

    if get_data:
        return get_data
    return []
