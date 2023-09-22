from pydantic import BaseModel, Field


class DatasetResponse(BaseModel):
    id: int
    temperature: float
    moisture: float
    atmospheric_station: float = Field(alias="atmosphericStation")
    atmospheric_sea: float = Field(alias="atmosphericSea")
    wind: float
    rain_mm: float
    direction_wind: float = Field(alias="directionWind")
    uv: float

    class Config:
        from_attributes = True
        populate_by_name = True
