from fastapi import HTTPException
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

def all_my_availabilities(user: User, db: Session):
    availabilities = (
        db.query(CoachAvailability)
        .filter(CoachAvailability.coach_id == user.id)
        .order_by(
            CoachAvailability.day_of_week,
            CoachAvailability.start_time,
        )
        .all()
    )

    return availabilities

def delete_my_availability(id: str, db: Session, user: User):
    availability = (
        db.query(CoachAvailability)
        .filter(
            CoachAvailability.id == id, 
            CoachAvailability.coach_id == user.id
        )
        .first()
    )

    if not availability:
        raise HTTPException(status_code=404, detail="Availability not found")

    db.delete(availability)
    db.commit()
