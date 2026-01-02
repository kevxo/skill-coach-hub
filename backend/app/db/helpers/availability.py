from sqlalchemy.orm import Session
from app.models.coach_availability import CoachAvailability
from app.models.user import User
from app.schemas.coach_availability import AvailabilityCreate

def new_availability(user: User, payload: AvailabilityCreate, db: Session):
    availability = CoachAvailability(
        coach_id=user.id,
        day_of_week=payload.day_of_week,
        start_time=payload.start_time,
        end_time=payload.end_time
    )

    db.add(availability)
    db.commit()
    db.refresh(availability)

    return availability