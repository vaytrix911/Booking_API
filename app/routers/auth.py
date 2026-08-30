from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.schemas import UserCreate,UserResponse,LoginRequest,Token
from app.database import get_db
from app.security import hash_password,create_access_token,verify_password
from app.models import User
from dotenv import load_dotenv
from jose import jwt
from datetime import datetime, timedelta
import os
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
router = APIRouter()
@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="username already exists")
    hashed_password = hash_password(user.password)
    new_user = User(
        username = user.username,
        password_hash = hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
@router.post("/login")
def login(logreq: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == logreq.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    verified = verify_password(logreq.password, user.password_hash)
    if not verified:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(int(payload.get("sub")))
    return Token(access_token=token, token_type="bearer")