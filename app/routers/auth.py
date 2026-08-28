from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.schemas import UserCreate,UserResponse,LoginRequest,Token
from app.database import Base
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
def login(logreq:LoginRequest,db:Session = Depends(get_db)):
    user = db.query(User).filter(User.username == logreq.username).first()
    if not user:
        raise HTTPException(status_code=404,detail="user not found")
    verified = verify_password(logreq.password, user.password_hash)
    if not verified:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return Token(access_token=token, token_type="bearer")
@router.get("/just_check")
def check_pass():
    return {f"ALGORITHM":f"{SECRET_KEY}"}