from app.models.user import User
from app.schemas.user import UserUpdate
from sqlalchemy.orm import Session
import uuid

def get_user_by_uuid(db: Session, uuid: uuid) -> User | Exception:
    user = db.query(User).filter(User.id == uuid).first()

    if user is None:
        raise Exception(
            {
                "message": "Could not validate credentials", 
                "status_code": 401
            }
        )

    return user

def update_user_profile(db: Session, payload: UserUpdate, current_user: User):
    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data:
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)

    return current_user
