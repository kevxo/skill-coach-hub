from app.models.user import User
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