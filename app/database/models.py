from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    Float,
)


Base = declarative_base()


class Temperature(Base):
    __tablename__ = "temperature"
    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float)
    moisture = Column(Float)
    atmospheric_station = Column(Float)
    atmospheric_sea = Column(Float)
    wind = Column(Float)
    rain_mm = Column(Float)
    direction_wind = Column(Float)
    uv = Column(Float)
