from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EarthquakeCreate(BaseModel):

    time: datetime
    latitude: float
    longitude: float
    depth: float
    magnitude: float
    place: str


class EarthquakeUpdate(BaseModel):

    time: Optional[datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    depth: Optional[float] = None
    magnitude: Optional[float] = None
    place: Optional[str] = None