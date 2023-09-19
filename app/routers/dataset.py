from fastapi import APIRouter
from fastapi import status


router = APIRouter()


@router.get("/read", status_code=status.HTTP_200_OK)
def read():
    return
