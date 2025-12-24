from passlib.context import CryptContext
from datetime import datetime, timedelta
from uuid import UUID

from starlette.status import HTTP_401_UNAUTHORIZED
from app.core.config import settings
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.db.helpers.user import get_user_by_uuid
from app.models.user import User 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") 

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def create_access_token(subject: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": subject, "exp": expire}

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exemption = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id: str | None = payload.get("sub")

        if user_id is None:
            raise credentials_exemption
        
        try:
            user_uuid = UUID(user_id)
        except (ValueError, TypeError):
            raise credentials_exemption
    except JWTError:
        raise credentials_exemption

    return get_user_by_uuid(db, user_uuid)