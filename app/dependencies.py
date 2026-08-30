from fastapi import HTTPException
from jose import JWTError,jwt
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from app.models import User
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
def get_current_user(token:str=Depends(oauth2_scheme),db:Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    user:object =db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401,detail="user not found")
    return user