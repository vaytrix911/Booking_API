from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str = Field(min_length=6)
class UserResponse(BaseModel):
    id : int
    username : str
    model_config = ConfigDict(from_attributes=True)
class LoginRequest(BaseModel):
    username : str
    password : str
class Token(BaseModel):
    access_token: str
    token_type: str
class AppointmentCreate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
class AppointmentResponse(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    owner_id: int
    
    model_config = ConfigDict(from_attributes=True)
class AppointmentUpdate(BaseModel):
    title: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None