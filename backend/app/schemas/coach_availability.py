from pydantic import BaseModel, field_validator
from datetime import time
from uuid import UUID

class AvailabilityCreate(BaseModel):
    day_of_week: int
    start_time: time
    end_time: time

    @field_validator("day_of_week")
    @classmethod
    def validate_day(cls, v):
        if v < 0 or v > 6:
            raise ValueError("day_of_week must be between 0 and 6")
        
        return v

    @field_validator("end_time")
    @classmethod
    def validate_time_order(cls, v, info):
        start = info.data.get("start_time")
        if start and v <= start:
            raise ValueError("end_time must be after start_time")

        return v

class AvailabilityResponse(AvailabilityCreate):
    id: UUID