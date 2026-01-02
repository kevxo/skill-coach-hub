from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db

from app.schemas.coach_availability import AvailabilityCreate, AvailabilityResponse
from app.core.security import get_current_user
from app.models.user import User
from app.services.availability import has_overlay
from app.db.helpers.availability import new_availability, all_my_availabilities, delete_my_availability

router = APIRouter(prefix="/availability", tags=["availability"])

@router.post("", response_model=AvailabilityResponse)
def create_availability(payload: AvailabilityCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if has_overlay(db=db, coach_id=current_user.id, day_of_week=payload.day_of_week, start_time=payload.start_time, end_time=payload.end_time):
        raise HTTPException(
            status_code=400,
            detail="Availability overlaps with existing time slot"
        )

    return new_availability(current_user, payload, db)

@router.get("/me", response_model=list[AvailabilityResponse])
def get_all_my_availabilities(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return all_my_availabilities(db, current_user)

@router.delete("/{availability_id}", status_code=204)
def delete_availability(
    availability_id: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    delete_my_availability(availability_id, db, current_user)
