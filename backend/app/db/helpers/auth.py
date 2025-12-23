from app.schemas.user import UserCreate
from app.models.user import User
from app.core.security import hash_password
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


def register_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
    db_user = User(email=user.email, password=hashed_password, first_name=user.first_name, last_name=user.last_name, role=user.role)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_user_by_email(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid email. Email not found.")

    return user