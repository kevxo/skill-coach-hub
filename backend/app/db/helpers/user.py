from fastapi import HTTPException
from app.models.user import User
from app.schemas.user import UserUpdate
from sqlalchemy.orm import Session
from app.core.config import settings
import uuid

from app.core.s3 import generate_presigned_upload_url

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

    for field, value in update_data.items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)

    return current_user


def update_user_avatar(content_type: str, db: Session, user: User):
    if not content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image type")

    key = f"avatars/{user.id}/{uuid.uuid4()}"

    upload_url = generate_presigned_upload_url(
        bucket=settings.AWS_S3_BUCKET,
        key=key,
        content_type=content_type
    )

    avatar_url = f"https://{settings.AWS_S3_BUCKET}.s3.amazonaws.com/{key}"

    user.avatar_url = avatar_url

    db.commit()
    db.refresh(user)

    return {
        "upload_url": upload_url,
        "avatar_url": avatar_url
    }
