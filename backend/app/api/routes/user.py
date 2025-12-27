from fastapi import APIRouter, Depends
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.core.security import get_current_user
from sqlalchemy.orm import Session
from app.db.deps import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch("/me", response_model=UserResponse)
def update_user(
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_user_profile(db, payload, current_user)