from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserCreate, UserLogin, Token, UserResponse
from app.models.user import User
from app.core.security import verify_password, create_access_token
from app.db.deps import get_db
from app.db.helpers.auth import register_user, get_user_by_email
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    db_user = register_user(db, user)

    return db_user

@router.post("/login", response_model=Token)
def login(login_user: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_email(db, login_user.email)
   
    if not verify_password(login_user.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return Token(access_token=create_access_token(user.email), token_type="bearer")