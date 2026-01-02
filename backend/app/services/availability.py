import uuid
from sqlalchemy.orm import Session
from app.models.coach_availability import CoachAvailability
from datetime import time

def has_overlay(*, db: Session, coach_id: uuid, day_of_week: int, start_time: time, end_time: time) -> bool:
    return (
        db.query(CoachAvailability)
        .filter(
            CoachAvailability.coach_id == coach_id,
            CoachAvailability.day_of_week == day_of_week,
            CoachAvailability.start_time < end_time,
            CoachAvailability.end_time > start_time,
        )
        .first()
        is not None
    )