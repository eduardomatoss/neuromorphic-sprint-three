from logging import getLogger

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from sqlalchemy.orm import Session
from dynaconf import settings

from app.database.connection import get_db
from app.database.models import Temperature as TemperatureModel
from app.services.thingspeak_api import ThingspeakApiClient


router = APIRouter()
logger = getLogger()
thingspeak_api_client = ThingspeakApiClient(uri=settings("thingspeak_api_url"))


@router.post("/ingest", status_code=status.HTTP_201_CREATED)
def ingest(db: Session = Depends(get_db)):
    logger.info("Getting temperature data in thingspeak api")
    thingspeak_list = thingspeak_api_client.get_data()

    logger.info("Saving temperature data in the database")

    for thingspeak_data in thingspeak_list.feeds:
        try:
            db_temperature = TemperatureModel(
                temperature=thingspeak_data.temperature,
                moisture=thingspeak_data.moisture,
                atmospheric_station=thingspeak_data.atmospheric_station,
                atmospheric_sea=thingspeak_data.atmospheric_sea,
                wind=thingspeak_data.wind,
                rain_mm=thingspeak_data.rain_mm,
                direction_wind=thingspeak_data.direction_wind,
                uv=thingspeak_data.uv,
            )
            db.add(db_temperature)
            db.commit()
        except Exception as error:
            logger.error(error)
