from typing import List
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json, Undefined, config


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(frozen=False)
class FeedBase:
    temperature: float = field(metadata=config(field_name="field1"), default=0.0)
    moisture: float = field(metadata=config(field_name="field2"), default=0.0)
    atmospheric_station: float = field(
        metadata=config(field_name="field3"), default=0.0
    )
    atmospheric_sea: float = field(metadata=config(field_name="field4"), default=0.0)
    wind: float = field(metadata=config(field_name="field5"), default=0.0)
    rain_mm: float = field(metadata=config(field_name="field6"), default=0.0)
    direction_wind: float = field(metadata=config(field_name="field7"), default=0.0)
    uv: float = field(metadata=config(field_name="field8"), default=0.0)


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(frozen=False)
class ThingspeakResponse:
    feeds: List[FeedBase] = field(default=None)
