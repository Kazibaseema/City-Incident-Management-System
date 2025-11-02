from pydantic import BaseModel, Field
from datetime import datetime

class IncidentIn(BaseModel):
    id: str = Field(..., description="Service request id")
    type: str
    description: str
    reported_at: datetime
    lon: float
    lat: float
    address: str | None = None
